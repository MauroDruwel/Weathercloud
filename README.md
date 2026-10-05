# weathercloud

[![PyPI](https://img.shields.io/pypi/v/weathercloud.svg)](https://pypi.org/project/weathercloud/)
[![Python](https://img.shields.io/pypi/pyversions/weathercloud.svg)](https://pypi.org/project/weathercloud/)
[![CI](https://github.com/MauroDruwel/Weathercloud/actions/workflows/ci.yml/badge.svg)](https://github.com/MauroDruwel/Weathercloud/actions/workflows/ci.yml)
[![Cloudflare Forge](https://github.com/MauroDruwel/Weathercloud/actions/workflows/forge.yml/badge.svg)](https://github.com/MauroDruwel/Weathercloud/actions/workflows/forge.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Official schema-first, fully-typed Python SDK for [Weathercloud](https://app.weathercloud.net).
Powered by **Cloudflare Forge** and Fern code generation from the canonical [`openapi.yaml`](./openapi.yaml) definition.

Read live sensor conditions, station metadata, historical evolution, popular stations, airport METARs, and forecasts from any public station — **no account, no API key required** for public data.

> ⚠️ Reverse-engineered from the public web app. Not affiliated with or endorsed
> by Weathercloud; upstream endpoints may change without notice.

---

## 📢 Version 1.0.0 Breaking Changes & Deprecation Notice

> [!WARNING]
> **`weathercloud >= 1.0.0` is a complete schema-first rewrite.**
>
> All legacy `v0.1.x` methods (`get_current_conditions()`, `get_station_info()`, `CurrentConditions`, `StationInfo`, `VariableCode`, `WeathercloudError`) are **deprecated and removed** in favor of direct, typed sub-clients (`client.device_live`, `client.forecast`, etc.) returning Pydantic v2 models.
>
> If you are maintaining an existing integration (such as Home Assistant), see the [Migration Guide (v0.1.x → v1.0.0)](#-migration-guide-v01x--v100) below.

---

## ✨ Highlights

- ⚡ **100% Schema-First Architecture** — Zero handwritten HTTP boilerplate. The entire Python SDK is generated directly from [`openapi.yaml`](./openapi.yaml) via Fern.
- 🏗️ **Sync & Async Out-of-the-Box** — Includes both `WeathercloudClient` and `AsyncWeathercloudClient` powered by modern `httpx` with automatic retries and connection pooling.
- 🧱 **Strict Pydantic v2 Typing** — Strongly-typed models (`DeviceValues`, `DeviceInfo`, `DeviceStats`, `ForecastResponse`) with validation and serialization.
- 🤖 **Native Model Context Protocol (MCP)** — Powered directly by `@cloudflare/forge-mcp` from `openapi.yaml` for Claude Desktop, Cursor, and AI coding agents.
- 📚 **Interactive API Portal** — Saturn-themed [Scalar API reference](https://weathercloud-api.maurodruwel.be) with instant search, dark mode, and native Python snippets.
- 🧪 **Strictly Tested & Typed** — Ships `py.typed`, passes `mypy` and `ruff`, and supports Python 3.10–3.13.

---

## 📦 Installation

```sh
pip install weathercloud
```

Or with `uv`:

```sh
uv add weathercloud
```

---

## 🚀 Quick start

### Synchronous Client

```python
from weathercloud import WeathercloudClient

client = WeathercloudClient()

# Live weather sensor readings:
values = client.device_live.get_values(device_id="5726468552")
print(f"Temperature: {values.temp}°C, Humidity: {values.hum}%, Pressure: {values.bar} hPa")

# Station metadata:
info = client.device_live.get_info(device_id="5726468552")
print(f"Station: {info.device.name} in {info.device.city}, Status: {info.values.status}")

# Airport METAR weather (ICAO code):
metar = client.metar.get_values(device_id="EBBR")
print(f"EBBR Pressure: {metar.bar} hPa, Wind Speed: {metar.wspd} m/s")
```

### Asynchronous Client (`httpx`-powered, ideal for Home Assistant)

```python
import asyncio
from weathercloud import AsyncWeathercloudClient

async def main():
    client = AsyncWeathercloudClient()

    # Direct non-blocking async calls — no executor needed!
    values = await client.device_live.get_values(device_id="5726468552")
    print(f"Async Temp: {values.temp}°C")

asyncio.run(main())
```

---

## 📖 API Reference

All operations are grouped into typed sub-clients:

| Sub-client | Method | Return Type | Description |
|---|---|---|---|
| `client.device_live` | `get_values(device_id=...)` | `DeviceValues` | Real-time weather sensor readings |
| `client.device_live` | `get_info(device_id=...)` | `DeviceInfo` | Station metadata, model, update interval |
| `client.device_live` | `get_stats(code=...)` | `DeviceStats` | Daily/monthly/yearly min-max statistics |
| `client.device_history` | `get_evolution(device=..., variable=..., period=...)` | `EvolutionResponse` | Hourly bucket historical time-series |
| `client.forecast` | `get_daily(id=...)` | `ForecastResponse` | 6-day WMO daily weather forecast |
| `client.stations` | `get_popular(country=..., period=...)` | `PageDevicesResponse` | Top-ranked popular weather stations |
| `client.stations` | `get_nearby(lat=..., lon=..., km=...)` | `PageDevicesResponse` | Stations within a radius of GPS coordinates |
| `client.metar` | `get_values(device_id=...)` | `DeviceValues` | Official airport METAR observation |
| `client.map_` | `get_devices(...)` | `MapDevicesResponse` | Bounding box station discovery |
| `client.auth` | `login(...)` | `str` | Account sign-in for private indoor sensors |

### Error Handling

All failed API requests raise `ApiError` with HTTP status code and response body:

```python
from weathercloud import WeathercloudClient
from weathercloud.core.api_error import ApiError

client = WeathercloudClient()

try:
    values = client.device_live.get_values(device_id="5726468552")
except ApiError as e:
    print(f"API Error ({e.status_code}): {e.body}")
```

---

## 🔄 Migration Guide (v0.1.x → v1.0.0)

If you are upgrading from `weathercloud < 1.0.0`:

### 1. Live Readings
- **Old**: `cond = client.get_current_conditions("5726468552")` -> `cond.temperature`, `cond.humidity`, `cond.wind_speed`
- **New**: `values = client.device_live.get_values(device_id="5726468552")` -> `values.temp`, `values.hum`, `values.wspd`

### 2. Station Metadata
- **Old**: `info = client.get_station_info("5726468552")` (scraped HTML from web page)
- **New**: `info = client.device_live.get_info(device_id="5726468552")` -> `info.device.name`, `info.device.city`, `info.device.altitude`, `info.values.status`

### 3. Error Handling
- **Old**: `except WeathercloudError:`
- **New**: `from weathercloud.core.api_error import ApiError` -> `except ApiError as e:`

### 4. Async Support
- **Old**: Sync only (`requests`). Required `hass.async_add_executor_job()`.
- **New**: Native `AsyncWeathercloudClient` with `await client.device_live.get_values(...)`.

---

## 🤖 Model Context Protocol (MCP) for AI Agents

Because this repository is built on Cloudflare Forge, MCP is served directly from [`openapi.yaml`](./openapi.yaml) via `@cloudflare/forge-mcp` with zero custom code:

Add to your `claude_desktop_config.json` or Cursor MCP configuration:

```json
{
  "mcpServers": {
    "weathercloud": {
      "command": "npx",
      "args": [
        "-y",
        "@cloudflare/forge-mcp",
        "--spec",
        "https://raw.githubusercontent.com/MauroDruwel/Weathercloud/main/openapi.yaml"
      ]
    }
  }
}
```

---

## ⚡ Cloudflare Forge Pipeline

A unified developer script powers both local validation and CI:

```sh
# Lint OpenAPI spec and check Fern workspace
python scripts/forge.py lint

# Generate typed Python SDK (default)
python scripts/forge.py generate

# Generate other language SDKs from the same OpenAPI specification:
python scripts/forge.py generate --target csharp      # C# (.NET 8/Standard) SDK in sdks/csharp/
python scripts/forge.py generate --target typescript  # TypeScript SDK in sdks/typescript/
python scripts/forge.py generate --target go          # Go module SDK in sdks/go/
python scripts/forge.py generate --target all         # Generate all SDKs simultaneously

# Build interactive Scalar documentation in docs/index.html
python scripts/forge.py docs

# Run Python SDK test suite
python scripts/forge.py test

# Build distribution packages (wheel + sdist)
python scripts/forge.py build

# Execute full pipeline end-to-end
python scripts/forge.py all
```

---

## 🛠️ Development

```sh
git clone https://github.com/MauroDruwel/Weathercloud
cd Weathercloud

uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Lint and type check
uv run ruff check .
uv run mypy

# Run test suite
uv run pytest -v

# Run entire Forge pipeline
python scripts/forge.py all
```

---

## 📄 License

[MIT](LICENSE)
