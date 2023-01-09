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

from .client import MqttClientSetup

from .const import DOMAIN, LOGGER


class BambuLabConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle Bambu config flow"""

    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user step."""

        errors: dict[str, str] = {}

        can_connect = await self.hass.async_add_executor_job(try_connection(user_input))

        if can_connect:
            return self.async_create_entry(
                title="X1", data={CONF_HOST: user_input[CONF_HOST]}
            )

        errors["base"] = "cannot connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors or {},
        )


def try_connection(user_input: dict[str, Any]) -> bool:
    import paho.mqtt.client as mqtt

    client = MqttClientSetup(user_input).client
    result: queue.Queue[bool] = queue.Queue(maxsize=1)

    def on_connect(client, userdata, flags, rc, properties):
        result.put(rc = mqtt.CONNACK_ACCEPTED)

    client.on_connect = on_connect

    client.connect_async(user_input[CONF_HOST])
    client.loop_start()

    try:
        return result.get(timeout=5)
    except queue.Empty:
        return False
    finally:
        client.disconnect()
        client.loop_stop()