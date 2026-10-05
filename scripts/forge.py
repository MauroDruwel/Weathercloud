#!/usr/bin/env python3
"""Cloudflare Forge generation pipeline and developer surface tooling for Weathercloud.

Usage:
    python scripts/forge.py lint                         # Validate OpenAPI spec and Fern configuration
    python scripts/forge.py generate [--target TARGET]   # Generate SDKs (python, csharp, typescript, go, all)
    python scripts/forge.py docs                         # Build interactive Cloudflare-themed docs
    python scripts/forge.py test                         # Run test suite across SDK clients
    python scripts/forge.py build                        # Build distribution packages (wheel, sdist)
    python scripts/forge.py all                          # Execute the entire Forge pipeline end-to-end
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENAPI_SPEC = REPO_ROOT / "openapi.yaml"
FERN_DIR = REPO_ROOT / "fern"
DOCS_DIR = REPO_ROOT / "docs"
SRC_DIR = REPO_ROOT / "src" / "weathercloud"


def log(msg: str) -> None:
    print(f"\033[1;38;5;208m==> Forge:\033[0m \033[1m{msg}\033[0m")


def run(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> int:
    display_cmd = " ".join(cmd)
    print(f"\033[90m$ {display_cmd}\033[0m")
    result = subprocess.run(cmd, cwd=cwd or REPO_ROOT, env=env)
    if check and result.returncode != 0:
        print(f"\033[31mCommand failed with exit code {result.returncode}\033[0m", file=sys.stderr)
        sys.exit(result.returncode)
    return result.returncode


def get_python_exe() -> str:
    venv_py = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_py.exists():
        return str(venv_py)
    return sys.executable


def cmd_lint() -> None:
    log("Validating OpenAPI specification with Redocly CLI...")
    run([
        "npx",
        "--yes",
        "@redocly/cli",
        "lint",
        str(OPENAPI_SPEC),
        "--skip-rule",
        "operation-4xx-response",
    ])
    log("✓ openapi.yaml conforms to Forge schema requirements")

    log("Validating Fern workspace and SDK generators...")
    run(["npx", "--yes", "fern-api", "check"])
    log("✓ Fern configuration passed verification")


def cmd_generate(target: str = "python") -> None:
    targets = ["python", "csharp", "typescript", "go"] if target == "all" else [target]

    if "python" in targets:
        log("Generating typed Python SDK via Fern (fernapi/fern-python-sdk)...")
        run(["npx", "--yes", "fern-api", "generate", "--group", "python-sdk", "--local", "--force"])

        # Verify generated output
        client_file = SRC_DIR / "client.py"
        if not client_file.exists():
            print(f"\033[31mError: Expected {client_file} to exist after generation.\033[0m", file=sys.stderr)
            sys.exit(1)

        py = get_python_exe()
        env = dict(os.environ, PYTHONPATH=str(REPO_ROOT / "src"))
        run([py, "-c", "import weathercloud; print('✓ Verified weathercloud v' + weathercloud.__version__)"], env=env)
        log("✓ Fern Python SDK generated successfully in src/weathercloud")

    if "csharp" in targets:
        log("Generating typed C# (.NET) SDK via Fern (fernapi/fern-csharp-sdk)...")
        run(["npx", "--yes", "fern-api", "generate", "--group", "csharp-sdk", "--local"])
        log("✓ Fern C# (.NET) SDK generated successfully in sdks/csharp")

    if "typescript" in targets:
        log("Generating typed TypeScript SDK via Fern (fernapi/fern-typescript-sdk)...")
        run(["npx", "--yes", "fern-api", "generate", "--group", "typescript-sdk", "--local"])
        log("✓ Fern TypeScript SDK generated successfully in sdks/typescript")

    if "go" in targets:
        log("Generating typed Go SDK via Fern (fernapi/fern-go-sdk)...")
        run(["npx", "--yes", "fern-api", "generate", "--group", "go-sdk", "--local"])
        log("✓ Fern Go SDK generated successfully in sdks/go")


def cmd_docs() -> None:
    log("Bundling OpenAPI specification and generating interactive documentation...")
    bundle_path = REPO_ROOT / "docs" / "openapi.json"
    run([
        "npx",
        "--yes",
        "@redocly/cli",
        "bundle",
        str(OPENAPI_SPEC),
        "-o",
        str(bundle_path),
        "--ext",
        "json",
    ])

    spec_json = bundle_path.read_text(encoding="utf-8")
    html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Weathercloud API Reference — Cloudflare Forge</title>
    <link rel="icon" type="image/svg+xml" href="https://app.weathercloud.net/favicon.ico" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
    <style>
      :root {{
        --scalar-font: 'Inter', system-ui, -apple-system, sans-serif;
        --scalar-font-code: 'JetBrains Mono', ui-monospace, monospace;
        --scalar-color-1: #f6821f;
        --scalar-color-accent: #f6821f;
        --scalar-background-1: #0f172a;
        --scalar-background-2: #1e293b;
      }}
    </style>
  </head>
  <body>
    <script
      id="api-reference"
      type="application/json"
      data-configuration='{{"theme":"saturn","darkMode":true,"layout":"modern","showSidebar":true,"searchHotKey":"k","defaultHttpClient":{{"targetKey":"python","clientKey":"requests"}}}}'>
{spec_json}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
  </body>
</html>"""

    index_html = DOCS_DIR / "index.html"
    index_html.write_text(html_content, encoding="utf-8")
    log(f"✓ Generated interactive Scalar API documentation in {index_html}")


def cmd_test() -> None:
    log("Running pytest test suite across sync and async SDK clients...")
    py = get_python_exe()
    pytest_bin = REPO_ROOT / ".venv" / "bin" / "pytest"
    test_cmd = [str(pytest_bin) if pytest_bin.exists() else "pytest", "-v"]
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT / "src"))
    run(test_cmd, env=env)
    log("✓ All tests passed")


def cmd_build() -> None:
    log("Building distribution packages (wheel and sdist)...")
    if shutil.which("uv"):
        run(["uv", "build"])
    else:
        py = get_python_exe()
        run([py, "-m", "build"])
    log("✓ Distribution package built successfully in dist/")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cloudflare Forge Generation Pipeline for Weathercloud",
    )
    parser.add_argument(
        "step",
        choices=["lint", "generate", "docs", "test", "build", "all"],
        default="all",
        nargs="?",
        help="Pipeline step to execute (default: all)",
    )
    parser.add_argument(
        "--target",
        "-t",
        choices=["python", "csharp", "typescript", "go", "all"],
        default="python",
        help="Target SDK language to generate (default: python)",
    )
    args = parser.parse_args()

    if args.step == "lint":
        cmd_lint()
    elif args.step == "generate":
        cmd_generate(args.target)
    elif args.step == "docs":
        cmd_docs()
    elif args.step == "test":
        cmd_test()
    elif args.step == "build":
        cmd_build()
    elif args.step == "all":
        cmd_lint()
        cmd_generate(args.target)
        cmd_docs()
        cmd_test()
        cmd_build()
        log("🎉 Cloudflare Forge pipeline completed successfully!")


if __name__ == "__main__":
    main()
