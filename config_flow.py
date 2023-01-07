from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
import random
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .pybambu import BambuLab

from .const import DOMAIN, LOGGER


class BambuLabConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle Bambu config flow"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user step."""
        errors = {}

        if user_input is not None:
            try:
                LOGGER.debug("Config Flow Step User, connecting to device")
                device = await self._async_get_device(user_input[CONF_HOST])
                LOGGER.debug(f"Config Flow connected to Device: ${device.__dict__}")

            except:
                LOGGER.error("Cannot Connect")
                errors["base"] = "cannot_connect"
            else:
                # TODO:  Need to figure out the best way to set a unique ID
                await self.async_set_unique_id(random.randint(0,1000))
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: user_input[CONF_HOST]}
                )
                return self.async_create_entry(
                    title="X1", data={CONF_HOST: user_input[CONF_HOST]}
                )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors or {},
        )

    async def _async_get_device(self, host):
        bambu = BambuLab(host)
        device = None

        async def callback(cb):
            LOGGER.debug(f'Connected: ${cb}')
            device = cb
            await bambu.disconnect()

        try:
            LOGGER.debug("Async Get Device....")
            await bambu.connect()
            LOGGER.debug("Async get device connected")
            await bambu.subscribe(callback)
            return device
        except:            
            return None