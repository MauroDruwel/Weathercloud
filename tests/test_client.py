from __future__ import annotations

from typing import Any

import httpx
import pytest

from weathercloud import (
    AsyncWeathercloudClient,
    DeviceInfo,
    DeviceStats,
    DeviceValues,
    ForecastResponse,
    PageDevicesResponse,
    WeathercloudClient,
)
from weathercloud.core.api_error import ApiError

BASE = "https://app.weathercloud.net"
DEVICE_ID = "5726468552"
ICAO_ID = "EBBR"

VALUES_PAYLOAD = {
    "epoch": 1748358122,
    "temp": "22.8",
    "dew": "15.1",
    "chill": "22.8",
    "heat": "23.0",
    "hum": "62",
    "bar": "1013.2",
    "wdir": "180",
    "wdiravg": "175",
    "wspd": "1.0",
    "wspdavg": "0.8",
    "wspdhi": "1.4",
    "rainrate": "0.0",
    "rain": "2.4",
    "solarrad": "320.0",
    "uvi": "3",
    "tempin": "21.5",
    "humin": "55",
    "heatin": "22.0",
}

STATS_PAYLOAD = {
    "code": "101",
    "temp": {"cur": "22.8", "min": "14.2", "max": "26.5"},
}

DEVICE_INFO_PAYLOAD = {
    "device": {
        "name": "Station 5726468552",
        "city": "Brussels",
        "altitude": "45",
        "model": "Davis Vantage Pro2",
        "account_type": 0,
    },
    "values": {
        "status": "1",
        "seconds_since_update": 120,
    },
}

FORECAST_PAYLOAD = {
    "forecast": {
        "2026-10-01": {"temp": {"min": 12, "max": 24}, "weather": {"code": 1}}
    }
}

POPULAR_PAYLOAD = {
    "devices": [
        {"name": "Station Alpha", "code": "5726468552", "city": "Brussels"}
    ]
}


def create_mock_client(
    routes: dict[str, tuple[int, Any, dict[str, str] | None]] | None = None,
) -> WeathercloudClient:
    routes = routes or {}

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        path = request.url.raw_path.decode()
        for pattern, (status, data, headers) in routes.items():
            if pattern in url or pattern == path:
                resp_headers = headers or {"content-type": "application/json"}
                if isinstance(data, str):
                    return httpx.Response(status, text=data, headers=resp_headers)
                return httpx.Response(status, json=data, headers=resp_headers)
        return httpx.Response(404, json={"error": "Not Found"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport, base_url=BASE)
    return WeathercloudClient(base_url=BASE, httpx_client=http_client)


def create_async_mock_client(
    routes: dict[str, tuple[int, Any, dict[str, str] | None]] | None = None,
) -> AsyncWeathercloudClient:
    routes = routes or {}

    async def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        path = request.url.raw_path.decode()
        for pattern, (status, data, headers) in routes.items():
            if pattern in url or pattern == path:
                resp_headers = headers or {"content-type": "application/json"}
                if isinstance(data, str):
                    return httpx.Response(status, text=data, headers=resp_headers)
                return httpx.Response(status, json=data, headers=resp_headers)
        return httpx.Response(404, json={"error": "Not Found"})

    transport = httpx.MockTransport(handler)
    async_http_client = httpx.AsyncClient(transport=transport, base_url=BASE)
    return AsyncWeathercloudClient(base_url=BASE, httpx_client=async_http_client)


# ==============================================================================
# Synchronous Sub-Client Tests
# ==============================================================================


def test_device_live_get_values():
    client = create_mock_client({f"/device/values/{DEVICE_ID}": (200, VALUES_PAYLOAD, None)})
    res = client.device_live.get_values(device_id=DEVICE_ID)

    assert isinstance(res, DeviceValues)
    assert res.temp == 22.8
    assert res.hum == 62
    assert res.bar == 1013.2
    assert res.epoch == 1748358122
    assert res.tempin == 21.5


def test_device_live_get_stats():
    client = create_mock_client({"/device/stats": (200, STATS_PAYLOAD, None)})
    res = client.device_live.get_stats(code="101")

    assert isinstance(res, DeviceStats)


def test_device_live_get_info():
    client = create_mock_client({f"/device/info/{DEVICE_ID}": (200, DEVICE_INFO_PAYLOAD, None)})
    res = client.device_live.get_info(device_id=DEVICE_ID)

    assert isinstance(res, DeviceInfo)
    assert res.device is not None
    assert res.device.name == "Station 5726468552"
    assert res.device.city == "Brussels"
    assert res.values is not None
    assert res.values.status == "1"


def test_forecast_get_daily():
    client = create_mock_client({"/forecast/daily": (200, FORECAST_PAYLOAD, None)})
    res = client.forecast.get_daily(id=DEVICE_ID)

    assert isinstance(res, ForecastResponse)


def test_metar_get_values():
    client = create_mock_client({f"/metar/values/{ICAO_ID}": (200, VALUES_PAYLOAD, None)})
    res = client.metar.get_values(device_id=ICAO_ID)

    assert isinstance(res, DeviceValues)
    assert res.temp == 22.8


def test_stations_get_popular():
    client = create_mock_client({"/page/popular": (200, POPULAR_PAYLOAD, None)})
    res = client.stations.get_popular(country="BE", period="day")

    assert isinstance(res, PageDevicesResponse)
    assert res.devices is not None
    assert len(res.devices) == 1
    assert res.devices[0].name == "Station Alpha"


def test_error_handling_raises_api_error():
    client = create_mock_client({f"/device/values/{DEVICE_ID}": (500, {"error": "Server error"}, None)})
    with pytest.raises(ApiError) as exc_info:
        client.device_live.get_values(device_id=DEVICE_ID)

    assert exc_info.value.status_code == 500


# ==============================================================================
# Asynchronous Sub-Client Tests
# ==============================================================================


@pytest.mark.anyio
async def test_async_device_live_get_values():
    client = create_async_mock_client({f"/device/values/{DEVICE_ID}": (200, VALUES_PAYLOAD, None)})
    res = await client.device_live.get_values(device_id=DEVICE_ID)

    assert isinstance(res, DeviceValues)
    assert res.temp == 22.8
    assert res.hum == 62


@pytest.mark.anyio
async def test_async_device_live_get_info():
    client = create_async_mock_client({f"/device/info/{DEVICE_ID}": (200, DEVICE_INFO_PAYLOAD, None)})
    res = await client.device_live.get_info(device_id=DEVICE_ID)

    assert isinstance(res, DeviceInfo)
    assert res.device is not None
    assert res.device.city == "Brussels"


@pytest.mark.anyio
async def test_async_error_handling_raises_api_error():
    client = create_async_mock_client({f"/device/values/{DEVICE_ID}": (404, {"error": "Station not found"}, None)})
    with pytest.raises(ApiError) as exc_info:
        await client.device_live.get_values(device_id=DEVICE_ID)

    assert exc_info.value.status_code == 404
