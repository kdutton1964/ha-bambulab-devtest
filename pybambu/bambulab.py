"""Asynchronous Python client for Bambu Lab Printers."""
from __future__ import annotations

import json
import asyncio
import logging

from dataclasses import dataclass
from paho.mqtt import client as mqtt_client

from .models import Device

from .exceptions import (
    BambuLabError,
    BambuLabConnectionError,
    BambuLabConnectionClosed,
    BambuLabUnsupportedFeature,
    BambuLabConnectionTimeoutError
)

LOGGER = logging.getLogger(__name__)


@dataclass
class BambuLab:
    """Main class for handling connections with Bambu Printers."""

    host: str
    _client: mqtt_client.Client | None = None
    _close_session: bool = False
    _device: Device | None = None
    _connected: bool = False

    @property
    def connected(self):
        LOGGER.debug(f"connected() {self._connected}")
        return self._connected

    def on_connect(self, client, userdata, flags, rc):
        LOGGER.debug("on_connect() Connected with result code " + str(rc))

        if rc == 0:
            LOGGER.debug("on_connect() Connected to MQTT Broker!")
            self._connected = True
        else:
            LOGGER.debug("on_connect() Failed to connect, return code %d\n", rc)

    async def connect(self):
        """ Connect to the MQTT Server of a Bambu Printer

        Raises:
            BambuLabConnectionError: Error occurred while communicating with Bambu Printer
        """

        LOGGER.debug(f"connect() Connecting MQTT Server on: {self.host}")
        self._client = mqtt_client.Client()
        self._client.on_connect = self.on_connect
        self._client.connect(self.host, 1883)
        self._client.loop_start()
        await asyncio.sleep(5)
        return self._client

    async def subscribe(self, callback):
        def on_message(client, userdata, msg):
            while not self._connected:
                LOGGER.debug("subcribe() on_message() received message")
                if self._device is None:
                    self._device = Device(json.loads(msg.payload))

                self._device.update_from_dict(data=json.loads(msg.payload))
                LOGGER.debug('subscribe() on_message() Device Update')
                return callback(self._device)

        if not self._client or not self._connected:
            raise BambuLabError(f"Not connected to MQTT Server {self._connected}")

        LOGGER.debug("subscribe() Subscribing ")
        self._client.on_message = on_message
        self._client.subscribe("device/#")
        # return

    async def disconnect(self):
        """Disconnect from the MQTT Server of a Bambu Printer."""
        if not self._client:
            LOGGER.debug("Cannot disconnect from MQTT Server, as no client connection exists")
            return

        LOGGER.debug("disconnect() Disconnecting....")
        self._client.loop_stop()
        self._client.disconnect()
        self._connected = False
        LOGGER.debug("disconnect() Disconnected")
        return

    async def get_device(self):
        device = None

        def new_update(cb):
            nonlocal device
            LOGGER.debug(f"get_device() new_update() {cb.__dict__}")
            device = cb

        LOGGER.debug("get_device() Connecting")
        await self.connect()
        asyncio.create_task(self.subscribe(callback=new_update))
        await asyncio.sleep(5)
        LOGGER.debug("get_device() Disconnecting")
        await self.disconnect()
        return device

    async def __aenter__(self):
        """Async enter.

        Returns:
            The BambuLab object.
        """
        return self

    async def __aexit__(self, *_exc_info):
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.disconnect()
