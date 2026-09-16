from __future__ import annotations

import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import frontmatter

_META_FILE = "_meta.md"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
  workspace  TEXT NOT NULL,
  path       TEXT NOT NULL,
  title      TEXT,
  layer      TEXT NOT NULL,
  content    TEXT NOT NULL,
  updated_at TEXT,
  PRIMARY KEY (workspace, path)
);

CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
  workspace UNINDEXED,
  path,
  title,
  content,
  tokenize = 'porter unicode61'
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def default_home() -> Path:
    override = os.environ.get("CONTEXTFORGE_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".contextforge"


def default_layer(rel: str) -> str:
    posix = rel.replace("\\", "/").strip("/")
    if posix == "sittings" or posix.startswith("sittings/"):
        return "sittings"
    return "working"


def safe_relpath(path: str) -> str:
    """Return a posix relative path, or raise ValueError."""
    raw = path.strip().replace("\\", "/")
    if not raw or raw.startswith("/") or (len(raw) > 1 and raw[1] == ":"):
        raise ValueError("path must be relative")
    parts = [p for p in raw.split("/") if p not in ("", ".")]
    if not parts or any(p == ".." for p in parts):
        raise ValueError("path must be relative and stay inside the workspace")
    return "/".join(parts)


class Storage:
    def __init__(self, home: Path | None = None):
        self.home = Path(home) if home is not None else default_home()
        self.workspaces_dir = self.home / "workspaces"
        self.index_dir = self.home / ".index"
        self.db_path = self.index_dir / "store.db"
        self._lock = threading.Lock()
        self._conn: sqlite3.Connection | None = None
        self.home.mkdir(parents=True, exist_ok=True)
        self.workspaces_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _db(self) -> sqlite3.Connection:
        if self._conn is None:
            raise RuntimeError("storage is closed")
        return self._conn

    def workspace_dir(self, workspace: str) -> Path:
        slug = workspace.strip()
        if not slug or "/" in slug or "\\" in slug or slug in (".", ".."):
            raise ValueError("invalid workspace")
        return self.workspaces_dir / slug

    def _meta_path(self, workspace: str) -> Path:
        return self.workspace_dir(workspace) / _META_FILE

    def read_meta(self, workspace: str) -> dict[str, Any]:
        path = self._meta_path(workspace)
        if not path.exists():
            raise FileNotFoundError(f"workspace not bound: {workspace}")
        post = frontmatter.loads(path.read_text(encoding="utf-8"))
        always = post.get("always_include") or []
        if isinstance(always, str):
            always = [always]
        return {
            "workspace": workspace,
            "bind": post.get("bind"),
            "always_include": list(always),
            "sensitive": bool(post.get("sensitive", False)),
        }

    def bind_workspace(self, path: str, slug: str | None = None) -> dict[str, Any]:
        bind_path = str(Path(path).expanduser())
        workspace = (slug or Path(bind_path).name).strip()
        if not workspace:
            raise ValueError("workspace slug is empty")
        root = self.workspace_dir(workspace)
        root.mkdir(parents=True, exist_ok=True)
        (root / "sittings").mkdir(exist_ok=True)
        meta_path = root / _META_FILE
        if meta_path.exists():
            post = frontmatter.loads(meta_path.read_text(encoding="utf-8"))
            post["bind"] = bind_path
        else:
            post = frontmatter.Post(
                "Workspace bind. Layer defaults: sittings/ is sittings, everything else is working.\n"
            )
            post["bind"] = bind_path
            post["always_include"] = []
            post["sensitive"] = False
        meta_path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")
        self._index_file(workspace, _META_FILE)
        self._db().commit()
        return self.read_meta(workspace)

    def write(self, workspace: str, path: str, content: str) -> dict[str, Any]:
        self.read_meta(workspace)
        rel = safe_relpath(path)
        dest = self.workspace_dir(workspace) / Path(*rel.split("/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = content if content.endswith("\n") else content + "\n"
        dest.write_text(text, encoding="utf-8")
        doc = self._index_file(workspace, rel)
        self._db().commit()
        return doc

    def get_document(self, workspace: str, path: str) -> dict[str, Any]:
        rel = safe_relpath(path)
        dest = self.workspace_dir(workspace) / Path(*rel.split("/"))
        if not dest.exists():
            raise FileNotFoundError(rel)
        return self._document_from_file(workspace, rel, dest)

    def search(
        self,
        workspace: str,
        query: str,
        limit: int = 20,
        sittings_only: bool = False,
    ) -> list[dict[str, Any]]:
        self.read_meta(workspace)
        q = query.strip()
        if not q:
            return []
        sql = """
            SELECT d.workspace, d.path, d.title, d.layer, d.content, d.updated_at
            FROM documents_fts f
            JOIN documents d ON d.workspace = f.workspace AND d.path = f.path
            WHERE documents_fts MATCH ? AND d.workspace = ?
        """
        params: list[Any] = [_fts_or_query(q), workspace]
        if sittings_only:
            sql += " AND d.layer = 'sittings'"
        sql += " ORDER BY rank LIMIT ?"
        params.append(max(1, int(limit)))
        cur = self._db().execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def get_pack(
        self,
        workspace: str,
        query: str | None = None,
        limit: int = 8,
    ) -> dict[str, Any]:
        meta = self.read_meta(workspace)
        included: list[dict[str, Any]] = []
        missing: list[str] = []
        for rel in meta["always_include"]:
            try:
                included.append(self.get_document(workspace, rel))
            except (FileNotFoundError, ValueError):
                missing.append(rel)
        hits: list[dict[str, Any]] = []
        dropped: list[str] = []
        if query and query.strip():
            found = self.search(
                workspace,
                query,
                limit=max(1, int(limit)) + 50,
                sittings_only=True,
            )
            cap = max(1, int(limit))
            hits = found[:cap]
            dropped = [d["path"] for d in found[cap:]]
        return {
            "workspace": workspace,
            "always_include": included,
            "missing_include": missing,
            "sittings": hits,
            "dropped": dropped,
            "sensitive": meta["sensitive"],
        }

    def _document_from_file(self, workspace: str, rel: str, dest: Path) -> dict[str, Any]:
        text = dest.read_text(encoding="utf-8")
        post = frontmatter.loads(text)
        title = post.get("title") or _title_from_body(post.content) or Path(rel).stem
        layer = post.get("layer") or default_layer(rel)
        return {
            "workspace": workspace,
            "path": rel,
            "title": str(title),
            "layer": str(layer),
            "content": text,
            "updated_at": _now(),
        }

    def _index_file(self, workspace: str, rel: str) -> dict[str, Any]:
        dest = self.workspace_dir(workspace) / Path(*rel.split("/"))
        doc = self._document_from_file(workspace, rel, dest)
        db = self._db()
        with self._lock:
            db.execute(
                "DELETE FROM documents_fts WHERE workspace = ? AND path = ?",
                (workspace, rel),
            )
            db.execute(
                "DELETE FROM documents WHERE workspace = ? AND path = ?",
                (workspace, rel),
            )
            db.execute(
                """
                INSERT INTO documents (workspace, path, title, layer, content, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    doc["workspace"],
                    doc["path"],
                    doc["title"],
                    doc["layer"],
                    doc["content"],
                    doc["updated_at"],
                ),
            )
            db.execute(
                """
                INSERT INTO documents_fts (workspace, path, title, content)
                VALUES (?, ?, ?, ?)
                """,
                (doc["workspace"], doc["path"], doc["title"], doc["content"]),
            )
        return doc


def _title_from_body(body: str) -> str | None:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def _fts_or_query(text: str, max_terms: int = 50) -> str:
    terms: list[str] = []
    for raw in text.replace("\n", " ").split():
        token = "".join(ch for ch in raw if ch.isalnum() or ch in "-_")
        if token:
            terms.append('"' + token.replace('"', "") + '"')
        if len(terms) >= max_terms:
            break
    return " OR ".join(terms) if terms else '""'
