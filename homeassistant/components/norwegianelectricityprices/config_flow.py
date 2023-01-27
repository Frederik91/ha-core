"""Config flow for Norwegian Electricity Prices integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import AREA_CODES, CURRENCY_CODES, DOMAIN, TITLE

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(
            "currency", description="Enter the currency you want to use."
        ): vol.In(CURRENCY_CODES),
        vol.Required(
            "area_code", description="Select the area code for your location."
        ): vol.In(AREA_CODES),
    }
)


class InvalidData(Exception):
    """Exception for invalid data."""

    def __init__(self, errors: dict) -> None:
        """Initialize the exception."""
        super().__init__()
        self.errors = errors


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input."""
    errors = {}

    # Perform validation on the data
    if "currency" not in data:
        errors["currency"] = "Please enter a currency"
    elif data["currency"] not in CURRENCY_CODES:
        errors["currency"] = "Invalid currency"

    if "area_code" not in data:
        errors["area_code"] = "Please enter an area code"
    elif data["area_code"] not in AREA_CODES:
        errors["area_code"] = "Invalid area code"

    if errors:
        raise InvalidData(errors)

    return data


class OptionsFlowHandler(OptionsFlow):
    """Handle Norwegian Electricity Prices options."""

    def __init__(self, config_entry):
        """Initialize Norwegian Electricity Prices options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title=TITLE, data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    "currency",
                    description="Enter the currency you want to use.",
                    default=self.config_entry.options.get("currency"),
                ): vol.In(CURRENCY_CODES),
                vol.Required(
                    "area_code",
                    description="Select the area code for your location.",
                    default=self.config_entry.options.get("area_code"),
                ): vol.In(AREA_CODES),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(title=TITLE, data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Norwegian Electricity Prices."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            validation_result = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidData as ex:
            errors = ex.errors
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        if errors:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )

        await self.async_set_unique_id(
            "norwegianelectricityprices_" + user_input["area_code"]
        )
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=TITLE, data=validation_result)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
