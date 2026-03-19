from __future__ import annotations

import asyncio
import time
from typing import Any

import aiohttp

from .const import DEVICE_INFO_URL, DEVICES_URL, LOGIN_URL


class NinebotApiError(Exception):
    """Base Ninebot API error."""


class NinebotAuthError(NinebotApiError):
    """Raised when auth fails."""


class NinebotNoDevicesError(NinebotApiError):
    """Raised when account has no devices."""


class NinebotClient:
    def __init__(self, session: aiohttp.ClientSession, username: str, password: str, language: str = "zh") -> None:
        self._session = session
        self._username = username
        self._password = password
        self._language = language
        self._token: str | None = None

    async def async_login(self) -> str:
        payload = {"username": self._username, "password": self._password}
        headers = {
            "clientId": "open_claw_client",
            "timestamp": str(int(time.time() * 1000)),
            "Content-Type": "application/json",
        }
        data = await self._async_request("POST", LOGIN_URL, headers=headers, json=payload)
        token = ((data.get("data") or {}).get("access_token"))
        if not token:
            code = data.get("resultCode") or data.get("code")
            desc = data.get("resultDesc") or data.get("desc") or "login failed"
            if code in {"00002", "401", 401}:
                raise NinebotAuthError(f"{code}: {desc}")
            raise NinebotApiError(f"Login failed: {code} {desc}")
        self._token = token
        return token

    async def async_get_devices(self) -> list[dict[str, Any]]:
        token = self._token or await self.async_login()
        payload = {"access_token": token, "lang": self._language}
        data = await self._async_request("POST", DEVICES_URL, json=payload)
        if data.get("code") in {401903, 401, "401"}:
            self._token = None
            token = await self.async_login()
            payload = {"access_token": token, "lang": self._language}
            data = await self._async_request("POST", DEVICES_URL, json=payload)
        devices = data.get("data") or []
        if not devices:
            raise NinebotNoDevicesError("No devices returned")
        return devices

    async def async_get_device_info(self, sn: str) -> dict[str, Any]:
        token = self._token or await self.async_login()
        payload = {"access_token": token, "sn": sn}
        data = await self._async_request("POST", DEVICE_INFO_URL, json=payload)
        if data.get("code") in {401903, 401, "401"}:
            self._token = None
            token = await self.async_login()
            payload = {"access_token": token, "sn": sn}
            data = await self._async_request("POST", DEVICE_INFO_URL, json=payload)
        return data

    async def async_get_device_snapshot(self, selected_sn: str | None = None) -> dict[str, Any]:
        devices = await self.async_get_devices()
        selected = None
        if selected_sn:
            selected = next((device for device in devices if str(device.get("sn")) == selected_sn), None)
        if selected is None:
            selected = devices[0]
        sn = str(selected.get("sn"))
        info_raw = await self.async_get_device_info(sn)
        info = info_raw.get("data") or {}
        location = (info.get("locationInfo") or {}).get("locationDesc")
        return {
            "device": selected,
            "devices": devices,
            "info": info_raw,
            "sn": selected.get("sn"),
            "device_name": selected.get("deviceName"),
            "battery": info.get("dumpEnergy"),
            "estimate_mileage": info.get("estimateMileage"),
            "location": location,
            "location_info": info.get("locationInfo") or {},
            "charging_state": info.get("chargingState"),
            "power_status": info.get("powerStatus"),
            "pwr": info.get("pwr"),
            "gsm": info.get("gsm"),
            "gsm_time": info.get("gsmTime"),
            "remain_charge_time": info.get("remainChargeTime"),
            "wnumber": info.get("wnumber"),
        }

    async def _async_request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        timeout = aiohttp.ClientTimeout(total=20)
        try:
            async with self._session.request(method, url, timeout=timeout, **kwargs) as response:
                data = await response.json(content_type=None)
                if response.status == 401:
                    raise NinebotAuthError(str(data))
                if response.status >= 400:
                    raise NinebotApiError(f"HTTP {response.status}: {data}")
                return data
        except NinebotApiError:
            raise
        except asyncio.TimeoutError as err:
            raise NinebotApiError("Request timeout") from err
        except aiohttp.ClientError as err:
            raise NinebotApiError(str(err)) from err
