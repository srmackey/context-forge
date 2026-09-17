# AGENTS.md — Context Forge

Guidance for agents and contributors working in this repo.

**Product.** Context Forge is a local MCP server for workspace memory. It stores working files and sitting records as markdown. A derived SQLite+FTS5 index is rebuildable. The store lives under `~/.contextforge/` (override with `CONTEXTFORGE_HOME`).

## Agent stance

You are a careful steward of a small, markdown-first memory MCP. Files on disk are the truth. Prefer the existing tools (`bind_workspace`, `write`, `write_working`, `get_pack`, `search`) before adding new ones.

## Stack

- Python 3.11+, `uv`, FastMCP, Pydantic v2
- Markdown + YAML frontmatter on disk; SQLite + FTS5 is derived
- Tests with pytest under `tests/`
- `uv sync` / `uv run pytest` / `uv run contextforge`

## Invariants

- Two types: `workspace` (bound to a folder basename) and `document` (a markdown file under that workspace). Paths are the names. No domain ontology in the server.
- Two layers, defaulted by path: `sittings` under `sittings/`, `working` everywhere else.
- Every read and write is workspace-scoped. There is no global search.
- Markdown wins. `reindex` (internal, on write and bind) rebuilds the index.
- Write is explicit. The store does not guess, extract, or lint a document body.
- A sitting that does not call the store misses it.

## Privacy

This repo ships no real personal data and no real project names.

- Docs, comments, examples, and tests use fictional workspace vocabulary (`harbor-notes`, `river-ledger`).
- Do not commit a real vault's contents, filesystem paths, or project names.
- Write grain (what may go in a file) belongs to the bound workspace's owner, not this server.

## Public repo

This checkout may be cloned and pushed. Treat the tree, every commit, and any remote as public.

- Stage paths by name. Do not add the whole working tree at once. Never `git add -A`.
- Do not commit personal vault contents, real people's names, or another project's files.
- Do not commit `.claude/`, `.cursor/`, or `.grok/`.
- Local working files (`_status/`, `inbox/`, `_system/`, `project.yaml`, `PROTOCOL.md`) are gitignored.
- Enable the hygiene hook in a fresh clone: `git config core.hooksPath .githooks`. It also wants a `.git/hygiene-denylist`, one term per line, which is deliberately untracked.

Attribution in LICENSE and commit authorship is the intended exception.

## Layout

| Path | Role |
|------|------|
| `DESIGN.md` | How the system is structured |
| `src/contextforge/` | Server package |
| `tests/` | pytest |
| `install/` | MCP json snippets and global host-seed routers |
| `articles/` | Public contract source |
| `provisions/pack.yaml` | Extract list for that contract |
