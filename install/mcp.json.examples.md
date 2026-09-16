# MCP host snippets

Context Forge is one process and one vault. Set the vault with `CONTEXTFORGE_HOME`, or pass `--vault`. If neither is set, the server uses `~/.contextforge`.

Replace the repo path with your checkout.

## Cursor (`~/.cursor/mcp.json` or project `.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "contextforge": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/context-forge",
        "contextforge"
      ]
    }
  }
}
```

## Claude Code (`~/.claude.json` mcpServers, or a project `.mcp.json`)

```json
{
  "mcpServers": {
    "contextforge": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/context-forge",
        "contextforge"
      ]
    }
  }
}
```

## Grok

```json
{
  "mcpServers": {
    "contextforge": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/context-forge",
        "contextforge"
      ]
    }
  }
}
```
