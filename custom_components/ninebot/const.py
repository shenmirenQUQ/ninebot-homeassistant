from __future__ import annotations

DOMAIN = "ninebot"
PLATFORMS = ["sensor", "binary_sensor"]

CONF_DEVICE_SN = "device_sn"
CONF_DEVICE_NAME = "device_name"
CONF_LANGUAGE = "language"

DEFAULT_LANGUAGE = "zh"
DEFAULT_SCAN_INTERVAL = 300

LOGIN_URL = "https://api-passport-bj.ninebot.com/v3/openClaw/user/login"
DEVICES_URL = "https://cn-cbu-gateway.ninebot.com/app-api/inner/device/ai/get-device-list"
DEVICE_INFO_URL = "https://cn-cbu-gateway.ninebot.com/app-api/inner/device/ai/get-device-dynamic-info"

ATTR_ESTIMATE_MILEAGE = "estimate_mileage"
ATTR_GSM = "gsm"
ATTR_LOCATION = "location"
ATTR_POWER_STATUS = "power_status"
ATTR_CHARGING_STATE = "charging_state"
ATTR_SN = "sn"
