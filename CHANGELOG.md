# Changelog

## 0.2.0

- Public contract 0.2.0: working overlay lives in the store at the chair's relative paths. Checkout overlay is not the home.
- Added `write_working` for working overlay. `write` is sittings only. Wrong-layer results name the other write tool.
- `bind_workspace` takes optional `always_include` (owner list on the session card; omit leaves it).
- Both writes refuse `_meta.md`.

## 0.1.0

- Workspace memory MCP. Types: workspace, document. Layers: `working`, `sittings`.
- Markdown under `~/.contextforge/workspaces/<slug>/` is the source of truth; SQLite + FTS5 is rebuildable.
- Tools: `get_pack` (session-start card; optional `path` binds), `write`, `search`, `bind_workspace`. Workspace-scoped. Results carry `summary`. Unbound calls name `bind_workspace`.
- Public contract: `articles/methodology/use-context-forge.md`, listed from `provisions/pack.yaml`.
- Global host seed: `install/routers/`.
