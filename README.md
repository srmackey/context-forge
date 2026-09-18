# Context Forge

A local MCP server for workspace memory. Markdown files are the source of truth. SQLite + FTS5 is a derived index. The store lives under `~/.contextforge/` (override with `CONTEXTFORGE_HOME`).

It holds working files (the set in play) and sittings (freeze-frames of a session that a successor in the same workspace would want). It is not a wiki, not standing guidance, and not a bulletin.

## Stack

- Python 3.11+, `uv`, FastMCP, Pydantic v2
- Markdown + YAML frontmatter under `~/.contextforge/workspaces/<slug>/`
- Tests with pytest under `tests/`

## Setup

```bash
uv sync
uv run pytest
uv run contextforge
```

| Variable | Role |
|---|---|
| `CONTEXTFORGE_HOME` | Vault root (default `~/.contextforge`; or pass `--vault`) |

MCP host snippets: [`install/mcp.json.examples.md`](install/mcp.json.examples.md). Global host seed (so a new agent knows the tools exist): [`install/README.md`](install/README.md).

## Tools

Every tool is workspace-scoped. Bind first, or miss it.

| Tool | Job |
|---|---|
| `get_pack` | Session-start card. Pass `path` to bind if needed. Includes `recent_sittings`, `syos`, `syos_parked`, `syos_wait`. |
| `write` | Sitting freeze-frame under `sittings/`. |
| `write_working` | Working overlay. Not under `sittings/`. `syos.md` is the session brief. |
| `search` | FTS inside one workspace when the pack is too narrow. |
| `bind_workspace` | Bind a folder only. Optional `always_include`. Skip if `get_pack` already has `path`. |

A sitting record lives at `sittings/YYYY-MM-DD-slug.md`. Layer defaults from that path.

## Tests

Fixtures use fictional workspaces only (`harbor-notes`, `river-ledger`). Do not point a test run at a real vault.

Locked behavior: [`DESIGN.md`](DESIGN.md) (v0.3.1).
