# Changelog

## 0.1.0

- Workspace memory MCP. Types: workspace, document. Layers: `working`, `sittings`.
- Markdown under `~/.contextforge/workspaces/<slug>/` is the source of truth; SQLite + FTS5 is rebuildable.
- Tools: `get_pack` (session-start card; optional `path` binds), `write`, `search`, `bind_workspace`. Workspace-scoped. Results carry `summary`. Unbound calls name `bind_workspace`.
- Public contract: `articles/methodology/use-context-forge.md`, listed from `provisions/pack.yaml`.
- Global host seed: `install/routers/`.
