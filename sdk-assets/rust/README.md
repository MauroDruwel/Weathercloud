# Weathercloud Rust SDK

[![crates.io](https://img.shields.io/crates/v/weathercloud.svg)](https://crates.io/crates/weathercloud)
[![docs.rs](https://docs.rs/weathercloud/badge.svg)](https://docs.rs/weathercloud)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Fern](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com)

Asynchronous, strongly-typed Rust SDK for [Weathercloud](https://weathercloud.net) — query real-time weather station sensor readings, METAR airport observations, sensor statistics, and historical trends without requiring authentication or CSRF tokens.

Powered by `tokio`, `reqwest`, and `serde`.

---

## Table of Contents

- [Installation](#installation)
- [Quickstart](#quickstart)
- [Live Weather Station Readings](#live-weather-station-readings)
- [Sensor Variables Reference](#sensor-variables-reference)
- [Station Profile & Metadata](#station-profile--metadata)
- [Map & Station Discovery](#map--station-discovery)
- [METAR Airport Observations](#metar-airport-observations)
- [Error Handling](#error-handling)
- [Full Reference](#full-reference)

---

## Installation

Add `weathercloud` and `tokio` to your `Cargo.toml`:

```toml
[dependencies]
weathercloud = "1.0.0"
tokio = { version = "1", features = ["full"] }
```

Or using `cargo add`:

```bash
cargo add weathercloud
cargo add tokio --features full
```

---

## Quickstart

Get current weather readings for any public Weathercloud station using its device ID (e.g., `5726468552`):

```rust
use weathercloud::prelude::*;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = WeathercloudClient::default();

    // Query live sensor readings — no login or CSRF tokens required
    let weather = client.device_live.get_values("5726468552", None).await?;

    println!("Timestamp:   {:?}", weather.epoch);
    println!("Temperature: {:?} °C", weather.temp);
    println!("Humidity:    {:?} %", weather.hum);
    println!("Pressure:    {:?} hPa", weather.bar);
    println!("Wind Speed:  {:?} m/s (Gusts: {:?} m/s)", weather.wspd, weather.wspdhi);
    println!("Wind Dir:    {:?}°", weather.wdir);
    println!("Daily Rain:  {:?} mm", weather.rain);

    Ok(())
}
```

---

## Live Weather Station Readings

### All Sensor Values

`client.device_live.get_values(...)` returns strongly-typed sensor readings:

```rust
use weathercloud::prelude::*;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = WeathercloudClient::default();
    let values = client.device_live.get_values("5726468552", None).await?;

    // Temperature & Humidity
    println!("Temp: {:?}°C | Dew Point: {:?}°C | Heat: {:?}°C | Chill: {:?}°C", 
        values.temp, values.dew, values.heat, values.chill);
    println!("Humidity: {:?}%", values.hum);

    // Wind
    println!("Wind Speed: {:?} m/s (Avg: {:?} m/s, Max: {:?} m/s)", 
        values.wspd, values.wspdavg, values.wspdhi);
    println!("Direction:  {:?}° (Avg: {:?}°)", values.wdir, values.wdiravg);

    // Barometer & Rain
    println!("Barometer:  {:?} hPa", values.bar);
    println!("Rain Today: {:?} mm (Rate: {:?} mm/h)", values.rain, values.rainrate);

    // Solar & UV (if supported by station hardware)
    if let Some(uvi) = values.uvi {
        println!("UV Index: {}", uvi);
    }
    if let Some(solarrad) = values.solarrad {
        println!("Solar Radiation: {} W/m²", solarrad);
    }

    Ok(())
}
```

---

## Sensor Variables Reference

Weathercloud reports abbreviated keys across its API. The SDK exposes these as clean Rust struct fields:

| Field | Type | Description | Unit / Format |
|---|---|---|---|
| `epoch` | `Option<i64>` | Timestamp of last sensor transmission | Unix epoch (seconds) |
| `temp` | `Option<f64>` | Air temperature | °C |
| `dew` | `Option<f64>` | Dew point | °C |
| `chill` | `Option<f64>` | Wind chill | °C |
| `heat` | `Option<f64>` | Heat index | °C |
| `hum` | `Option<i64>` | Relative humidity | % (0–100) |
| `bar` | `Option<f64>` | Atmospheric / barometric pressure | hPa |
| `wdir` | `Option<i64>` | Instantaneous wind direction | Degrees (0–360°) |
| `wdiravg` | `Option<i64>` | Average wind direction | Degrees (0–360°) |
| `wspd` | `Option<f64>` | Instantaneous wind speed | m/s |
| `wspdavg` | `Option<f64>` | Average wind speed | m/s |
| `wspdhi` | `Option<f64>` | Peak wind gust of the day | m/s |
| `rain` | `Option<f64>` | Accumulated daily precipitation | mm |
| `rainrate` | `Option<f64>` | Current precipitation rate | mm/h |
| `uvi` | `Option<f64>` | UV index | Index (0–16) |
| `solarrad` | `Option<f64>` | Solar radiation | W/m² |

---

## Station Profile & Metadata

Retrieve station model, manufacturer, coordinates, and observer details:

```rust
use weathercloud::prelude::*;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = WeathercloudClient::default();

    // Station metadata
    let info = client.device_live.get_info("5726468552", None).await?;
    if let Some(dev) = info.device {
        println!("Station Name: {:?}", dev.name);
        println!("Model:        {:?}", dev.model);
        println!("Coordinates:  {:?}, {:?}", dev.latitude, dev.longitude);
    }

    // Global network statistics
    let stats = client.device_live.get_stats(None).await?;
    println!("Active Devices:     {:?}", stats.devices_active);
    println!("Total Measurements: {:?}", stats.measurements_total);

    Ok(())
}
```

---

## Map & Station Discovery

Discover active weather stations within a geographic area or near coordinates:

```rust
use weathercloud::prelude::*;
use weathercloud::api::types::GetDevicesMapRequest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = WeathercloudClient::default();

    let devices = client.map.get_devices(&GetDevicesMapRequest {
        min_lat: Some(40.7000),
        max_lat: Some(40.8500),
        min_lon: Some(-74.0500),
        max_lon: Some(-73.9000),
        ..Default::default()
    }, None).await?;

    for dev in devices {
        println!("ID: {:?} | Name: {:?}", dev.id, dev.name);
    }

    Ok(())
}
```

---

## METAR Airport Observations

Query aviation weather reports from global airport METAR stations:

```rust
use weathercloud::prelude::*;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = WeathercloudClient::default();

    let metar = client.metar.get_values("EHAM", None).await?;
    println!("Airport METAR: {:?}", metar);

    Ok(())
}
```

---

## Error Handling

All failed API requests return `weathercloud::ApiError`:

```rust
use weathercloud::prelude::*;

#[tokio::main]
async fn main() {
    let client = WeathercloudClient::default();

    match client.device_live.get_values("nonexistent-id", None).await {
        Ok(weather) => println!("Temp: {:?}", weather.temp),
        Err(err) => eprintln!("API Error: {:?}", err),
    }
}
```

---

## Full Reference

For comprehensive API definitions, request parameters, and response schemas, see [reference.md](./reference.md).
