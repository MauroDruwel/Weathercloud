# Weathercloud Go SDK

[![pkg.go.dev](https://pkg.go.dev/badge/github.com/MauroDruwel/weathercloud-go.svg)](https://pkg.go.dev/github.com/MauroDruwel/weathercloud-go)
[![Go Report Card](https://goreportcard.com/badge/github.com/MauroDruwel/weathercloud-go)](https://goreportcard.com/report/github.com/MauroDruwel/weathercloud-go)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Fern](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com)

Idiomatic, strongly-typed Go client library for [Weathercloud](https://weathercloud.net) — query real-time weather station sensor readings, METAR airport observations, sensor statistics, and historical trends without requiring authentication or CSRF tokens.

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

```bash
go get github.com/MauroDruwel/weathercloud-go
```

---

## Quickstart

Get current weather readings for any public Weathercloud station using its device ID (e.g., `5726468552`):

```go
package main

import (
	"context"
	"fmt"
	"log"

	weathercloud "github.com/MauroDruwel/weathercloud-go"
	client "github.com/MauroDruwel/weathercloud-go/client"
)

func main() {
	c := client.NewWeathercloudClient()

	// Query live sensor readings — no login or CSRF tokens required
	weather, err := c.DeviceLive.GetValues(context.Background(), &weathercloud.GetValuesDeviceLiveRequest{
		DeviceId: "5726468552",
	})
	if err != nil {
		log.Fatalf("Failed to fetch readings: %v", err)
	}

	fmt.Printf("Timestamp:   %v\n", *weather.Epoch)
	fmt.Printf("Temperature: %v °C\n", *weather.Temp)
	fmt.Printf("Humidity:    %v %%\n", *weather.Hum)
	fmt.Printf("Pressure:    %v hPa\n", *weather.Bar)
	fmt.Printf("Wind Speed:  %v m/s (Gusts: %v m/s)\n", *weather.Wspd, *weather.Wspdhi)
	fmt.Printf("Wind Dir:    %v°\n", *weather.Wdir)
	fmt.Printf("Daily Rain:  %v mm\n", *weather.Rain)
}
```

---

## Live Weather Station Readings

### All Sensor Values

`c.DeviceLive.GetValues(...)` returns strongly-typed sensor readings:

```go
package main

import (
	"context"
	"fmt"
	"log"

	weathercloud "github.com/MauroDruwel/weathercloud-go"
	client "github.com/MauroDruwel/weathercloud-go/client"
)

func main() {
	c := client.NewWeathercloudClient()

	values, err := c.DeviceLive.GetValues(context.Background(), &weathercloud.GetValuesDeviceLiveRequest{
		DeviceId: "5726468552",
	})
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	// Temperature & Humidity
	if values.Temp != nil {
		fmt.Printf("Temp: %v°C | Dew Point: %v°C\n", *values.Temp, *values.Dew)
	}
	if values.Hum != nil {
		fmt.Printf("Humidity: %v%%\n", *values.Hum)
	}

	// Wind
	if values.Wspd != nil {
		fmt.Printf("Wind Speed: %v m/s (Avg: %v m/s, Max: %v m/s)\n", *values.Wspd, *values.Wspdavg, *values.Wspdhi)
	}

	// Barometer & Rain
	if values.Bar != nil {
		fmt.Printf("Barometer: %v hPa\n", *values.Bar)
	}
	if values.Rain != nil {
		fmt.Printf("Rain Today: %v mm\n", *values.Rain)
	}
}
```

---

## Sensor Variables Reference

Weathercloud reports abbreviated keys across its API. The SDK exposes these as clean, PascalCase pointer fields:

| Field | Type | Description | Unit / Format |
|---|---|---|---|
| `Epoch` | `*int` | Timestamp of last sensor transmission | Unix epoch (seconds) |
| `Temp` | `*float64` | Air temperature | °C |
| `Dew` | `*float64` | Dew point | °C |
| `Chill` | `*float64` | Wind chill | °C |
| `Heat` | `*float64` | Heat index | °C |
| `Hum` | `*int` | Relative humidity | % (0–100) |
| `Bar` | `*float64` | Atmospheric / barometric pressure | hPa |
| `Wdir` | `*int` | Instantaneous wind direction | Degrees (0–360°) |
| `Wdiravg` | `*int` | Average wind direction | Degrees (0–360°) |
| `Wspd` | `*float64` | Instantaneous wind speed | m/s |
| `Wspdavg` | `*float64` | Average wind speed | m/s |
| `Wspdhi` | `*float64` | Peak wind gust of the day | m/s |
| `Rain` | `*float64` | Accumulated daily precipitation | mm |
| `Rainrate` | `*float64` | Current precipitation rate | mm/h |
| `Uvi` | `*float64` | UV index | Index (0–16) |
| `Solarrad` | `*float64` | Solar radiation | W/m² |

---

## Station Profile & Metadata

Retrieve station model, manufacturer, coordinates, and observer details:

```go
info, err := c.DeviceLive.GetInfo(context.Background(), &weathercloud.GetInfoDeviceLiveRequest{
    DeviceId: "5726468552",
})
if err == nil && info.Device != nil {
    fmt.Printf("Station Name: %v\n", *info.Device.Name)
    fmt.Printf("Model:        %v\n", *info.Device.Model)
}

stats, err := c.DeviceLive.GetStats(context.Background())
if err == nil {
    fmt.Printf("Active Devices: %v\n", *stats.DevicesActive)
}
```

---

## Map & Station Discovery

Discover active weather stations within a geographic area or near coordinates:

```go
devices, err := c.Map.GetDevices(context.Background(), &weathercloud.GetDevicesMapRequest{
    MinLat: float64Ptr(40.7000),
    MaxLat: float64Ptr(40.8500),
    MinLon: float64Ptr(-74.0500),
    MaxLon: float64Ptr(-73.9000),
})
if err == nil {
    for _, dev := range devices {
        fmt.Printf("ID: %v | Name: %v\n", dev.Id, dev.Name)
    }
}
```

---

## METAR Airport Observations

Query aviation weather reports from global airport METAR stations:

```go
metar, err := c.Metar.GetValues(context.Background(), &weathercloud.GetValuesMetarRequest{
    DeviceId: "EHAM",
})
if err == nil {
    fmt.Printf("Airport METAR: %+v\n", metar)
}
```

---

## Error Handling

```go
weather, err := c.DeviceLive.GetValues(context.Background(), &weathercloud.GetValuesDeviceLiveRequest{
    DeviceId: "nonexistent-id",
})
if err != nil {
    log.Printf("API error: %v", err)
}
```

---

## Full Reference

For comprehensive API definitions, request parameters, and response schemas, see [reference.md](./reference.md).
