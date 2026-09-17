---
id: methodology/use-context-forge
title: Use Context Forge
description: When to bind, pack, write, and search workspace memory.
---

# Use Context Forge

Context Forge is workspace memory: working files and sitting records. Markdown on disk is the truth. It is not a wiki, not standing guidance, and not a bulletin.

## When it fires

- **Session start** in a folder this store should remember: `get_pack` for this workspace. Pass `path` if it may not be bound yet. That is the card. Do not walk `search` for this view. Without `query`, the card is `always_include` only (no sittings).
- **A durable freeze-frame** for a successor in this workspace: `write` to `sittings/YYYY-MM-DD-slug.md`. Not every turn. Not a transcript. Not a wiki page.
- **The set in play** (working overlay): `write_working`. Not a sitting. Not session start.
- **A lookup the pack did not cover:** `search` inside that workspace only.

If the `contextforge` tools are missing, the MCP server is not connected. See `install/mcp.json.examples.md`. Do not invent a parallel file store.

## When not

- Standing guidance (constitutions, articles, composed protocol).
- Cross-workspace chatter or a published bulletin.
- Knowledge that left the workspace (a wiki capture). Context Forge does not write the wiki. If a sitting transcends the workspace, another product takes the capture; this store may hold a pointer.
- Settle / status. This server is not that card.

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

Reason: hosts do not share sessions. The write a successor is trained to pick up has to live in a store both hosts query.

**Class: single-system.** Groups with Context Forge.
