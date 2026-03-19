from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NinebotApiError, NinebotAuthError, NinebotClient
from .const import CONF_DEVICE_SN, CONF_LANGUAGE, DEFAULT_LANGUAGE, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NinebotDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.client = NinebotClient(
            async_get_clientsession(hass),
            entry.data["username"],
            entry.data["password"],
            entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
        )
        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"ninebot_{entry.title}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        try:
            return await self.client.async_get_device_snapshot(self.entry.data.get(CONF_DEVICE_SN))
        except NinebotAuthError as err:
            raise UpdateFailed(f"Auth failed: {err}") from err
        except NinebotApiError as err:
            raise UpdateFailed(str(err)) from err
