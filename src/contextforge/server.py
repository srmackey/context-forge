from __future__ import annotations

import atexit
import logging
import os
import sys
from typing import Any

from fastmcp import FastMCP

from .storage import Storage

INSTRUCTIONS = """\
Context Forge: local workspace memory.

Types: workspace (bound folder) and document (markdown path under it).
Layers: sittings (under sittings/) and working (everything else).

Data lives under ~/.contextforge/ (override with CONTEXTFORGE_HOME). Markdown
is the source of truth; SQLite+FTS5 is derived.

Tools are workspace-scoped. Bind first. There is no global search.
Write is explicit: sittings/YYYY-MM-DD-slug.md for a freeze-frame.
get_pack returns always_include plus FTS sittings. Dropped hits are listed.
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


_setup_logging()
mcp = FastMCP("ContextForge", instructions=INSTRUCTIONS)
_storage = Storage()


@mcp.tool
def bind_workspace(path: str, slug: str | None = None) -> dict[str, Any]:
    """Bind a folder as a workspace. Slug defaults to the folder basename."""
    return _storage.bind_workspace(path, slug)


@mcp.tool
def write(workspace: str, path: str, content: str) -> dict[str, Any]:
    """Write a markdown document at a path inside the workspace."""
    return _storage.write(workspace, path, content)


@mcp.tool
def get_pack(
    workspace: str,
    query: str | None = None,
    limit: int = 8,
) -> dict[str, Any]:
    """always_include plus FTS over sittings. Dropped hits are listed."""
    return _storage.get_pack(workspace, query=query, limit=limit)


@mcp.tool
def search(workspace: str, query: str, limit: int = 20) -> list[dict[str, Any]]:
    """FTS inside one workspace only."""
    return _storage.search(workspace, query, limit=limit)


def _shutdown() -> None:
    _storage.close()


atexit.register(_shutdown)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
