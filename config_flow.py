from __future__ import annotations

import logging
import queue

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
            LOGGER.debug("Config Flow Step User, connecting to device")
            can_connect = await self.hass.async_add_executor_job(
                try_connection, user_input)

            if can_connect:
                LOGGER.debug(f"Config Flow connected to Device")

                return self.async_create_entry(
                    title="X1", data={CONF_HOST: user_input[CONF_HOST]}
                )

            errors["base"] = "cannot connect"


        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors or {},
        )

    async def _async_get_device(self, host):
        bambu = BambuLab(host)
        device = await bambu.get_device()
        LOGGER.debug(f"async get device: {device}")
        return device


def try_connection(
        user_input: dict[str, Any],
) -> bool:
    """Test if we can connect to an MQTT broker."""

    import paho.mqtt.client as mqtt  # pylint: disable=import-outside-toplevel

    client = mqtt.Client()

    result: queue.Queue[bool] = queue.Queue(maxsize=1)

    def on_connect(
            client_: mqtt.Client,
            userdata: None,
            flags: dict[str, Any],
            result_code: int,
            properties: mqtt.Properties | None = None,
    ) -> None:
        """Handle connection result."""
        result.put(result_code == mqtt.CONNACK_ACCEPTED)

        client.on_connect = on_connect

        client.connect_async(user_input[CONF_HOST], 1883)
        client.loop_start()

        try:
            return result.get(timeout=MQTT_TIMEOUT)
        except queue.Empty:
            return False
        finally:
            client.disconnect()
            client.loop_stop()
