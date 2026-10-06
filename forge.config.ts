/**
 * Cloudflare Forge Configuration for Weathercloud
 * Generates client SDKs and documentation directly from docs/openapi.yaml.
 */

export default {
  // Source OpenAPI 3.0.3 specification
  spec: "./docs/openapi.yaml",

  // Generation output targets
  targets: [
    {
      type: "sdk",
      language: "python",
      outDir: "./src/weathercloud",
      options: {
        packageName: "weathercloud",
      },
    },
    {
      type: "sdk",
      language: "typescript",
      outDir: "./packages/weathercloud-ts",
      options: {
        packageName: "@maurodruwel/weathercloud",
      },
    },
    {
      type: "sdk",
      language: "rust",
      outDir: "./crates/weathercloud-rs",
      options: {
        crateName: "weathercloud",
      },
    },
    {
      type: "mcp",
      outDir: "./packages/weathercloud-mcp",
      options: {
        serverName: "weathercloud-mcp",
      },
    },
  ],
};
