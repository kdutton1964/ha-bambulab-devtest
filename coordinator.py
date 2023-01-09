import asyncio
from typing import Type

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .pybambu import Device as BambuDevice, BambuLab, BambuLabError, BambuLabConnectionClosed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL


class BambuCoordinator(DataUpdateCoordinator[BambuDevice]):
    """Class to manage fetching Bambu data."""
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, *, entry: ConfigEntry) -> None:
        self.bambu = BambuLab(
            entry.data[CONF_HOST]
        )
        self.unsub: CALLBACK_TYPE | None = None
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)
        self.use_mqtt()

    @callback
    def use_mqtt(self) -> None:

        async def listen() -> None:
            """Listen for state changes via WebSocket."""

            try:
                LOGGER.debug("Connecting to Bambu")
                await self.bambu.connect()
            except BambuLabError as err:
                LOGGER.error(f"use_mqtt() connect error {err}")
                if self.unsub:
                    self.unsub
                    self.unsub = None
                return

            try:
                LOGGER.debug("Subscribing to Bambu")
                await self.bambu.subscribe(callback=self.async_set_updated_data)
            except BambuLabConnectionClosed as error:
                LOGGER.error(f"use_mqtt() subscription error {error}")
            except BambuLabError as err:
                self.async_update_listeners()
                LOGGER.error(err)


            LOGGER.debug("Disconnecting from Bambu")
            await self.bambu.disconnect()
            if self.unsub:
                self.unsub()
                self.unsub = None

        async def close_mqtt_connection(_: Event) -> None:
            """Close MQTT connection."""
            LOGGER.debug("Closing Connection")
            self.unsub = None
            await self.bambu.disconnect()

        # Clean disconnect WebSocket on Home Assistant shutdown
        self.unsub = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, close_mqtt_connection
        )

        asyncio.create_task(listen())

    async def _async_update_data(self):
        """Manually fetches data.  Probably not needed"""

        LOGGER.debug("Manually update data")

        if not self.bambu.connected and not self.unsub:
            LOGGER.debug("Not Connected")
            self.use_mqtt()
        return

