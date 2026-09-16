# Changelog

## 0.1.0

- Workspace memory MCP. Types: workspace, document. Layers: `working`, `sittings`.
- Markdown under `~/.contextforge/workspaces/<slug>/` is the source of truth; SQLite + FTS5 is rebuildable.
- Tools: `bind_workspace`, `write`, `get_pack`, `search`. All workspace-scoped. No global search.
