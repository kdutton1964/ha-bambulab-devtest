from __future__ import annotations

from typing import Any

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import datetime as dt
from homeassistant.helpers.typing import StateType

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import BambuCoordinator
from .const import DOMAIN, LOGGER
from .models import BambuEntity
from .pybambu import Device as BambuDevice
from homeassistant.const import (
    POWER_WATT,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)


@dataclass
class BambuSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[[BambuDevice], datetime | StateType]


@dataclass
class BambuSensorEntityDescription(
    SensorEntityDescription, BambuSensorEntityDescriptionMixin
):
    """Describes Bambu sensor entity."""

    exists_fn: Callable[[BambuDevice], bool] = lambda _: True


SENSORS: tuple[BambuSensorEntityDescription, ...] = (
    BambuSensorEntityDescription(
        key="wifi_signal",
        name="Wi-Fi Signal",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.network.signal_strength
    ),
)


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Evonic sensor based on a config entry."""
    coordinator: BambuCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        BambuSensorEntity(coordinator, description)
        for description in SENSORS
        if description.exists_fn(coordinator.data)
    )



def get_timestamp(time):
    datetime_object = dt.datetime.strptime(time, '%H:%M:%S')
    return dt.datetime.combine(date=dt.date.today(), time=datetime_object.time(), tzinfo=dt.datetime.now().astimezone().tzinfo)

class BambuSensorEntity(BambuEntity, SensorEntity):
    """Defines a Evonic sensor entity."""

    entity_description: BambuSensorEntityDescription

    def __init__(
            self,
            coordinator: BambuCoordinator,
            description: BambuSensorEntityDescription,
    ) -> None:
        """Initialize a Bambu sensor entity."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        # TODO: Set unique key - use serial number 
        self._attr_unique_id = f"08:e9:f6:df:e4:94_{description.key}"

    @property
    def native_value(self) -> datetime | StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
