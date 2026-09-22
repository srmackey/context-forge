# Changelog

## [Unreleased]

### Added

- Security policy: how to report a vulnerability, and what the local process can touch.
- README states the tools, the trust boundary, and how to launch the server on the hosts this repo is run from.

## 0.3.2

- `get_pack` and `search` reindex the workspace from disk first. Files added or edited without a write tool are found; files deleted on disk drop out of results.
- `get_pack` returns `reindexed` (files touched) and names it in the summary when nonzero.

## 0.3.1

- `get_pack` returns `recent_sittings`: the two most recent sitting titles and paths. FTS `sittings` stay empty without a query.
- Public contract 0.4.0: this article is an overlay home. Overlay paths resolve in the store. Owner articles name the paths. Checkout absence is expected.
- Public contract 0.4.1: the session-start card names that preview (search for more).

## 0.3.0

- Session brief on the pack: reserved path `syos.md`. `get_pack` returns `syos`, `syos_parked`, and `syos_wait`.
- `write_working` to `syos.md` posts a new current brief (`check` + `jump`), parks with `later: true`, or clears with `clear: current|parked|all`. No new tools.
- One current (wait) and one parked (no wait). A third parked brief overflows to `sittings/YYYY-MM-DD-syos-parked.md`.
- `syos_wait` true means present the brief and wait. Empty fields stay on the pack so the sitting knows it looked.

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
