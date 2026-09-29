#!/usr/bin/env python3
"""
Generates the official Fern / Cloudflare Docs UI from openapi.yaml.
Produces a self-contained, interactive 3-column documentation site in docs/index.html
matching the ElevenLabs & Cloudflare API reference style.
"""

import json
import re
import subprocess
import os

def load_spec():
    # Convert openapi.yaml to JSON using npx yaml or python if available
    try:
        raw_json = subprocess.check_output(
            ["npx", "--yes", "yaml", "--json"],
            stdin=open("openapi.yaml", "rb")
        )
        data = json.loads(raw_json)
        return data[0] if isinstance(data, list) else data
    except Exception as e:
        raise RuntimeError(f"Failed to parse openapi.yaml: {e}")

def get_code_samples(ep):
    path = ep['path']
    method = ep['method']
    params = ep.get('parameters', [])
    body = ep.get('requestBody', {})
    
    # Path params formatting
    url_path = path
    for p in params:
        if p.get('in') == 'path':
            ex = p.get('example', p.get('schema', {}).get('example', '5726468552'))
            url_path = url_path.replace(f"{{{p['name']}}}", str(ex))
            
    base_url = "https://app.weathercloud.net"
    full_url = f"{base_url}{url_path}"
    
    # cURL snippet
    curl_lines = [f"curl -X {method} '{full_url}' \\", "  -H 'X-Requested-With: XMLHttpRequest'"]
    if method == 'POST':
        curl_lines.append("  -H 'Content-Type: application/x-www-form-urlencoded' \\")
        curl_lines.append("  -d 'variable=101&period=week'")
    curl = " \\\n".join(curl_lines)

    # Python snippet
    py_lines = [
        "import requests",
        "",
        f"url = '{full_url}'",
        "headers = {'X-Requested-With': 'XMLHttpRequest'}"
    ]
    if method == 'POST':
        py_lines.append("data = {'variable': 101, 'period': 'week'}")
        py_lines.append("response = requests.post(url, headers=headers, data=data)")
    else:
        py_lines.append("response = requests.get(url, headers=headers)")
    py_lines.append("print(response.json())")
    python = "\n".join(py_lines)

    # TypeScript snippet
    ts_lines = [
        f"const response = await fetch('{full_url}', {{",
        f"  method: '{method}',",
        "  headers: {",
        "    'X-Requested-With': 'XMLHttpRequest',",
        "  },",
    ]
    if method == 'POST':
        ts_lines.append("  body: new URLSearchParams({ variable: '101', period: 'week' }),")
    ts_lines.append("});")
    ts_lines.append("const data = await response.json();")
    ts_lines.append("console.log(data);")
    typescript = "\n".join(ts_lines)

    return curl, python, typescript

def main():
    spec = load_spec()
    title = spec.get('info', {}).get('title', 'Weathercloud API')
    version = spec.get('info', {}).get('version', '1.0.0')

    categories = {}
    endpoints = []

    for path, methods in spec.get('paths', {}).items():
        for method, op in methods.items():
            if method not in ['get', 'post', 'put', 'delete', 'patch']:
                continue
            tag = (op.get('tags') or ['General'])[0]
            if tag not in categories:
                categories[tag] = []
            
            # Resolve parameters
            resolved_params = []
            for p in op.get('parameters', []):
                if '$ref' in p:
                    ref_name = p['$ref'].split('/')[-1]
                    ref_param = spec.get('components', {}).get('parameters', {}).get(ref_name, {})
                    resolved_params.append(ref_param)
                else:
                    resolved_params.append(p)

            op_id = op.get('operationId') or f"{method}_{path}".replace('/', '_').replace('{', '').replace('}', '')
            ep = {
                'id': op_id,
                'path': path,
                'method': method.upper(),
                'summary': op.get('summary', path),
                'description': op.get('description', ''),
                'tag': tag,
                'group': op.get('x-fern-sdk-group-name', ''),
                'sdkMethod': op.get('x-fern-sdk-method-name', ''),
                'availability': op.get('x-fern-availability', 'generally-available'),
                'parameters': resolved_params,
                'requestBody': op.get('requestBody', {}),
                'responses': op.get('responses', {})
            }
            curl, python, typescript = get_code_samples(ep)
            ep['curl'] = curl
            ep['python'] = python
            ep['typescript'] = typescript
            
            categories[tag].append(ep)
            endpoints.append(ep)

    os.makedirs("docs", exist_ok=True)
    
    html = f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Reference</title>
  <link rel="icon" type="image/svg+xml" href="https://app.weathercloud.net/favicon.ico" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0b0f19;
      --bg-sidebar: #0f172a;
      --bg-card: #131b2e;
      --bg-code: #0a0e17;
      --border: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.15);
      --accent: #f6821f;
      --accent-muted: rgba(246, 130, 31, 0.15);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --badge-get-bg: rgba(16, 185, 129, 0.15);
      --badge-get-text: #34d399;
      --badge-post-bg: rgba(59, 130, 246, 0.15);
      --badge-post-text: #60a5fa;
      --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, Menlo, Consolas, monospace;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: var(--font);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }}
    /* Top Header */
    header {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 56px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
      z-index: 50;
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .logo-badge {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 700;
      font-size: 1rem;
      color: #fff;
      text-decoration: none;
    }}
    .logo-badge svg {{
      color: var(--accent);
    }}
    .version-tag {{
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 9999px;
      background: var(--accent-muted);
      color: var(--accent);
      font-weight: 600;
      font-family: var(--font-mono);
    }}
    .fern-pill {{
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .header-search {{
      position: relative;
      width: 320px;
    }}
    .search-input {{
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.45rem 2rem 0.45rem 2.2rem;
      color: var(--text);
      font-size: 0.85rem;
      font-family: var(--font);
      outline: none;
      transition: all 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-muted);
    }}
    .search-icon {{
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      pointer-events: none;
    }}
    .search-kbd {{
      position: absolute;
      right: 0.6rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 0.7rem;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 1px 5px;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }}
    .header-right {{
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .header-link {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
      transition: color 0.15s;
    }}
    .header-link:hover {{
      color: #fff;
    }}

    /* Main Container */
    .app-container {{
      display: flex;
      margin-top: 56px;
      min-height: calc(100vh - 56px);
    }}

    /* Sidebar Navigation */
    aside.sidebar {{
      width: 290px;
      flex-shrink: 0;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border);
      height: calc(100vh - 56px);
      position: sticky;
      top: 56px;
      overflow-y: auto;
      padding: 1rem 0;
    }}
    .sidebar-group {{
      margin-bottom: 1.25rem;
    }}
    .group-title {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-dim);
      padding: 0.25rem 1.25rem;
      margin-bottom: 0.25rem;
    }}
    .nav-item {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.4rem 1.25rem;
      font-size: 0.825rem;
      color: var(--text-muted);
      text-decoration: none;
      transition: all 0.15s;
      border-left: 2px solid transparent;
      cursor: pointer;
    }}
    .nav-item:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.03);
    }}
    .nav-item.active {{
      color: var(--accent);
      background: var(--accent-muted);
      border-left-color: var(--accent);
      font-weight: 500;
    }}
    .method-badge {{
      font-size: 0.65rem;
      font-weight: 700;
      font-family: var(--font-mono);
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.03em;
    }}
    .method-badge.get {{
      background: var(--badge-get-bg);
      color: var(--badge-get-text);
    }}
    .method-badge.post {{
      background: var(--badge-post-bg);
      color: var(--badge-post-text);
    }}

    /* Content Area: Center + Right */
    main.content {{
      flex: 1;
      display: flex;
      overflow-x: hidden;
    }}
    .doc-pane {{
      flex: 1;
      max-width: 680px;
      padding: 2.5rem;
    }}
    .code-pane {{
      width: 480px;
      flex-shrink: 0;
      padding: 2.5rem 1.5rem 2.5rem 0;
      position: sticky;
      top: 56px;
      height: calc(100vh - 56px);
      overflow-y: auto;
    }}

    /* Operation Header */
    .op-header {{
      margin-bottom: 2rem;
    }}
    .op-meta-pills {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.75rem;
      flex-wrap: wrap;
    }}
    .sdk-group-pill {{
      font-size: 0.75rem;
      font-family: var(--font-mono);
      padding: 2px 8px;
      border-radius: 6px;
      background: rgba(246, 130, 31, 0.1);
      color: var(--accent);
      border: 1px solid rgba(246, 130, 31, 0.2);
    }}
    .avail-pill {{
      font-size: 0.7rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.1);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.2);
    }}
    .op-title {{
      font-size: 1.75rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 0.75rem;
      color: #fff;
    }}
    .endpoint-pill {{
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.4rem 0.75rem;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      margin-bottom: 1.25rem;
    }}
    .endpoint-pill .path {{
      color: #e2e8f0;
    }}
    .op-desc {{
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.6;
      margin-bottom: 2rem;
    }}

    /* Section Headings */
    .section-title {{
      font-size: 0.95rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
      margin: 1.75rem 0 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    /* Parameters Table */
    .params-table {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 2rem;
      background: var(--bg-card);
    }}
    .param-row {{
      display: flex;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
      align-items: baseline;
      gap: 1rem;
    }}
    .param-row:last-child {{
      border-bottom: none;
    }}
    .param-name-col {{
      width: 160px;
      flex-shrink: 0;
    }}
    .param-name {{
      font-family: var(--font-mono);
      font-weight: 600;
      font-size: 0.85rem;
      color: #fff;
    }}
    .param-type {{
      font-size: 0.75rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
      margin-top: 2px;
    }}
    .param-req {{
      color: #ef4444;
      font-size: 0.7rem;
      margin-left: 2px;
    }}
    .param-desc-col {{
      flex: 1;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    /* Code Console Box */
    .console-box {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 1.25rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}
    .console-header {{
      background: rgba(15, 23, 42, 0.6);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.4rem 0.75rem;
    }}
    .lang-tabs {{
      display: flex;
      gap: 0.25rem;
    }}
    .tab-btn {{
      background: none;
      border: none;
      color: var(--text-dim);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-family: var(--font);
      transition: all 0.15s;
    }}
    .tab-btn:hover {{
      color: #fff;
    }}
    .tab-btn.active {{
      background: rgba(255, 255, 255, 0.08);
      color: var(--accent);
    }}
    .copy-btn {{
      background: none;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      padding: 4px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      transition: color 0.15s;
    }}
    .copy-btn:hover {{
      color: #fff;
    }}
    .code-content {{
      padding: 1rem;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: #e2e8f0;
      background: var(--bg-code);
      overflow-x: auto;
      white-space: pre;
      line-height: 1.6;
    }}

    /* Response Preview */
    .response-status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      font-family: var(--font-mono);
      color: #34d399;
    }}
    .response-status-badge::before {{
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
    }}

    /* Empty state / hidden */
    .op-section {{
      display: none;
    }}
    .op-section.active {{
      display: block;
    }}

    /* Scrollbars */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.12);
      border-radius: 3px;
    }}
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <a href="#" class="logo-badge">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
        </svg>
        <span>{title}</span>
      </a>
      <span class="version-tag">v{version}</span>
      <span class="fern-pill">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
        Forge & Fern Docs
      </span>
    </div>

    <div class="header-search">
      <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="text" id="searchInput" class="search-input" placeholder="Search endpoints... (Press /)" />
      <span class="search-kbd">/</span>
    </div>

    <div class="header-right">
      <a href="https://github.com/MauroDruwel/Weathercloud" target="_blank" class="header-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/></svg>
        GitHub
      </a>
      <a href="./openapi.yaml" target="_blank" class="header-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        OpenAPI Spec
      </a>
    </div>
  </header>

  <div class="app-container">
    <!-- Sidebar Navigation -->
    <aside class="sidebar" id="sidebar">
"""

    for tag, ops in categories.items():
        html += f"""      <div class="sidebar-group">
        <div class="group-title">{tag}</div>
"""
        for op in ops:
            m_class = op['method'].lower()
            html += f"""        <a class="nav-item" data-id="{op['id']}" onclick="showEndpoint('{op['id']}')">
          <span class="method-badge {m_class}">{op['method']}</span>
          <span>{op['summary']}</span>
        </a>
"""
        html += "      </div>\n"

    html += """    </aside>

    <!-- Main Content Area -->
    <main class="content">
"""

    for i, ep in enumerate(endpoints):
        is_active = "active" if i == 0 else ""
        m_class = ep['method'].lower()
        
        # Format parameters table
        params_html = ""
        params = ep.get('parameters', [])
        if params:
            params_rows = ""
            for p in params:
                req = '<span class="param-req">*</span>' if p.get('required') else ''
                schema = p.get('schema', {})
                p_type = schema.get('type', 'string')
                desc = p.get('description', '')
                ex = p.get('example', '')
                if ex:
                    desc += f" (Example: <code>{ex}</code>)"
                params_rows += f"""<div class="param-row">
                  <div class="param-name-col">
                    <div class="param-name">{p['name']}{req}</div>
                    <div class="param-type">{p_type} • {p.get('in', 'query')}</div>
                  </div>
                  <div class="param-desc-col">{desc}</div>
                </div>"""
            params_html = f"""<div class="section-title">Parameters</div>
            <div class="params-table">{params_rows}</div>"""

        # Description HTML
        desc_html = ep['description'].replace('\n', '<br/>')

        html += f"""      <!-- Operation: {ep['id']} -->
      <section class="op-section {is_active}" id="sec_{ep['id']}">
        <div style="display: flex;">
          <div class="doc-pane">
            <div class="op-header">
              <div class="op-meta-pills">
                <span class="sdk-group-pill">{ep['group']}.{ep['sdkMethod']}()</span>
                <span class="avail-pill">{ep['availability']}</span>
              </div>
              <h1 class="op-title">{ep['summary']}</h1>
              <div class="endpoint-pill">
                <span class="method-badge {m_class}">{ep['method']}</span>
                <span class="path">{ep['path']}</span>
              </div>
              <p class="op-desc">{desc_html}</p>
            </div>

            {params_html}

            <div class="section-title">Response</div>
            <div class="params-table">
              <div class="param-row">
                <div class="param-name-col">
                  <div class="param-name">200 OK</div>
                  <div class="param-type">application/json</div>
                </div>
                <div class="param-desc-col">Successful response returning requested data or telemetry.</div>
              </div>
            </div>
          </div>

          <div class="code-pane">
            <!-- Request Snippet Box -->
            <div class="console-box">
              <div class="console-header">
                <div class="lang-tabs">
                  <button class="tab-btn active" onclick="switchTab('{ep['id']}', 'curl')">cURL</button>
                  <button class="tab-btn" onclick="switchTab('{ep['id']}', 'python')">Python</button>
                  <button class="tab-btn" onclick="switchTab('{ep['id']}', 'ts')">TypeScript</button>
                </div>
                <button class="copy-btn" title="Copy code" onclick="copyCode('{ep['id']}')">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                </button>
              </div>
              <div class="code-content" id="code_{ep['id']}">{ep['curl']}</div>
            </div>

            <!-- Response Preview Box -->
            <div class="console-box">
              <div class="console-header">
                <span class="response-status-badge">200 OK</span>
                <button class="copy-btn" title="Copy JSON" onclick="copyResponse('{ep['id']}')">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                </button>
              </div>
              <div class="code-content" id="resp_{ep['id']}">{{
  "status": "success",
  "data": {{ ... }}
}}</div>
            </div>
          </div>
        </div>
      </section>
"""

    first_ep_id = endpoints[0]['id'] if endpoints else ""

    html += f"""    </main>
  </div>

  <script>
    const snippets = {json.dumps({ep['id']: {'curl': ep['curl'], 'python': ep['python'], 'ts': ep['typescript']} for ep in endpoints})};

    function showEndpoint(id) {{
      document.querySelectorAll('.op-section').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      
      const sec = document.getElementById('sec_' + id);
      const nav = document.querySelector('.nav-item[data-id="' + id + '"]');
      if (sec) sec.classList.add('active');
      if (nav) nav.classList.add('active');
      window.location.hash = id;
    }}

    function switchTab(epId, lang) {{
      const sec = document.getElementById('sec_' + epId);
      if (!sec) return;
      sec.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      const clicked = event.target;
      clicked.classList.add('active');
      
      const codeBlock = document.getElementById('code_' + epId);
      if (codeBlock && snippets[epId]) {{
        codeBlock.textContent = snippets[epId][lang] || snippets[epId]['curl'];
      }}
    }}

    function copyCode(epId) {{
      const codeBlock = document.getElementById('code_' + epId);
      if (codeBlock) {{
        navigator.clipboard.writeText(codeBlock.textContent);
        const btn = event.currentTarget;
        btn.style.color = '#10b981';
        setTimeout(() => btn.style.color = '', 1200);
      }}
    }}

    function copyResponse(epId) {{
      const respBlock = document.getElementById('resp_' + epId);
      if (respBlock) {{
        navigator.clipboard.writeText(respBlock.textContent);
        const btn = event.currentTarget;
        btn.style.color = '#10b981';
        setTimeout(() => btn.style.color = '', 1200);
      }}
    }}

    // Search filter
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('.nav-item').forEach(item => {{
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(q) ? 'flex' : 'none';
      }});
    }});

    // Shortcut
    window.addEventListener('keydown', (e) => {{
      if (e.key === '/' && document.activeElement !== searchInput) {{
        e.preventDefault();
        searchInput.focus();
      }}
    }});

    // Initialize from hash
    const initialHash = window.location.hash.replace('#', '') || '{first_ep_id}';
    showEndpoint(initialHash);
  </script>
</body>
</html>
"""

    with open("docs/index.html", "w") as f:
        f.write(html)
    print("✓ Successfully generated Fern / Cloudflare Docs UI in docs/index.html")

if __name__ == "__main__":
    main()
