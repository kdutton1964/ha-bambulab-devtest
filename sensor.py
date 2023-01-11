"""Support for Bambu Lab through MQTT."""
from __future__ import annotations
import json
from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.issue_registry import IssueSeverity, async_create_issue
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import slugify
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, LOGGER
from .definitions import SENSORS, AMS_SENSORS, BambuLabSensorEntityDescription


async def async_setup_entry(
        _: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bambu Lab sensors from config entry."""
    async_add_entities(BambuLabSensor(description, config_entry) for description in SENSORS)
    # async_add_entities(BambuLabSensor(description, config_entry) for description in AMS_SENSORS)


class BambuLabSensor(SensorEntity):
    """Representation of a BambuLab that is updated via MQTT."""

    entity_description: BambuLabSensorEntityDescription

    def __init__(
            self, description: BambuLabSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""

        LOGGER.debug(config_entry)
        self.config_entry = config_entry
        self.entity_description = description
        slug = slugify(description.key.replace(".", "_"))
        self.entity_id = f"sensor.{slug}"
        self._attr_unique_id = f"{config_entry.entry_id}-{slug}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.config_entry.unique_id)
            },
            name=self.config_entry.title,
            manufacturer="Bambu Lab",
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        def value_of(data, location):
            for part in location.split("."):
                data = data.get(part)
                if not data:
                    return None
            return data

        @callback
        def message_received(message):
            """Handle new MQTT messages."""

            json_data = json.loads(message.payload)

            if json_data.get("print"):
                if self.entity_description.state is not None:
                    self._attr_native_value = self.entity_description.state(
                        value_of(json_data, self.entity_description.key))
                else:
                    self._attr_native_value = value_of(json_data, self.entity_description.key)

                self.async_write_ha_state()

        """ For now, manually add your device serial number below"""
        await mqtt.async_subscribe(
            self.hass, f"device/{self.config_entry.unique_id}/report", message_received, 1
        )


# class AMSSensor(SensorEntity):
#     """Representation of a BambuLab that is updated via MQTT."""
#
#     entity_description: BambuLabSensorEntityDescription
#
#     def __init__(
#             self, description: BambuLabSensorEntityDescription, config_entry: ConfigEntry
#     ) -> None:
#         """Initialize the sensor."""
#
#         self.config_entry = config_entry
#         self.entity_description = description
#         slug = slugify(description.key.replace(".", "_"))
#         self.entity_id = f"sensor.{slug}"
#         self._attr_unique_id = f"{config_entry.entry_id}-{slug}"
#
#     @property
#     def device_info(self) -> DeviceInfo:
#         """Return the device info."""
#         return DeviceInfo(
#             identifiers={
#                 (DOMAIN, f"{self.config_entry.unique_id}_ams")
#             },
#             name="Automatic Material System",
#             manufacturer="Bambu Lab",
#             model="AMS"
#         )
#
#     async def async_added_to_hass(self) -> None:
#         """Subscribe to MQTT events."""
#
#         def value_of(data, location):
#             for part in location.split("."):
#                 data = data.get(part)
#                 if not data:
#                     return None
#             return data
#
#         @callback
#         def message_received(message):
#             """Handle new MQTT messages."""
#
#             json_data = json.loads(message.payload)
#
#             if json_data.get("print").get("ams"):
#                 if self.entity_description.state is not None:
#                     self._attr_native_value = self.entity_description.state(
#                         value_of(json_data, self.entity_description.key))
#                 else:
#                     self._attr_native_value = value_of(json_data, self.entity_description.key)
#
#                 self.async_write_ha_state()
#
#         await mqtt.async_subscribe(
#             self.hass, f"device/{self.config_entry.unique_id}/report", message_received, 1
#         )
