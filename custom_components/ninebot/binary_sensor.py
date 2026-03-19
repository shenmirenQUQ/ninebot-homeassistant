from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import NinebotDataUpdateCoordinator
from .entity import NinebotEntity


@dataclass(frozen=True, kw_only=True)
class NinebotBinarySensorDescription(BinarySensorEntityDescription):
    value_key: str
    on_values: tuple[int | str, ...]


BINARY_SENSORS: tuple[NinebotBinarySensorDescription, ...] = (
    NinebotBinarySensorDescription(
        key="charging",
        translation_key="charging",
        name="Charging",
        value_key="charging_state",
        on_values=(1, "1", True),
    ),
    NinebotBinarySensorDescription(
        key="power",
        translation_key="power",
        name="Powered on",
        value_key="power_status",
        on_values=(1, "1", True),
    ),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: NinebotDataUpdateCoordinator = hass.data["ninebot"][entry.entry_id]
    async_add_entities(NinebotBinarySensor(coordinator, description) for description in BINARY_SENSORS)


class NinebotBinarySensor(NinebotEntity, BinarySensorEntity):
    entity_description: NinebotBinarySensorDescription

    def __init__(self, coordinator: NinebotDataUpdateCoordinator, description: NinebotBinarySensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.data['device_sn']}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get(self.entity_description.value_key)
        if value is None:
            return None
        return value in self.entity_description.on_values
