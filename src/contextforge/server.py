from __future__ import annotations

import atexit
import logging
import os
import sys
from typing import Any

from fastmcp import FastMCP

from .storage import Storage, UnboundWorkspace

INSTRUCTIONS = """\
Context Forge: local workspace memory.

Types: workspace (bound folder) and document (markdown path under it).
Layers: sittings (under sittings/) and working (everything else).

Data lives under ~/.contextforge/ (override with CONTEXTFORGE_HOME). Markdown
is the source of truth; SQLite+FTS5 is derived. There is no global search.

Session start: get_pack for this workspace. Pass path if it may not be bound yet.
That card binds if needed. Do not walk search for the common sitting view.

Write a sitting when something is durable for a successor here:
sittings/YYYY-MM-DD-slug.md. Not every turn. Not a wiki.

If a workspace is not bound, the result names bind_workspace (or get_pack with path).
"""


def _setup_logging() -> None:
    level_name = os.environ.get("CONTEXTFORGE_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    )
    log = logging.getLogger("contextforge")
    log.setLevel(level)
    log.addHandler(handler)


def _unbound(workspace: str) -> dict[str, Any]:
    return {
        "ok": False,
        "summary": f"Workspace {workspace!r} is not bound.",
        "try": "bind_workspace",
        "hint": "Pass the folder path. Slug defaults to the basename. Or call get_pack with path.",
        "workspace": workspace,
    }


_setup_logging()
mcp = FastMCP("ContextForge", instructions=INSTRUCTIONS)
_storage = Storage()


@mcp.tool
def bind_workspace(path: str, slug: str | None = None) -> dict[str, Any]:
    """Register a folder as a workspace. Writes. Idempotent.

    Use when this folder is not bound yet, or to refresh the bind path.
    Do not use for the sitting view; that is get_pack (pass path there if unbound).
    Do not use to write a sitting; that is write.

    Returns the workspace meta (slug, bind, always_include, sensitive) plus summary.
    """
    meta = _storage.bind_workspace(path, slug)
    ws = meta["workspace"]
    return {
        "ok": True,
        "summary": f"Bound {ws}. sensitive={meta['sensitive']}.",
        "next": "Call get_pack for this sitting.",
        **meta,
    }


@mcp.tool
def write(workspace: str, path: str, content: str) -> dict[str, Any]:
    """Write a markdown document in one workspace. Writes.

    Use when something is durable for a successor in this workspace.
    Sitting freeze-frames go at sittings/YYYY-MM-DD-slug.md. Layer defaults from path.
    Do not use for a wiki or standing guidance. Do not use to read; that is get_pack or search.
    If the workspace is not bound, the result names bind_workspace.

    Returns the written document (path, layer, title) plus summary.
    """
    try:
        doc = _storage.write(workspace, path, content)
    except UnboundWorkspace as exc:
        return _unbound(exc.workspace)
    return {
        "ok": True,
        "summary": f"Wrote {doc['path']} ({doc['layer']}) in {workspace}.",
        "next": "Call get_pack if a successor needs this in view. Do not write a wiki from this tool.",
        **doc,
    }


@mcp.tool
def get_pack(
    workspace: str,
    query: str | None = None,
    limit: int = 8,
    path: str | None = None,
) -> dict[str, Any]:
    """Session-start card: always_include plus FTS sittings for this workspace. Read.

    Use at step-in or session start. Pass path to bind if the workspace may be new.
    Pass query for the sitting's goal. Dropped hits are listed, not silent.
    Do not walk search for this view. Do not use to write.

    Returns always_include, sittings, dropped, missing_include, plus summary.
    Writes only if path is set and bind runs.
    """
    try:
        pack = _storage.get_pack(workspace, query=query, limit=limit, path=path)
    except UnboundWorkspace as exc:
        return _unbound(exc.workspace)
    dropped = pack.get("dropped") or []
    n_inc = len(pack.get("always_include") or [])
    n_sit = len(pack.get("sittings") or [])
    summary = f"Pack for {pack['workspace']}: {n_inc} always_include, {n_sit} sittings."
    if dropped:
        summary += f" {len(dropped)} dropped."
    return {
        "ok": True,
        "summary": summary,
        "next": "Write a sitting if something is durable for a successor here.",
        **pack,
    }


@mcp.tool
def search(workspace: str, query: str, limit: int = 20) -> dict[str, Any]:
    """FTS inside one workspace. Read. Does not write.

    Use when get_pack is too narrow or you need working files as well as sittings.
    Do not use as session start; that is get_pack. There is no global search.

    Returns hits and count plus summary. If unbound, names bind_workspace.
    """
    try:
        hits = _storage.search(workspace, query, limit=limit)
    except UnboundWorkspace as exc:
        return _unbound(exc.workspace)
    n = len(hits)
    summary = (
        f"{n} hit(s) in {workspace} for {query!r}."
        if n
        else f"No hits in {workspace} for {query!r}."
    )
    return {
        "ok": True,
        "summary": summary,
        "workspace": workspace,
        "count": n,
        "hits": hits,
    }


def _shutdown() -> None:
    _storage.close()


atexit.register(_shutdown)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
