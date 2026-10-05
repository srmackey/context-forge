# Changelog

## [Unreleased]

### Added

- `CONTEXTFORGE_ROOT` (or `--root`). When that folder has `nexus.md`, each nexus keeps a store at `_contextforge/`. A call names an address. The workspace slug stays the folder basename. A bare name resolves only when it is unique. Without the root, `~/.contextforge` / `CONTEXTFORGE_HOME` is unchanged.

### Changed

- **Install reads `platforms.yaml`.** The procedure is `install/README.md`. One server block is upserted into each enabled host. The host file, the format, and the key come from the stored definition. With no environment file, user-global host config is not edited, and no project instruction file is written.
- Each tool sets read-only, destructive, idempotent, and open-world hints. None are open to the network. `search` is the read-only tool. `get_pack` is marked as a write because `path` can bind a workspace.

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
