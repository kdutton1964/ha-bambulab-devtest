"""Definitions for Bambu Lab sensors added to MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import (
    POWER_WATT,
    PERCENTAGE,
    TEMPERATURE,
    UnitOfTemperature,
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

def fan_to_percent(speed):
    return round(int(speed)/15)*100


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
        name="Bed Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BambuLabSensorEntityDescription(
        key="print.bed_target_temper",
        name="Target Bed Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BambuLabSensorEntityDescription(
        key="print.chamber_temper",
        name="Chamber Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BambuLabSensorEntityDescription(
        key="print.nozzle_target_temper",
        name="Nozzle Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BambuLabSensorEntityDescription(
        key="print.nozzle_temper",
        name="Nozzle Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BambuLabSensorEntityDescription(
        key="print.cooling_fan_speed",
        name="Cooling Fan Speed",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        state=fan_to_percent
    ),
    BambuLabSensorEntityDescription(
        key="print.big_fan1_speed",
        name="Big Fan 1 Speed",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        state=fan_to_percent
    ),
    BambuLabSensorEntityDescription(
        key="print.big_fan2_speed",
        name="Big Fan 2 Speed",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        state=fan_to_percent
    ),
    BambuLabSensorEntityDescription(
        key="print.heatbreak_fan_speed",
        name="Heatbreak Fan Speed",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        state=fan_to_percent
    )

)
