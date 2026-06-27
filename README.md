# mcp-adapters

A small Python project that connects [MCP](https://modelcontextprotocol.io/) servers to LangChain agents using [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters).

It includes example MCP servers and a client that loads MCP tools and runs a LangChain agent powered by OpenAI.

## What it does

1. Starts an MCP server as a subprocess (stdio transport)
2. Opens an MCP client session
3. Loads MCP tools and converts them to LangChain tools
4. Runs a LangChain agent that can call those tools

Example flow: ask *"What is 54 + 2 * 3?"* → the agent calls `multiply` and `add` from the math server → returns the answer.

## Project structure

```
mcp-adapters/
├── main.py                 # MCP client + LangChain agent (main demo)
├── langchain_client.py     # Placeholder for MultiServerMCPClient approach
├── servers/
│   ├── math_server.py      # MCP server: add, multiply (stdio)
│   └── weather_server.py   # MCP server: get_weather (sse)
├── pyproject.toml
└── .env                    # API keys (not committed)
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key

## Setup

```bash
git clone https://github.com/MLmilica/mcp-adapters.git
cd mcp-adapters

# Install dependencies
uv sync

# Activate the virtual environment (optional if using uv run)
source .venv/bin/activate
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key-here
```

## Run

```bash
uv run main.py
```

Expected output:

```
session initialized
The answer is ...
```

Before running, update the math server path in `main.py` if needed:

```python
stdio_server_params = StdioServerParameters(
    command="python",
    args=["/absolute/path/to/mcp-adapters/servers/math_server.py"],
)
```

## MCP servers

### Math server (`stdio`)

`servers/math_server.py` exposes two tools:

| Tool       | Description          |
|-----------|----------------------|
| `add`     | Add two numbers      |
| `multiply`| Multiply two numbers |

Uses `transport="stdio"` — designed to be started by a client as a subprocess.

Run standalone (for testing):

```bash
uv run servers/math_server.py
```

### Weather server (`sse`)

`servers/weather_server.py` exposes:

| Tool           | Description                    |
|----------------|--------------------------------|
| `get_weather`  | Get weather for a location     |

Uses `transport="sse"` — runs as an HTTP server. Start it separately, then connect via URL.

```bash
uv run servers/weather_server.py
```

## stdio vs sse

| Transport | How it works                         | Use case                    |
|-----------|--------------------------------------|-----------------------------|
| `stdio`   | Client starts server as subprocess   | Local tools (Cursor, CLI)   |
| `sse`     | Server runs on HTTP, client uses URL | Remote / standalone server |

## Key dependencies

- [`mcp`](https://github.com/modelcontextprotocol/python-sdk) — MCP Python SDK
- [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters) — bridge MCP tools to LangChain
- [`langchain`](https://github.com/langchain-ai/langchain) + [`langchain-openai`](https://github.com/langchain-ai/langchain) — agent and LLM
- [`langgraph`](https://github.com/langchain-ai/langgraph) — agent runtime

## Using in Cursor

To use the math server directly in Cursor, add to your MCP config (`~/.cursor/mcp.json` or project settings):

```json
{
  "mcpServers": {
    "math": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-adapters/servers/math_server.py"]
    }
  }
}
```

## Next steps

- Wire up `langchain_client.py` with `MultiServerMCPClient` for multiple servers
- Connect the weather server over SSE/HTTP
- Replace the mock weather response with a real weather API
