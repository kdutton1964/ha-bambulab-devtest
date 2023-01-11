"""Config flow to configure Bambu Lab."""
from __future__ import annotations

from collections.abc import Awaitable
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.config_entry_flow import DiscoveryFlowHandler

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _async_has_devices(_: HomeAssistant) -> bool:
    return True


class BambuLabFlowHandler(DiscoveryFlowHandler[Awaitable[bool]], domain=DOMAIN):
    """Handle Bambu Lab config flow. The MQTT step is inherited from the parent class."""

    VERSION = 1

    def __init__(self) -> None:
        """Set up the config flow."""
        super().__init__(DOMAIN, "Bambu Lab", _async_has_devices)

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm setup."""
        if user_input is None:
            return self.async_show_form(
                step_id="confirm",
            )

        return await super().async_step_confirm(user_input)
