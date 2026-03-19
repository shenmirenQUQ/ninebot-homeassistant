from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NinebotDataUpdateCoordinator


class NinebotEntity(CoordinatorEntity[NinebotDataUpdateCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: NinebotDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        device = coordinator.data.get("device") or {}
        sn = str(device.get("sn") or coordinator.entry.data.get("device_sn"))
        name = device.get("deviceName") or coordinator.entry.data.get("device_name") or sn
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, sn)},
            manufacturer="Ninebot",
            model=name,
            name=name,
        )
