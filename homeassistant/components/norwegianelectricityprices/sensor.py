"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .api_client import ApiClient
from .const import DOMAIN


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    api_client = hass.data[DOMAIN]
    entities = [
        CurrentScoreSensor(api_client),
        CurrentPriceSensor(api_client),
    ]
    add_entities(entities)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up entry."""
    api_client = hass.data[DOMAIN]
    entities = [
        CurrentScoreSensor(api_client),
        CurrentPriceSensor(api_client),
    ]

    async_add_devices(entities)


class CurrentScoreSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Current score"

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, api_client: ApiClient) -> None:
        """Initialize the sensor."""
        self.client = api_client

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""

        self._attr_native_value = await self.client.async_get_current_score()


class CurrentPriceSensor(SensorEntity):
    """Representation of a Sensor."""

    _client: ApiClient
    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self) -> str:
        """Name of the entity."""
        return "Current price"

    def __init__(self, api_client: ApiClient) -> None:
        """Initialize the sensor."""
        self._client = api_client

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""

        val = await self._client.async_get_current_price()
        self._attr_native_value = val
