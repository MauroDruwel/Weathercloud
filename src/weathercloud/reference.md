# Reference
## Auth
<details><summary><code>client.auth.<a href="src/weathercloud/auth/client.py">login</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Authenticates a user session to allow viewing private indoor sensors (`tempin`, `humin`, `heatin`) for the user's station.
This endpoint expects form urlencoded data and returns a `302 Found` redirect on successful login.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.auth.login(
    login_form_entity="LoginForm[entity]",
    login_form_password="LoginForm[password]",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**login_form_entity:** `str` — Username or email address
    
</dd>
</dl>

<dl>
<dd>

**login_form_password:** `str` — Account password
    
</dd>
</dl>

<dl>
<dd>

**login_form_remember_me:** `typing.Optional[LoginAuthRequestLoginFormRememberMe]` — Keep the user logged in
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## DeviceLive
<details><summary><code>client.device_live.<a href="src/weathercloud/device_live/client.py">get_values</a>(...) -> DeviceValues</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the latest sensor values for a device. **No CSRF token needed.**
This is the primary endpoint for a Home Assistant sensor integration.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_live.get_values(
    device_id="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**device_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.device_live.<a href="src/weathercloud/device_live/client.py">get_stats</a>(...) -> DeviceStats</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns current values plus day/month/year min and max for all sensors.
Each value is a `[unix_timestamp, value]` tuple.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_live.get_stats(
    code="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**code:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.device_live.<a href="src/weathercloud/device_live/client.py">get_info</a>(...) -> DeviceInfo</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Station name, location, elevation, equipment info.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_live.get_info(
    device_id="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**device_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.device_live.<a href="src/weathercloud/device_live/client.py">get_wind_rose</a>(...) -> WindData</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Wind direction distribution data for the wind rose chart.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_live.get_wind_rose(
    code="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**code:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.device_live.<a href="src/weathercloud/device_live/client.py">get_update_status</a>(...) -> GetUpdateStatusDeviceLiveResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns seconds since last update and device online status.

> ⚠️ **Requires `X-Requested-With: XMLHttpRequest`** header — without it the server returns an empty 200.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_live.get_update_status(
    d="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**d:** `str` — Device ID
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.device_live.<a href="src/weathercloud/device_live/client.py">get_owner_profile</a>(...) -> DeviceProfile</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns observer name, follower count, and device brand/model.

> ⚠️ **Requires `X-Requested-With: XMLHttpRequest`** header — without it the server returns an empty 200.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_live.get_owner_profile(
    d="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**d:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## DeviceHistory
<details><summary><code>client.device_history.<a href="src/weathercloud/device_history/client.py">get_evolution</a>(...) -> EvolutionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns hourly aggregated history for a given variable and period.

> ⚠️ **Requires `X-Requested-With: XMLHttpRequest`** header — without it the server returns an empty 200.

**Variable codes:**
| Code | Sensor |
|------|--------|
| 101  | Temperature (°C) |
| 201  | Humidity (%) |
| 541  | Dew point (°C) |
| 641  | Barometric pressure (hPa) |
| 701  | Wind speed (m/s) |
| 6001 | Wind direction (°) |
| 6501 | Wind gust / high speed (m/s) |
| 801  | Rain (mm) |
| 811  | Rain rate (mm/h) |
| 1001 | Solar radiation (W/m²) |
| 1101 | UV index |

**Period values:** `day`, `week`, `month`, `year`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.device_history.get_evolution(
    device="5726468552",
    variable=101,
    period="day",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**device:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**variable:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**period:** `GetEvolutionDeviceHistoryRequestPeriod` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Forecast
<details><summary><code>client.forecast.<a href="src/weathercloud/forecast/client.py">get_daily</a>(...) -> ForecastResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.forecast.get_daily(
    id="5726468552",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Map
<details><summary><code>client.map_.<a href="src/weathercloud/map_/client.py">get_devices</a>(...) -> MapDevicesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns stations visible on the map for a given location bounding box.

> ⚠️ **Requires `X-Requested-With: XMLHttpRequest`** header — without it the server returns an empty 200.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.map_.get_devices()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**user:** `typing.Optional[str]` — Filter by user (empty = all)
    
</dd>
</dl>

<dl>
<dd>

**location:** `typing.Optional[str]` — lat,lon,zoom format
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.map_.<a href="src/weathercloud/map_/client.py">get_background_devices</a>(...) -> MapDevicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.map_.get_background_devices()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**user:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.map_.<a href="src/weathercloud/map_/client.py">get_metars</a>(...) -> GetMetarsMapResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.map_.get_metars(
    request={
        "key": "value"
    },
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `typing.Dict[str, typing.Any]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Stations
<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_nearby</a>(...) -> PageDevicesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns nearby stations as JSON (despite `text/html` content-type header).
All `page/*` endpoints return `PageDevice` objects that include the **station name**.
Values are scaled integers — divide by 10 (e.g. `temp: 281` = 28.1°C).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_nearby(
    lat=1.1,
    lon=1.1,
    km=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**lat:** `float` 
    
</dd>
</dl>

<dl>
<dd>

**lon:** `float` 
    
</dd>
</dl>

<dl>
<dd>

**km:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_popular</a>(...) -> PageDevicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_popular(
    country="BE",
    period="day",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**period:** `GetPopularStationsRequestPeriod` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_newest</a>(...) -> PageDevicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_newest(
    country="BE",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_most_followed</a>(...) -> PageDevicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_most_followed(
    country="BE",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**country:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_last_views</a>() -> PageDevicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_last_views()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_own</a>() -> PageDevicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_own()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.stations.<a href="src/weathercloud/stations/client.py">get_station_page</a>(...) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The station **name** is not available from any JSON API endpoint.
The easiest way to get it is to fetch the station's HTML page and extract
the name from the `<title>` or `og:title` meta tag.

**Example response title:**
```
WeatherStation Skyline - Weathercloud | Global network of weather stations
```

Strip everything from ` - Weathercloud` onward to get the clean station name.

> This is a plain HTML page, not a JSON API. Use it for scraping only.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.stations.get_station_page(
    device_id="deviceId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**device_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Metar
<details><summary><code>client.metar.<a href="src/weathercloud/metar/client.py">get_values</a>(...) -> DeviceValues</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Most `device/*` routes work identically for METAR (airport) stations by replacing the `device` prefix with `metar`.

METAR station IDs are **ICAO codes** (4 letters), e.g. `EBBR` for Brussels Airport.

**Supported `metar/*` routes (same request/response as their `device/*` counterparts):**
- `GET /metar/values/{icao}` — current readings
- `GET /metar/stats?code={icao}` — statistics
- `GET /metar/wind?code={icao}` — wind rose
- `GET /metar/info/{icao}` — station metadata
- `POST /metar/ajaxupdatedate` — last update time
- `POST /metar/ajaxprofile` — station profile
- `POST /metar/evolution` — time-series history

> **Not supported for METAR:** `/device/ajaxdevicestats`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from weathercloud import WeathercloudClient
from weathercloud.environment import WeathercloudClientEnvironment

client = WeathercloudClient(
    environment=WeathercloudClientEnvironment.DEFAULT,
)

client.metar.get_values(
    device_id="EBBR",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**device_id:** `str` — ICAO airport code
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

