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

MCP host snippets: [`install/mcp.json.examples.md`](install/mcp.json.examples.md).

## Tools

Every tool is workspace-scoped. Bind first, or miss it.

| Tool | Job |
|---|---|
| `bind_workspace` | Bind a folder. Slug defaults to the folder basename. Writes `_meta.md`. |
| `write` | Write a markdown document at a path inside that workspace. |
| `get_pack` | `always_include` plus FTS over sittings matching a query. Dropped hits are listed. |
| `search` | FTS inside one workspace only. |

A sitting record lives at `sittings/YYYY-MM-DD-slug.md`. Layer defaults from that path.

## Tests

Fixtures use fictional workspaces only (`harbor-notes`, `river-ledger`). Do not point a test run at a real vault.

Locked behavior: [`DESIGN.md`](DESIGN.md) (v0.1).
