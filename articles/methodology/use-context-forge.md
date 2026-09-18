---
id: methodology/use-context-forge
title: Use Context Forge
description: When to bind, pack, write, and search workspace memory.
---

# Use Context Forge

Context Forge is workspace memory: working files and sitting records. Markdown on disk is the truth. It is not a wiki, not standing guidance, and not a bulletin.

## When it fires

- **Session start** in a folder this store should remember: `get_pack` for this workspace. Pass `path` if it may not be bound yet. That is the card. Do not walk `search` for this view. Without `query`, FTS sittings are empty. The card still names the two most recent sittings by date, titles only, as `recent_sittings` (search for more). The card always names `syos`, `syos_parked`, and `syos_wait` (empty when absent).
- **A durable freeze-frame** for a successor in this workspace: `write` to `sittings/YYYY-MM-DD-slug.md`. Not every turn. Not a transcript. Not a wiki page.
- **The set in play** (working overlay): `write_working`. Not a sitting. Not session start.
- **A session brief** for the next sitting here: `write_working` to `syos.md`. Two beats: `check` and `jump`. If `syos_wait` is true on the pack, present the brief and wait. If only `syos_parked` is set, show it on the readout and do not freeze. `later: true` parks current. `clear: current|parked|all` clears. Act or skip clears that slot. Do not call a second tool.
- **A lookup the pack did not cover:** `search` inside that workspace only.

If the `contextforge` tools are missing, the MCP server is not connected. See `install/mcp.json.examples.md`. Do not invent a parallel file store.

## When not

- Standing guidance (constitutions, articles, composed protocol).
- Cross-workspace chatter or a published bulletin.
- Knowledge that left the workspace (a wiki capture). Context Forge does not write the wiki. If a sitting transcends the workspace, another product takes the capture; this store may hold a pointer.
- The settle operation (`methodology/settle`). This server holds the overlay files settle reads and writes. It does not run settle.

## Tools

All workspace-scoped. There is no global search.

| Tool | Writes | Job |
|---|---|---|
| `get_pack` | Only if `path` binds | Session-start card |
| `write` | Yes | Sitting freeze-frame under `sittings/` |
| `write_working` | Yes | Working overlay; not under `sittings/` |
| `search` | No | FTS in one workspace when the pack is too narrow |
| `bind_workspace` | Yes | Register a folder. Idempotent. Optional `always_include` replaces the owner list on the card. Skip if `get_pack` already has `path` |

A sitting that does not call the store misses it.

Write grain (what may go in the file) belongs to the workspace owner, not this server.

## Overlay home

This article is an overlay home. Overlay paths resolve in this store, at the same relative paths the owner articles named. Write `write_working`. Read `get_pack` or `search`. Those paths do not exist in the git checkout. Checkout absence is expected.

This article does not name the owner paths.

Reason: hosts do not share sessions. The write a successor is trained to pick up has to live in a store both hosts query.

**Class: single-system.** Groups with Context Forge.
