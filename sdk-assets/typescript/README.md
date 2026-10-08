# Weathercloud TypeScript / JavaScript Library

[![npm version](https://img.shields.io/npm/v/weathercloud.svg?color=blue)](https://www.npmjs.com/package/weathercloud)
[![npm downloads](https://img.shields.io/npm/dm/weathercloud.svg)](https://www.npmjs.com/package/weathercloud)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Fern](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com)

Typed, modern TypeScript / Node.js client library for [Weathercloud](https://weathercloud.net) — query real-time weather station sensor readings, METAR airport observations, sensor statistics, and historical trends without requiring authentication or CSRF tokens.

Works in Node.js 18+, Bun, Deno, and modern browser / edge environments.

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

```bash
npm install weathercloud
```

Or using [pnpm](https://pnpm.io) or [yarn](https://yarnpkg.com):

```bash
pnpm add weathercloud
# or
yarn add weathercloud
# or
bun add weathercloud
```

---

## Quickstart

Get current weather readings for any public Weathercloud station using its device ID (e.g., `5726468552`):

```typescript
import { WeathercloudClient } from "weathercloud";

const client = new WeathercloudClient();

// Query live sensor readings — no login or CSRF tokens required
const weather = await client.deviceLive.getValues({
  deviceId: "5726468552",
});

console.log(`Timestamp:   ${weather.epoch}`);
console.log(`Temperature: ${weather.temp} °C`);
console.log(`Humidity:    ${weather.hum} %`);
console.log(`Pressure:    ${weather.bar} hPa`);
console.log(`Wind Speed:  ${weather.wspd} m/s (Gusts: ${weather.wspdhi} m/s)`);
console.log(`Wind Dir:    ${weather.wdir}°`);
console.log(`Daily Rain:  ${weather.rain} mm`);
```

---

## Live Weather Station Readings

### All Sensor Values

`client.deviceLive.getValues(...)` returns strongly-typed sensor readings:

```typescript
import { WeathercloudClient } from "weathercloud";

const client = new WeathercloudClient();

const values = await client.deviceLive.getValues({
  deviceId: "5726468552",
});

// Temperature & Humidity
console.log(`Temp: ${values.temp}°C | Dew Point: ${values.dew}°C | Heat Index: ${values.heat}°C | Chill: ${values.chill}°C`);
console.log(`Humidity: ${values.hum}%`);

// Wind
console.log(`Wind Speed: ${values.wspd} m/s (Avg: ${values.wspdavg} m/s, Max: ${values.wspdhi} m/s)`);
console.log(`Direction:  ${values.wdir}° (Avg: ${values.wdiravg}°)`);

// Barometer & Rain
console.log(`Barometer:  ${values.bar} hPa`);
console.log(`Rain Today: ${values.rain} mm (Rate: ${values.rainrate} mm/h)`);

// Solar & UV (if supported by station hardware)
if (values.uvi !== undefined) {
  console.log(`UV Index: ${values.uvi}`);
}
if (values.solarrad !== undefined) {
  console.log(`Solar Radiation: ${values.solarrad} W/m²`);
}
```

---

## Sensor Variables Reference

Weathercloud reports abbreviated keys across its API. The SDK exposes these as clean, camelCase typed properties:

| Property | Type | Description | Unit / Format |
|---|---|---|---|
| `epoch` | `number` | Timestamp of last sensor transmission | Unix epoch (seconds) |
| `temp` | `number` | Air temperature | °C |
| `dew` | `number` | Dew point | °C |
| `chill` | `number` | Wind chill | °C |
| `heat` | `number` | Heat index | °C |
| `hum` | `number` | Relative humidity | % (0–100) |
| `bar` | `number` | Atmospheric / barometric pressure | hPa |
| `wdir` | `number` | Instantaneous wind direction | Degrees (0–360°) |
| `wdiravg` | `number` | Average wind direction | Degrees (0–360°) |
| `wspd` | `number` | Instantaneous wind speed | m/s |
| `wspdavg` | `number` | Average wind speed | m/s |
| `wspdhi` | `number` | Peak wind gust of the day | m/s |
| `rain` | `number` | Accumulated daily precipitation | mm |
| `rainrate` | `number` | Current precipitation rate | mm/h |
| `uvi` | `number` | UV index | Index (0–16) |
| `solarrad` | `number` | Solar radiation | W/m² |

---

## Station Profile & Metadata

Retrieve station model, manufacturer, coordinates, and observer details:

```typescript
import { WeathercloudClient } from "weathercloud";

const client = new WeathercloudClient();

// Station metadata
const info = await client.deviceLive.getInfo({
  deviceId: "5726468552",
});

if (info.device) {
  console.log(`Station Name: ${info.device.name}`);
  console.log(`Model:        ${info.device.model}`);
  console.log(`Coordinates:  ${info.device.latitude}, ${info.device.longitude}`);
}

// Global network statistics
const stats = await client.deviceLive.getStats();
console.log(`Active Devices:     ${stats.devicesActive}`);
console.log(`Total Measurements: ${stats.measurementsTotal}`);
```

---

## Map & Station Discovery

Discover active weather stations within a geographic area or near coordinates:

```typescript
import { WeathercloudClient } from "weathercloud";

const client = new WeathercloudClient();

// Search stations in a latitude/longitude bounding box
const devices = await client.map.getDevices({
  minLat: 40.7000,
  maxLat: 40.8500,
  minLon: -74.0500,
  maxLon: -73.9000,
});

for (const dev of devices) {
  console.log(`ID: ${dev.id} | Name: ${dev.name} | Lat: ${dev.latitude}, Lon: ${dev.longitude}`);
}
```

---

## METAR Airport Observations

Query aviation weather reports from global airport METAR stations:

```typescript
import { WeathercloudClient } from "weathercloud";

const client = new WeathercloudClient();

// Fetch airport METAR report by ICAO identifier (e.g., EHAM)
const metar = await client.metar.getValues({
  deviceId: "EHAM",
});

console.log(`Airport METAR:`, metar);
```

---

## Error Handling

All failed HTTP requests throw typed `WeathercloudError`:

```typescript
import { WeathercloudClient, WeathercloudError } from "weathercloud";

const client = new WeathercloudClient();

try {
  const weather = await client.deviceLive.getValues({
    deviceId: "nonexistent-id",
  });
} catch (err) {
  if (err instanceof WeathercloudError) {
    console.error(`Status: ${err.statusCode}`);
    console.error(`Message: ${err.message}`);
  }
}
```

---

## Custom Configuration & Environments

```typescript
import { WeathercloudClient, WeathercloudEnvironment } from "weathercloud";

const client = new WeathercloudClient({
  environment: WeathercloudEnvironment.Default,
  maxRetries: 3,
  timeoutInSeconds: 15,
});
```

---

## Full Reference

For comprehensive API definitions, request parameters, and response schemas, see [reference.md](./reference.md).
