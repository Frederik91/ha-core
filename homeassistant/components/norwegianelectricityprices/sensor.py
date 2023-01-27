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
    add_entities([CurrentPriceScoreSensor(api_client)])


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up entry."""
    api_client = hass.data[DOMAIN]
    async_add_devices([CurrentPriceScoreSensor(api_client)])


class CurrentPriceScoreSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Current price score"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _current_price_score = 0

    def __init__(self, api_client: ApiClient) -> None:
        """Initialize the sensor."""
        self.client = api_client

    def update(self) -> None:
        """Fetch new state data for the sensor."""

        score = self.client.get_current_price_score()
        self._current_price_score = score

    @property
    def current_price_pcore(self):
        """Return the current price score."""
        return self._current_price_score
