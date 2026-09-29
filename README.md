# weathercloud

[![PyPI](https://img.shields.io/pypi/v/weathercloud.svg)](https://pypi.org/project/weathercloud/)
[![Python](https://img.shields.io/pypi/pyversions/weathercloud.svg)](https://pypi.org/project/weathercloud/)
[![CI](https://github.com/MauroDruwel/Weathercloud/actions/workflows/ci.yml/badge.svg)](https://github.com/MauroDruwel/Weathercloud/actions/workflows/ci.yml)
[![Cloudflare Forge](https://github.com/MauroDruwel/Weathercloud/actions/workflows/forge.yml/badge.svg)](https://github.com/MauroDruwel/Weathercloud/actions/workflows/forge.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Unofficial, fully-typed Python client for [Weathercloud](https://app.weathercloud.net).
Read live conditions, station metadata, history, and forecasts from any public
station — **no account, no API key** (recommended). Authentication is optional and only required if you want to access private indoor sensors (like inside temperature, humidity, and heat index) of a station you own.

> ⚠️ Reverse-engineered from the public web app. Not affiliated with or endorsed
> by Weathercloud, and the upstream endpoints may change without notice.

## ✨ Highlights

- 🌡️ **Typed results** — `get_current_conditions()` returns a `CurrentConditions`
  dataclass, not a bag of stringly-typed JSON.
- 🧱 **Raw access too** — every endpoint also has a `dict`-returning method when
  you need the full payload.
- 🧯 **One exception to catch** — every failure (network, HTTP, bad JSON) raises
  `WeathercloudError`.
- 🧪 **Tested & type-checked** — ships `py.typed`, runs on Python 3.10–3.13.

## 📦 Installation

```sh
pip install weathercloud
```

## 🚀 Quick start

```python
from weathercloud import WeathercloudClient

# Public data requires no login:
with WeathercloudClient() as client:
    cond = client.get_current_conditions("5726468552")

print(cond.temperature)   # 22.8
print(cond.humidity)      # 62

# Pass your credentials to fetch private indoor sensors:
with WeathercloudClient(username="my_user", password="my_password") as client:
    cond = client.get_current_conditions("5726468552")

print(cond.inside_temperature)  # 21.5 (None if not logged in)
print(cond.inside_humidity)     # 55
```

The client owns a `requests.Session`, so use it as a context manager (or call
`client.close()`) to release connections. You can also tune the request timeout:

```python
client = WeathercloudClient(timeout=30)   # seconds; default is 10
# or with both credentials and timeout:
client = WeathercloudClient(username="user", password="pass", timeout=15)
```

## 📖 API

### `get_current_conditions(device_id)` → `CurrentConditions`

Live sensor readings as a typed dataclass — the one you'll call most. Stations
only report the sensors they actually have, so **every field is optional**: a
reading the station doesn't provide comes back as `None` rather than raising.

| Field | Type | Unit | Field | Type | Unit |
|---|---|---|---|---|---|
| `temperature` | `float \| None` | °C | `pressure` | `float \| None` | hPa |
| `dew_point` | `float \| None` | °C | `wind_speed` | `float \| None` | m/s |
| `wind_chill` | `float \| None` | °C | `wind_speed_avg` | `float \| None` | m/s |
| `heat_index` | `float \| None` | °C | `wind_gust` | `float \| None` | m/s |
| `humidity` | `int \| None` | % | `wind_direction` | `int \| None` | ° |
| `rain` | `float \| None` | mm | `rain_rate` | `float \| None` | mm/h |
| `solar_radiation` | `float \| None` | W/m² | `uv_index` | `int \| None` | — |
| `inside_temperature` | `float \| None` | °C | `inside_humidity` | `int \| None` | % |
| `inside_heat_index` | `float \| None` | °C | `epoch` | `int \| None` | unix ts |

### `get_station_info(device_id, scrape_name=True)` → `StationInfo`

Station metadata. The name isn't exposed by any JSON endpoint, so it's scraped
from the page `<title>` (one extra request). Pass `scrape_name=False` to skip it
and use the `device_id` as the name instead.

```python
info = client.get_station_info("5726468552")
info.name                   # "Ginometeo"
info.city                   # "Ingelmunster"
info.altitude               # "18.0"  (metres, as string)
info.status                 # "online" | "recently_online" | "offline" | "unknown"
info.seconds_since_update   # int
info.account_type           # 0 = free, >0 = premium
```

### `get_device_stats(device_id)` → `dict`

Current readings plus day / month / year min–max. Each value is a
`[unix_timestamp, value]` pair, keyed as `{sensor}_{period}_{type}`.

```python
stats = client.get_device_stats("5726468552")
stats["temp_day_max"]       # [1748358122, 30.9]
stats["rain_month_total"]   # [1748358122, 12.4]
```

### `get_evolution(device_id, variable, period="day")` → `dict`

Hourly history for a single sensor. `period` is `"day"`, `"week"`, `"month"`, or
`"year"`.

```python
from weathercloud import VariableCode

evo = client.get_evolution("5726468552", VariableCode.TEMPERATURE, "week")
```

Available codes: `TEMPERATURE`, `HUMIDITY`, `DEW_POINT`, `PRESSURE`, `WIND_SPEED`,
`WIND_DIRECTION`, `WIND_GUST`, `RAIN`, `RAIN_RATE`, `SOLAR_RADIATION`, `UV_INDEX`.

### `get_forecast(device_id)` → `dict`

6-day WMO daily forecast for the station's location.

### `get_nearby_stations(lat, lon, distance_km=5)` → `dict`

Stations within a radius of a coordinate. ⚠️ Sensor values inside each result are
**×10 integers** — divide by 10 (e.g. `temp: 281` → 28.1 °C).

### Other raw methods

```python
client.get_device_values(device_id)    # same data as get_current_conditions, raw
client.get_device_info(device_id)       # metadata + current values as strings
client.get_wind_rose(device_id)         # wind direction distribution
client.get_update_status(device_id)     # seconds since last update
client.get_owner_profile(device_id)     # observer name, hardware brand/model
client.get_station_name(device_id)      # scrape the station name only
```

## 🧯 Error handling

Every method raises `WeathercloudError` on failure — network error, HTTP error,
non-JSON body, or an unexpected response shape. Catch the one type and you're
covered.

```python
from weathercloud import WeathercloudClient, WeathercloudError

try:
    cond = client.get_current_conditions(device_id)
except WeathercloudError as exc:
    ...  # set unavailable, log it, retry — your call
```

## 🔎 Finding a device ID

It's the number at the end of the station URL:

```
app.weathercloud.net/d5726468552  →  device_id = "5726468552"
```

METAR (airport) stations use ICAO codes (`EBBR`, `EGLL`, …) and work on most
`device/*` endpoints — just swap the prefix to `metar/*`.

## ⚡ Cloudflare Forge & Surface Tooling (CLI & MCP)

This project uses **[Cloudflare Forge](https://github.com/cloudflare/forge)** to power a schema-first code generation and surface tooling architecture. The canonical [`openapi.yaml`](./openapi.yaml) specification serves as the single source of truth for the entire API ecosystem.

Instead of handwriting boilerplate adapters, Cloudflare Forge automatically derives typed SDKs, CLI commands, and Model Context Protocol (MCP) tools directly from the OpenAPI schema and its extensions (`x-fern-*`, `x-forge-*`, `x-codeSamples`).

```
                  +--------------------------------+
                  |  openapi.yaml (Single Source)  |
                  +---------------+----------------+
                                  |
                   Cloudflare Forge Schema Engine
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
+---------------+         +---------------+         +---------------+
|  Python SDK   |         |  Auto-Gen CLI |         | Auto-Gen MCP  |
| (weathercloud)|         |  (Forge CLI)  |         | (AI Agents)   |
+---------------+         +---------------+         +---------------+
        |                         |                         |
        +-------------------------+-------------------------+
                                  |
                                  v
                  +--------------------------------+
                  | Scalar Interactive API Portal  |
                  | weathercloud-api.maurodruwel.be|
                  +--------------------------------+
```

### 📚 Interactive API Documentation (Scalar)

The complete interactive API reference is deployed to Cloudflare Pages at **[weathercloud-api.maurodruwel.be](https://weathercloud-api.maurodruwel.be)** (branch preview: [feat-forge-pipeline.weathercloud-api.pages.dev](https://feat-forge-pipeline.weathercloud-api.pages.dev)).

- **Powered by Scalar**: Clean, modern saturn-themed API explorer with instant search, dark mode, and zero-runtime dependency static build.
- **Native Python Library Snippets**: Every operation includes dedicated `x-codeSamples` demonstrating usage with the `weathercloud` Python client library alongside standard HTTP requests.

### 💻 Automated CLI Generation

Cloudflare Forge's CLI generator transforms OpenAPI operations into native command-line commands without any custom CLI scripting:

```bash
# Query live station sensor readings
weathercloud device values 5726468552

# Fetch station metadata, status, and coordinates
weathercloud device info 5726468552

# Query daily, monthly, and yearly min/max statistics
weathercloud device stats --code 5726468552

# Fetch time-series historical evolution data
weathercloud device evolution --device 5726468552 --variable 101 --period week

# Search for nearby stations by GPS coordinates
weathercloud stations nearby --lat 50.8503 --lon 4.3517 --distance 10

# Fetch 6-day weather forecast
weathercloud forecast daily --id 5726468552
```

Every command, flag, help description, and argument validator is automatically synchronized with `openapi.yaml`.

### 🤖 Model Context Protocol (MCP) for AI Agents

Cloudflare Forge automatically compiles the OpenAPI specification into **Model Context Protocol (MCP)** tool definitions, enabling AI assistants (such as Claude Desktop, Cursor, and Antigravity) to query live weather stations and analyze sensor readings directly:

- **Zero Handwritten Glue Code**: Operations (`getDeviceValues`, `getDeviceInfo`, `getDeviceStats`, `getForecast`, `getNearbyStations`) map directly to MCP tools with typed JSON schemas.
- **Autonomous Station Discovery**: AI agents can discover nearby stations, inspect historical trends, and monitor real-time sensor updates autonomously.

#### Connecting to Claude Desktop / Cursor

Add the Weathercloud MCP server definition to your `claude_desktop_config.json` or Cursor MCP settings:

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

Once connected, your AI assistant can directly answer queries such as:
- *"What is the current temperature and wind speed at Weathercloud station 5726468552?"*
- *"Find all Weathercloud stations within 10 km of Brussels and compare their barometric pressures."*

## 💡 Notes

- 🔓 No authentication required for public endpoints (recommended). Supply credentials only if you need to fetch private inside sensors of a station you own.
- ⏱️ Poll at most every 10 minutes — that's how often free stations update.
- 🧭 Single source of truth: [`openapi.yaml`](./openapi.yaml).
- ⚡ Cloudflare Forge pipeline: [`.github/workflows/forge.yml`](./.github/workflows/forge.yml).

## 🛠️ Development

```sh
git clone https://github.com/MauroDruwel/Weathercloud
cd Weathercloud
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

ruff check .      # lint
mypy              # type-check
pytest            # tests
python -m build   # build sdist + wheel
```

CI runs the linter, type checker, and the test matrix (Python 3.10–3.13) on every push and pull request.

## 📄 License

[MIT](LICENSE)

