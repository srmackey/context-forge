# Context Forge — Design

**Version 0.3.1**

A local MCP server for durable, cross-host workspace memory. Markdown files are the source of truth. SQLite + FTS5 is a derived index. The store lives under `~/.contextforge/` (override with `CONTEXTFORGE_HOME`).

This file is the public picture of how the system is structured. Install steps are in [README.md](README.md). What moved between versions is in [CHANGELOG.md](CHANGELOG.md). Contributor rules are in [AGENTS.md](AGENTS.md).

## What it is for

Hosts do not share sessions. A new sitting loads instructions, not last Tuesday. Context Forge is the write another agent in the same workspace is trained to pick up: working files (current state) and sittings (accreting freeze-frames).

Write is explicit. If it is durable for a successor here, someone writes it. Retrieval is index over markdown, not a vibe.

It is not a wiki (knowledge that left the workspace). It is not standing guidance. It is not a bulletin.

## Types

Two types. No domain ontology in the server.

| Type | Role |
|---|---|
| **workspace** | Bound to a working folder. Slug is the folder basename unless bind names one. |
| **document** | A markdown file under that workspace. Path is the name. |

Refs are the path under the workspace: `workspace:harbor-notes/sittings/2026-09-16-first`.

## Layers

Two layers. They share permission and retrieval. They do not share a meaning the server has to know.

| Layer | What | On disk |
|---|---|---|
| `working` | The set in play. Replaced in place. | Default for everything not under `sittings/` |
| `sittings` | Freeze-frames of sittings. The pile that grows. | Folder `sittings/` |

Layer is frontmatter, defaulted by path. The store does not validate the body. What may go in a file is the workspace owner's grain, not a server enum.

## Layout

```
~/.contextforge/
  config.json
  .index/
    store.db
  workspaces/
    harbor-notes/
      _meta.md
      _status/
        STATUS.md
      syos.md
      sittings/
        2026-09-16-first.md
```

`_meta.md` holds bind path, `always_include`, and `sensitive` (enforcement bit for a future cross-workspace API; v0.2 has no global search).

## Tools (v0.3.1)

All workspace-scoped. Each result carries `ok`, `summary`, and (on success) `next` or (if unbound) `try`.

1. `get_pack` — session-start card: `always_include` plus FTS sittings, plus `recent_sittings`, plus `syos` / `syos_parked` / `syos_wait`. Pass `path` to bind if the workspace may be new. Without `query`, FTS sittings are empty. `recent_sittings` is the two latest sitting titles (search for more), not retrieval. Dropped hits listed, not silent. `syos_wait` true: present the brief and wait. Not a settle API.
2. `write` — sitting freeze-frame. Path must be under `sittings/`. Convention: `sittings/YYYY-MM-DD-slug.md`.
3. `write_working` — working overlay. Path must not be under `sittings/`. Reserved path `syos.md`: `check`+`jump` posts current, `later: true` parks, `clear: current|parked|all`. Wrong-layer calls name the other write tool.
4. `search` — FTS inside one workspace when the pack is too narrow. Returns `{summary, count, hits}`, not a bare list.
5. `bind_workspace` — register the folder only. Idempotent. Optional `always_include` replaces the owner list on the card. Skip if `get_pack` already has `path`.

Call or miss it. Same reliability as any store that is queried rather than auto-loaded. Bind-then-write is not a required session order: `get_pack` with `path` is independently valid; an unbound `write` or `search` names `bind_workspace`.

## Invariants

- Markdown wins. The index is rebuildable.
- No global FTS. A query in `river-ledger` cannot return `harbor-notes` documents.
- Destructive path traversal is refused (`..`, absolute paths).
- `sensitive: true` on `_meta.md` is reserved so a later cross-workspace API has something to refuse. v0.2 does not offer that API.
- Promote-to-wiki is not a Context Forge tool. If a sitting transcends the workspace, another product writes the capture; this store only holds a pointer.

## What it does not do

- No vector / semantic search. FTS5 is the search.
- No HTTP/SSE, no multi-tenancy. Stdio, one user.
- No silent workspace detection from cwd. Bind is explicit: `bind_workspace`, or `get_pack` with `path`.
- No auto-capture, no transcript dump, no lint of document bodies.
- No wiki write.

## Runtime vs this repo

The product store is `~/.contextforge/`. This git repo is the server, the tests, and the contributor docs. Do not treat the checkout as the vault.
