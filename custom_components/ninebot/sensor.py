from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, PERCENTAGE, UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .coordinator import NinebotDataUpdateCoordinator
from .entity import NinebotEntity


@dataclass(frozen=True, kw_only=True)
class NinebotSensorDescription(SensorEntityDescription):
    value_key: str


SENSORS: tuple[NinebotSensorDescription, ...] = (
    NinebotSensorDescription(
        key="battery",
        translation_key="battery",
        name="Battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery",
    ),
    NinebotSensorDescription(
        key="estimate_mileage",
        translation_key="estimate_mileage",
        name="Estimated mileage",
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="estimate_mileage",
    ),
    NinebotSensorDescription(
        key="location",
        translation_key="location",
        name="Location",
        value_key="location",
    ),
    NinebotSensorDescription(
        key="gsm",
        translation_key="gsm",
        name="GSM",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_key="gsm",
    ),
    NinebotSensorDescription(
        key="gsm_time",
        translation_key="gsm_time",
        name="GSM update time",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TIMESTAMP,
        value_key="gsm_time",
    ),
    NinebotSensorDescription(
        key="remain_charge_time",
        translation_key="remain_charge_time",
        name="Remaining charge time",
        value_key="remain_charge_time",
    ),
    NinebotSensorDescription(
        key="pwr",
        translation_key="pwr",
        name="PWR",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_key="pwr",
    ),
    NinebotSensorDescription(
        key="sn",
        translation_key="sn",
        name="SN",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_key="sn",
    ),
    NinebotSensorDescription(
        key="wnumber",
        translation_key="wnumber",
        name="Vehicle number",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_key="wnumber",
    ),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: NinebotDataUpdateCoordinator = hass.data["ninebot"][entry.entry_id]
    async_add_entities(NinebotSensor(coordinator, description) for description in SENSORS)


class NinebotSensor(NinebotEntity, SensorEntity):
    entity_description: NinebotSensorDescription

    def __init__(self, coordinator: NinebotDataUpdateCoordinator, description: NinebotSensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.data['device_sn']}_{description.key}"

    @property
    def native_value(self) -> Any:
        key = self.entity_description.key
        if key == "gsm_time":
            value = self.coordinator.data.get("gsm_time")
            if value in (None, ""):
                return None
            try:
                return dt_util.utc_from_timestamp(int(value))
            except (TypeError, ValueError):
                return None
        return self.coordinator.data.get(self.entity_description.value_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if self.entity_description.key != "location":
            return None
        location_info = self.coordinator.data.get("location_info") or {}
        return {
            "raw_location_info": location_info,
            "device_name": self.coordinator.data.get("device_name"),
        }
