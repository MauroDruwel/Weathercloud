# Weathercloud C# / .NET Library

[![NuGet version](https://img.shields.io/nuget/v/Weathercloud.svg?color=blue)](https://www.nuget.org/packages/Weathercloud/)
[![NuGet downloads](https://img.shields.io/nuget/dt/Weathercloud.svg)](https://www.nuget.org/packages/Weathercloud/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Fern](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com)

Typed, modern C# client library for [Weathercloud](https://weathercloud.net) — query real-time weather station sensor readings, METAR airport observations, sensor statistics, and historical trends without requiring authentication or CSRF tokens.

Compatible with **.NET 8+**, **.NET Framework 4.6.2+**, and **.NET Standard 2.0+**.

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
- [Custom Configuration & Environments](#custom-configuration--environments)
- [Full Reference](#full-reference)

---

## Installation

Add the package via the .NET CLI:

```bash
dotnet add package Weathercloud
```

Or via the NuGet Package Manager Console:

```powershell
Install-Package Weathercloud
```

Or add directly to your `.csproj`:

```xml
<PackageReference Include="Weathercloud" Version="1.0.0" />
```

---

## Quickstart

Get current weather readings for any public Weathercloud station using its device ID (e.g., `5726468552`):

```csharp
using System;
using Weathercloud;

var client = new WeathercloudClient();

// Query live sensor readings — no login or CSRF tokens required
var weather = await client.DeviceLive.GetValuesAsync(new GetValuesDeviceLiveRequest
{
    DeviceId = "5726468552"
});

Console.WriteLine($"Timestamp:   {weather.Epoch}");
Console.WriteLine($"Temperature: {weather.Temp} °C");
Console.WriteLine($"Humidity:    {weather.Hum} %");
Console.WriteLine($"Pressure:    {weather.Bar} hPa");
Console.WriteLine($"Wind Speed:  {weather.Wspd} m/s (Gusts: {weather.Wspdhi} m/s)");
Console.WriteLine($"Wind Dir:    {weather.Wdir}°");
Console.WriteLine($"Daily Rain:  {weather.Rain} mm");
```

---

## Live Weather Station Readings

### All Sensor Values

`client.DeviceLive.GetValuesAsync(...)` returns strongly-typed sensor readings:

```csharp
using System;
using Weathercloud;

var client = new WeathercloudClient();

var values = await client.DeviceLive.GetValuesAsync(new GetValuesDeviceLiveRequest
{
    DeviceId = "5726468552"
});

// Temperature & Humidity
Console.WriteLine($"Temp: {values.Temp}°C | Dew Point: {values.Dew}°C | Heat Index: {values.Heat}°C | Chill: {values.Chill}°C");
Console.WriteLine($"Humidity: {values.Hum}%");

// Wind
Console.WriteLine($"Wind Speed: {values.Wspd} m/s (Avg: {values.Wspdavg} m/s, Max: {values.Wspdhi} m/s)");
Console.WriteLine($"Direction:  {values.Wdir}° (Avg: {values.Wdiravg}°)");

// Barometer & Rain
Console.WriteLine($"Barometer:  {values.Bar} hPa");
Console.WriteLine($"Rain Today: {values.Rain} mm (Rate: {values.Rainrate} mm/h)");

// Solar & UV (if supported by station hardware)
if (values.Uvi.HasValue)
{
    Console.WriteLine($"UV Index: {values.Uvi.Value}");
}
if (values.Solarrad.HasValue)
{
    Console.WriteLine($"Solar Radiation: {values.Solarrad.Value} W/m²");
}
```

---

## Sensor Variables Reference

Weathercloud reports abbreviated keys across its API. The SDK exposes these as clean, PascalCase properties:

| Property | Type | Description | Unit / Format |
|---|---|---|---|
| `Epoch` | `int?` | Timestamp of last sensor transmission | Unix epoch (seconds) |
| `Temp` | `double?` | Air temperature | °C |
| `Dew` | `double?` | Dew point | °C |
| `Chill` | `double?` | Wind chill | °C |
| `Heat` | `double?` | Heat index | °C |
| `Hum` | `int?` | Relative humidity | % (0–100) |
| `Bar` | `double?` | Atmospheric / barometric pressure | hPa |
| `Wdir` | `int?` | Instantaneous wind direction | Degrees (0–360°) |
| `Wdiravg` | `int?` | Average wind direction | Degrees (0–360°) |
| `Wspd` | `double?` | Instantaneous wind speed | m/s |
| `Wspdavg` | `double?` | Average wind speed | m/s |
| `Wspdhi` | `double?` | Peak wind gust of the day | m/s |
| `Rain` | `double?` | Accumulated daily precipitation | mm |
| `Rainrate` | `double?` | Current precipitation rate | mm/h |
| `Uvi` | `double?` | UV index | Index (0–16) |
| `Solarrad` | `double?` | Solar radiation | W/m² |

---

## Station Profile & Metadata

Retrieve station model, manufacturer, coordinates, and observer details:

```csharp
using System;
using Weathercloud;

var client = new WeathercloudClient();

// Station metadata
var info = await client.DeviceLive.GetInfoAsync(new GetInfoDeviceLiveRequest
{
    DeviceId = "5726468552"
});

if (info.Device != null)
{
    Console.WriteLine($"Station Name: {info.Device.Name}");
    Console.WriteLine($"Model:        {info.Device.Model}");
    Console.WriteLine($"Coordinates:  {info.Device.Latitude}, {info.Device.Longitude}");
}

// Global network statistics
var stats = await client.DeviceLive.GetStatsAsync();
Console.WriteLine($"Active Devices:     {stats.DevicesActive}");
Console.WriteLine($"Total Measurements: {stats.MeasurementsTotal}");
```

---

## Map & Station Discovery

Discover active weather stations within a geographic area or near coordinates:

```csharp
using System;
using Weathercloud;

var client = new WeathercloudClient();

// Search stations in a latitude/longitude bounding box
var devices = await client.Map.GetDevicesAsync(new GetDevicesMapRequest
{
    MinLat = 40.7000,
    MaxLat = 40.8500,
    MinLon = -74.0500,
    MaxLon = -73.9000,
});

foreach (var dev in devices)
{
    Console.WriteLine($"ID: {dev.Id} | Name: {dev.Name} | Lat: {dev.Latitude}, Lon: {dev.Longitude}");
}
```

---

## METAR Airport Observations

Query aviation weather reports from global airport METAR stations:

```csharp
using System;
using Weathercloud;

var client = new WeathercloudClient();

// Fetch airport METAR report by ICAO identifier (e.g., EHAM)
var metar = await client.Metar.GetValuesAsync(new GetValuesMetarRequest
{
    DeviceId = "EHAM"
});

Console.WriteLine($"Airport METAR: {metar}");
```

---

## Error Handling

All failed HTTP requests throw typed `WeathercloudClientApiException`:

```csharp
using System;
using Weathercloud;
using Weathercloud.Core;

var client = new WeathercloudClient();

try
{
    var weather = await client.DeviceLive.GetValuesAsync(new GetValuesDeviceLiveRequest
    {
        DeviceId = "nonexistent-id"
    });
}
catch (WeathercloudClientApiException ex)
{
    Console.WriteLine($"Status Code: {ex.StatusCode}");
    Console.WriteLine($"Body:        {ex.Body}");
}
```

---

## Custom Configuration & Environments

```csharp
using Weathercloud;
using Weathercloud.Core;

var client = new WeathercloudClient(clientOptions: new ClientOptions
{
    BaseUrl = WeathercloudClientEnvironment.Default,
    MaxRetries = 3,
    Timeout = TimeSpan.FromSeconds(15)
});
```

---

## Full Reference

For comprehensive API definitions, request parameters, and response schemas, see [reference.md](./reference.md).
