from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

__all__ = ["VariableCode", "CurrentConditions", "StationInfo"]


class VariableCode(IntEnum):
    """Sensor variable codes used by the ``/device/evolution`` endpoint."""

    TEMPERATURE = 101
    HUMIDITY = 201
    DEW_POINT = 541
    PRESSURE = 641
    WIND_SPEED = 701
    WIND_DIRECTION = 6001
    WIND_GUST = 6501
    RAIN = 801
    RAIN_RATE = 811
    SOLAR_RADIATION = 1001
    UV_INDEX = 1101


@dataclass
class CurrentConditions:
    """Live sensor readings from ``/device/values`` — maps directly to HA sensor entities.

    Every field is optional: a station only reports the sensors it actually has,
    so any missing or unparseable reading is returned as ``None`` rather than
    raising.
    """

    epoch: int | None              # unix timestamp
    temperature: float | None      # °C
    dew_point: float | None        # °C
    wind_chill: float | None       # °C
    heat_index: float | None       # °C
    humidity: int | None           # %
    pressure: float | None         # hPa
    wind_direction: int | None     # ° instantaneous
    wind_direction_avg: int | None  # ° averaged
    wind_speed: float | None       # m/s instantaneous
    wind_speed_avg: float | None   # m/s averaged
    wind_gust: float | None        # m/s
    rain_rate: float | None        # mm/h
    rain: float | None             # mm total
    solar_radiation: float | None  # W/m²
    uv_index: float | None         # standard units; can be fractional
    inside_temperature: float | None  # °C
    inside_humidity: int | None       # %
    inside_heat_index: float | None   # °C


@dataclass
class StationInfo:
    """Station metadata combining ``/device/info`` and a scraped station name.

    ``latitude`` and ``longitude`` are populated only when ``get_station_info`` is
    called with ``fetch_location=True`` **and** the client is logged in (``/page/own``
    is the only endpoint that returns coordinates and it requires authentication).
    Both default to ``None`` so existing callers that skip location fetching are
    unaffected.
    """

    device_id: str
    name: str            # scraped from HTML — not available via JSON API
    city: str
    altitude: str        # metres (as string from API)
    status: str          # "online" | "recently_online" | "offline"
    seconds_since_update: int
    account_type: int    # 0 = free, >0 = premium
    latitude: float | None = None   # decimal degrees, None if unauthenticated or not found
    longitude: float | None = None  # decimal degrees, None if unauthenticated or not found
