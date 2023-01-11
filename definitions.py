"""Definitions for Bambu Lab sensors added to MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import (
    POWER_WATT,
    TEMPERATURE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    SPEED)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.util import dt as dt_util


def trim_wifi(string):
    return string.replace("dBm", "")


@dataclass
class BambuLabSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Bambu Lab."""

    state: Callable | None = None


SENSORS: tuple[BambuLabSensorEntityDescription, ...] = (
    BambuLabSensorEntityDescription(
        key="print.wifi_signal",
        name="Wi-Fi Signal",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        state=trim_wifi
    ),
    BambuLabSensorEntityDescription(
        key="print.bed_temper",
        name="Current Bed Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    )
)
