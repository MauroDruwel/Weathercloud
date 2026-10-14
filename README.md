# Weathercloud API & Cloudflare Forge Pipeline

[![Cloudflare Forge](https://github.com/MauroDruwel/Weathercloud/actions/workflows/forge.yml/badge.svg)](https://github.com/MauroDruwel/Weathercloud/actions/workflows/forge.yml)
[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1-6BA539.svg)](./openapi.yaml)
[![API Docs](https://img.shields.io/badge/docs-Scalar%20Reference-F6821F.svg)](https://weathercloud-api.maurodruwel.be)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

The single source of truth OpenAPI specification and **Cloudflare Forge** generation pipeline for [Weathercloud](https://app.weathercloud.net).

Read live weather conditions, station metadata, historical records, airport METARs, and weather forecasts from public weather stations — **no API key required** for public station data.

> ⚠️ Reverse-engineered from the public web app. Not affiliated with or endorsed by Weathercloud; upstream endpoints may change without notice.

---

## 📚 Interactive API Documentation

Browse the full, interactive [Scalar API Reference](https://weathercloud-api.maurodruwel.be) hosted on Cloudflare Pages:
* **Interactive Testing**: Test requests directly from your browser.
* **Schema Inspector**: Explore strongly-typed request and response structures.
* **Code Snippets**: Instant samples for Python, JavaScript, cURL, Go, C#, and more.

---

## 📦 Official Client Libraries (SDKs)

Client libraries are generated automatically from [`openapi.yaml`](./openapi.yaml) using Fern and published to their respective language ecosystems:

| Language | Ecosystem / Registry | Repository | Install Command |
| :--- | :--- | :--- | :--- |
| **Python** | [PyPI](https://pypi.org/project/weathercloud/) | [`MauroDruwel/weathercloud-py`](https://github.com/MauroDruwel/weathercloud-py) | `pip install weathercloud` |
| **C# / .NET** | [NuGet](https://www.nuget.org/) | [`MauroDruwel/weathercloud-csharp`](https://github.com/MauroDruwel/weathercloud-csharp) | `dotnet add package WeathercloudApi` |
| **TypeScript / Node** | [npm](https://www.npmjs.com/) | [`MauroDruwel/weathercloud-ts`](https://github.com/MauroDruwel/weathercloud-ts) | `npm install @weathercloud/sdk` |
| **Go** | Go Modules | [`MauroDruwel/weathercloud-go`](https://github.com/MauroDruwel/weathercloud-go) | `go get github.com/MauroDruwel/weathercloud-go` |
| **Rust** | [crates.io](https://crates.io/) | [`MauroDruwel/weathercloud-rust`](https://github.com/MauroDruwel/weathercloud-rust) | `cargo add weathercloud_api` |

---

## 🤖 Model Context Protocol (MCP) for AI Agents

Serve real-time Weathercloud station sensors to Claude Desktop, Cursor, or Antigravity with zero code using Cloudflare's `@cloudflare/forge-mcp`:

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

## 🏗️ Architecture

```
                       MauroDruwel/Weathercloud
                     ┌───────────────────────────┐
                     │       openapi.yaml        │  <-- Single source of truth
                     │    (Cloudflare Forge)     │
                     └─────────────┬─────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
   Scalar Docs                MCP Server              Fern Multi-SDKs
 (Cloudflare Pages)     (@cloudflare/forge-mcp)              │
weathercloud-api.maurodruwel.be                              │
         ┌─────────────────────────┬─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼                         ▼
  weathercloud-py         weathercloud-csharp         weathercloud-ts         weathercloud-rust
    (PyPI / uv)                 (NuGet)                    (npm)                 (crates.io)
```

---

## 🛠️ Development & Pipeline

This repository is 100% stock Node.js tooling (`@redocly/cli` and `fern-api`). You can run targets using either `make` or `npm`:

```sh
# Install dev dependencies
npm install

# Validate OpenAPI spec & Fern configuration
make lint
# or: npm run lint

# Bundle OpenAPI for Scalar documentation (docs/openapi.json)
make docs
# or: npm run docs

# Generate SDKs locally into sdks/
make generate
# or: npm run generate

# Generate a specific language SDK:
make generate-python       # Generates sdks/python/
make generate-csharp       # Generates sdks/csharp/
make generate-typescript   # Generates sdks/typescript/
make generate-go           # Generates sdks/go/
```

---

## 📄 License

[MIT](LICENSE)
