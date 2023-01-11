"""The Bambu Lab component."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN, LOGGER

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Bambu Lab integration."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the Bambu Lab integration."""
    # no data stored in hass.data
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
