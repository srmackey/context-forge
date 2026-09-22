# Context Forge

Context Forge gives an AI client a local memory of one workspace: working files and sitting notes, stored as markdown.

Not for a wiki, standing guidance, or a bulletin. There is no search across workspaces.

Markdown under `~/.contextforge/` is the source of truth (override with `CONTEXTFORGE_HOME`). SQLite + FTS5 is a derived index and can be rebuilt.

## Capabilities

Five tools. Each call names one workspace.

| Tool | Inputs | Returns | Side effects |
|---|---|---|---|
| `get_pack` | workspace, optional query, limit, path | The session card: included files, recent sittings, and the session brief | Reads the vault. Reindexes files changed on disk. Binds the workspace when `path` is set. |
| `write` | workspace, path, content | The written document | Writes a sitting. The path must be under `sittings/`. |
| `write_working` | workspace, path, content | The written document | Writes a working file. The path must not be under `sittings/`. `syos.md` is the session brief. |
| `search` | workspace, query, optional limit | Hits and a count | Reads one workspace. Reindexes files changed on disk. Does not write a document. |
| `bind_workspace` | path, optional slug and always_include | Workspace meta | Writes the workspace record in the vault. Does not read that folder's files. |

The server does not set `readOnlyHint`, `destructiveHint`, `idempotentHint`, or `openWorldHint`. The side-effects column is the behavior.

On initialize the server returns a short operating note (call `get_pack` at session start, use `write` for sittings and `write_working` for everything else). That note lives in the server. This page does not repeat it.

How the pieces fit together is in [DESIGN.md](DESIGN.md).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- FastMCP 2, over stdio

## Configure a client

The same process, three hosts that this repo is launched from. Replace the directory with your checkout. Set `CONTEXTFORGE_HOME` when the vault should not be `~/.contextforge`.

### Cursor and Claude Code

Cursor reads `~/.cursor/mcp.json` or a project `.cursor/mcp.json`. Claude Code reads `~/.claude.json` or a project `.mcp.json`.

```json
{
  "mcpServers": {
    "contextforge": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/context-forge", "contextforge"]
    }
  }
}
```

### Grok

`~/.grok/config.toml`:

```toml
[mcp_servers.contextforge]
command = "uv"
args = ["run", "--directory", "/path/to/context-forge", "contextforge"]
```

File paths and the host seed that tells an agent when to call the tools: [install/mcp.json.examples.md](install/mcp.json.examples.md) and [install/README.md](install/README.md).

## Trust boundary

- Transport is stdio. The host starts a local process as the user who launched it.
- The process reads and writes only under the vault (`CONTEXTFORGE_HOME`, or `~/.contextforge`).
- Binding a workspace stores that folder's path. The server does not read or write the folder's files.
- It does not use the network and it does not take a credential.
- It does write markdown and a derived SQLite index inside the vault.
- A path that escapes the workspace is refused.

The same boundary, and how to report a vulnerability, is in [SECURITY.md](SECURITY.md).

## Develop from source

```bash
uv sync
uv run pytest
uv run contextforge
```

Tests use fictional workspaces (`harbor-notes`, `river-ledger`). Do not point a run at a real vault.

There is no published package yet. Install by cloning and running from the checkout, as above.

## Versioning

A tool add, remove, or rename updates the capabilities table and [CHANGELOG.md](CHANGELOG.md) in the same change. The package version is in `pyproject.toml`.

## License

MIT. See [LICENSE](LICENSE).
