from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import NinebotApiError, NinebotAuthError, NinebotClient, NinebotNoDevicesError
from .const import CONF_DEVICE_NAME, CONF_DEVICE_SN, CONF_LANGUAGE, DEFAULT_LANGUAGE, DOMAIN


class NinebotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._user_input: dict[str, Any] = {}
        self._devices: list[dict[str, Any]] = []

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            self._user_input = dict(user_input)
            try:
                client = NinebotClient(
                    async_get_clientsession(self.hass),
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                )
                self._devices = await client.async_get_devices()
            except NinebotAuthError:
                errors["base"] = "invalid_auth"
            except NinebotNoDevicesError:
                errors["base"] = "no_devices"
            except NinebotApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                if len(self._devices) == 1:
                    return await self._async_create_entry_for_device(self._devices[0])
                return await self.async_step_device()

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(["zh", "zh-hant", "en"]),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_device(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            sn = user_input[CONF_DEVICE_SN]
            device = next((item for item in self._devices if str(item.get("sn")) == sn), None)
            if device is not None:
                return await self._async_create_entry_for_device(device)
            errors["base"] = "unknown"

        options = {
            str(device.get("sn")): device.get("deviceName") or str(device.get("sn"))
            for device in self._devices
        }
        schema = vol.Schema({vol.Required(CONF_DEVICE_SN): vol.In(options)})
        return self.async_show_form(step_id="device", data_schema=schema, errors=errors)

    async def _async_create_entry_for_device(self, device: Mapping[str, Any]) -> FlowResult:
        sn = str(device.get("sn"))
        await self.async_set_unique_id(sn)
        self._abort_if_unique_id_configured()

        data = {
            **self._user_input,
            CONF_DEVICE_SN: sn,
            CONF_DEVICE_NAME: device.get("deviceName") or sn,
        }
        title = device.get("deviceName") or sn
        return self.async_create_entry(title=title, data=data)
