# Mock MCP Documentation Server

This repository contains a minimal Model Context Protocol (MCP) server that
exposes a single tool: `get_documentation_from_database`.

Files added:

- `mock_doc_server.py` — FastMCP server exposing `get_documentation_from_database` which returns mocked documentation records.
- `requirements.txt` — minimal Python dependency pin for the MCP SDK.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. Run the server (stdio transport):

```bash
python mock_doc_server.py
```

The server listens on STDIO and is intended to be connected to by an MCP client
(for example, an MCP client implementation or an MCP-capable host like Claude).

If you want a streamable HTTP/SSE server or to mount this server in an ASGI app,
see the examples in the MCP Python SDK docs.
# Basic project

Provide a short description here.

## Setup

1. Create a virtual environment
2. Install dependencies
3. Run your app/tests

## Notes

- Update 
equirements.txt as you add packages.

## GNews MCP Server

This workspace includes `gnews_mcp.py` — a FastMCP server that wraps the GNews
API Search and Top Headlines endpoints. Quick usage:

1. Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Set your GNews API key in the environment:

```powershell
setx GNEWS_API_KEY "<your_api_key>"
# or for current session only:
$env:GNEWS_API_KEY = "<your_api_key>"
```

3. Run the server (streamable HTTP transport):

```bash
python gnews_mcp.py
```

4. The server exposes two tools:
- `search(query, max=10, lang=None, country=None)` — GNews Search
- `top_headlines(topic=None, max=10, lang=None, country=None)` — Top Headlines

See `gnews_mcp.py` for structured response models and usage notes.
