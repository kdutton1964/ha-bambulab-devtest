"""Config flow to configure Bambu Lab."""
from __future__ import annotations

import voluptuous as vol

from collections.abc import Awaitable
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.config_entry_flow import DiscoveryFlowHandler

from .const import DOMAIN, LOGGER


async def _async_has_devices(_: HomeAssistant) -> bool:
    return True


class BambuLabFlowHandler(DiscoveryFlowHandler[Awaitable[bool]], domain=DOMAIN):
    """Handle Bambu Lab config flow. The MQTT step is inherited from the parent class."""

    VERSION = 1

    discovered_device: str

    def __init__(self) -> None:
        """Set up the config flow."""
        super().__init__(DOMAIN, "Bambu Lab", _async_has_devices)

    # async def async_step_confirm(
    #         self, user_input: dict[str, Any] | None = None
    # ) -> FlowResult:
    #     """Confirm setup."""
    #
    #     if user_input is None:
    #         return self.async_show_form(
    #             step_id="confirm",
    #         )
    #
    #     return await super().async_step_confirm(user_input)

    async def async_step_mqtt(self, discovery_info) -> FlowResult:
        s = discovery_info.topic
        serial = s.split('/')[1]
        self.discovered_device = serial

        await self.async_set_unique_id(serial)
        self._abort_if_unique_id_configured()
        return await self.async_step_mqtt_confirm()

    async def async_step_mqtt_confirm(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(
                title=user_input['name'],
                data={
                    "serial_number": self.discovered_device
                }
            )

        return self.async_show_form(
            step_id="mqtt_confirm",
            description_placeholders={"name": self.discovered_device},
            data_schema=vol.Schema({vol.Required("name"): str})
        )
