# Weathercloud Python Library

[![PyPI version](https://img.shields.io/pypi/v/weathercloud.svg?color=blue)](https://pypi.org/project/weathercloud/)
[![Python versions](https://img.shields.io/pypi/pyversions/weathercloud.svg)](https://pypi.org/project/weathercloud/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Fern](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com)

Typed, modern Python client library for [Weathercloud](https://weathercloud.net) — query real-time weather station sensor readings, METAR airport observations, sensor statistics, and historical trends without requiring authentication or CSRF tokens.

Ideal for **Home Assistant** custom integrations, weather dashboards, automation scripts, and data analysis pipelines.

---

## Table of Contents

- [Installation](#installation)
- [Quickstart](#quickstart)
- [Live Weather Station Readings](#live-weather-station-readings)
- [Sensor Variables Reference](#sensor-variables-reference)
- [Station Profile & Metadata](#station-profile--metadata)
- [Map & Station Discovery](#map--station-discovery)
- [METAR Airport Observations](#metar-airport-observations)
- [Asynchronous Client](#asynchronous-client)
- [Error Handling](#error-handling)
- [Custom Configuration & Environments](#custom-configuration--environments)
- [Full Reference](#full-reference)

---

## Installation

```bash
pip install weathercloud
```

Or using [uv](https://github.com/astral-sh/uv) / [poetry](https://python-poetry.org):

```bash
uv add weathercloud
# or
poetry add weathercloud
```

---

## Quickstart

Get current weather readings for any public Weathercloud station using its device ID (e.g., `5726468552`):

```python
from weathercloud import WeathercloudClient

client = WeathercloudClient()

# Query live sensor readings — no login or CSRF tokens required
weather = client.device_live.get_values(device_id="5726468552")

print(f"Timestamp:   {weather.epoch}")
print(f"Temperature: {weather.temp} °C")
print(f"Humidity:    {weather.hum} %")
print(f"Pressure:    {weather.bar} hPa")
print(f"Wind Speed:  {weather.wspd} m/s (Gusts: {weather.wspdhi} m/s)")
print(f"Wind Dir:    {weather.wdir}°")
print(f"Daily Rain:  {weather.rain} mm")
```

---

## Live Weather Station Readings

### All Sensor Values

`client.device_live.get_values(device_id=...)` returns strongly-typed sensor readings:

```python
from weathercloud import WeathercloudClient

client = WeathercloudClient()
values = client.device_live.get_values(device_id="5726468552")

# Temperature & Humidity
print(f"Temp: {values.temp}°C | Dew Point: {values.dew}°C | Heat Index: {values.heat}°C | Chill: {values.chill}°C")
print(f"Humidity: {values.hum}%")

# Wind
print(f"Wind Speed: {values.wspd} m/s (Avg: {values.wspdavg} m/s, Max: {values.wspdhi} m/s)")
print(f"Direction:  {values.wdir}° (Avg: {values.wdiravg}°)")

# Barometer & Rain
print(f"Barometer:  {values.bar} hPa")
print(f"Rain Today: {values.rain} mm (Rate: {values.rainrate} mm/h)")

# Solar & UV (if supported by station hardware)
if values.uvi is not None:
    print(f"UV Index: {values.uvi}")
if values.solarrad is not None:
    print(f"Solar Radiation: {values.solarrad} W/m²")
```

---

## Sensor Variables Reference

Weathercloud reports abbreviated keys across its API. The SDK exposes these as clean, typed attributes:

| Attribute | Type | Description | Unit / Format |
|---|---|---|---|
| `epoch` | `int` | Timestamp of last sensor transmission | Unix epoch (seconds) |
| `temp` | `float` | Air temperature | °C |
| `dew` | `float` | Dew point | °C |
| `chill` | `float` | Wind chill | °C |
| `heat` | `float` | Heat index | °C |
| `hum` | `int` | Relative humidity | % (0–100) |
| `bar` | `float` | Atmospheric / barometric pressure | hPa |
| `wdir` | `int` | Instantaneous wind direction | Degrees (0–360°) |
| `wdiravg` | `int` | Average wind direction | Degrees (0–360°) |
| `wspd` | `float` | Instantaneous wind speed | m/s |
| `wspdavg` | `float` | Average wind speed | m/s |
| `wspdhi` | `float` | Peak wind gust of the day | m/s |
| `rain` | `float` | Accumulated daily precipitation | mm |
| `rainrate` | `float` | Current precipitation rate | mm/h |
| `uvi` | `float` | UV index | Index (0–16) |
| `solarrad` | `float` | Solar radiation | W/m² |

---

## Station Profile & Metadata

Retrieve station model, manufacturer, coordinates, and observer details:

```python
from weathercloud import WeathercloudClient

client = WeathercloudClient()

# Get station device info
info = client.device_live.get_info(device_id="5726468552")
if info.device:
    print(f"Station Name: {info.device.name}")
    print(f"Model:        {info.device.model}")
    print(f"Coordinates:  {info.device.latitude}, {info.device.longitude}")

# Global Weathercloud network stats
stats = client.device_live.get_stats()
print(f"Active Devices:     {stats.devices_active}")
print(f"Total Measurements: {stats.measurements_total}")
```

---

## Map & Station Discovery

Discover active weather stations within a geographic area or near coordinates:

```python
from weathercloud import WeathercloudClient

client = WeathercloudClient()

# Search stations in a latitude/longitude bounding box
devices = client.map.get_devices(
    min_lat=40.7000,
    max_lat=40.8500,
    min_lon=-74.0500,
    max_lon=-73.9000,
)

for dev in devices:
    print(f"ID: {dev.id} | Name: {dev.name} | Lat: {dev.latitude}, Lon: {dev.longitude}")
```

---

## METAR Airport Observations

Query aviation weather reports from global airport METAR stations:

```python
from weathercloud import WeathercloudClient

client = WeathercloudClient()

# Fetch airport METAR report by station / ICAO identifier
metar = client.metar.get_values(device_id="EHAM")
print(f"Airport METAR: {metar}")
```

---

## Asynchronous Client

The SDK provides a first-class `AsyncWeathercloudClient` powered by `httpx` for high-concurrency applications:

```python
import asyncio
from weathercloud import AsyncWeathercloudClient

async def fetch_stations():
    client = AsyncWeathercloudClient()
    
    station_ids = ["5726468552", "1839204918", "9283741920"]
    tasks = [client.device_live.get_values(device_id=sid) for sid in station_ids]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for sid, result in zip(station_ids, results):
        if not isinstance(result, Exception):
            print(f"Station {sid}: {result.temp}°C, {result.hum}% hum")
        else:
            print(f"Station {sid} failed: {result}")

asyncio.run(fetch_stations())
```

---

## Error Handling

All failed HTTP requests raise typed subclasses of `ApiError`:

```python
from weathercloud import WeathercloudClient
from weathercloud.core.api_error import ApiError

client = WeathercloudClient()

try:
    weather = client.device_live.get_values(device_id="nonexistent-id")
except ApiError as err:
    print(f"HTTP Status: {err.status_code}")
    print(f"Error Body:  {err.body}")
```

---

## Custom Configuration & Environments

```python
import httpx
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
    # Configure custom timeout or retries via httpx
    httpx_client=httpx.Client(timeout=10.0),
)
```

---

## Full Reference

For comprehensive API definitions, request parameters, and response schemas, see [reference.md](./reference.md).
