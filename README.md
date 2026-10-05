# Context Forge

Context Forge gives an AI client a local memory of one workspace: working files and sitting notes, stored as markdown.

Not for a wiki, standing guidance, or a bulletin. There is no search across workspaces.

Markdown under `~/.contextforge/` is the source of truth (override with `CONTEXTFORGE_HOME`). SQLite + FTS5 is a derived index and can be rebuilt.

Set `CONTEXTFORGE_ROOT` to an install that has `nexus.md` when each nexus should keep its own store at `<nexus>/_contextforge/`. A call then names an address (`pier/dock`). The workspace slug stays the folder basename. Without that root, the single store above is the whole product.

## Capabilities

Five tools. Each call names one workspace.

| Tool | Inputs | Returns | Side effects |
|---|---|---|---|
| `get_pack` | workspace, optional query, limit, path | The session card: included files, recent sittings, and the session brief | Reads the vault. Reindexes files changed on disk. Binds the workspace when `path` is set. |
| `write` | workspace, path, content | The written document | Writes a sitting. The path must be under `sittings/`. |
| `write_working` | workspace, path, content | The written document | Writes a working file. The path must not be under `sittings/`. `syos.md` is the session brief. |
| `search` | workspace, query, optional limit | Hits and a count | Reads one workspace. Reindexes files changed on disk. Does not write a document. |
| `bind_workspace` | path, optional slug and always_include | Workspace meta | Writes the workspace record in the vault. Does not read that folder's files. |

Every tool sets `openWorldHint` false. `search` is read-only. The other four can write in the vault, and a second call with the same arguments does not add more damage. `get_pack` writes only when `path` is set and a bind runs.

On initialize the server returns a short operating note (call `get_pack` at session start, use `write` for sittings and `write_working` for everything else). That note lives in the server. This page does not repeat it.

How the pieces fit together is in [DESIGN.md](DESIGN.md).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- FastMCP 2, over stdio

## Configure a client

The procedure is [install/README.md](install/README.md). The block is [install/mcp.json.examples.md](install/mcp.json.examples.md). Host files come from `platforms.yaml` next to `nexus.md`. With no environment file, user-global host config is left alone, and no project instruction file is written.

```yaml
command: uv
args: ["run", "--directory", "/path/to/context-forge", "contextforge"]
```

Set `CONTEXTFORGE_HOME` when the vault should not be `~/.contextforge`.

## Trust boundary

- Transport is stdio. The host starts a local process as the user who launched it.
- Without `CONTEXTFORGE_ROOT`, the process reads and writes only under the vault (`CONTEXTFORGE_HOME`, or `~/.contextforge`). With that root set, it reads and writes `_contextforge/` under each nexus folder in the install.
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
