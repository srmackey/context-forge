from __future__ import annotations

import os
import time


def _on_disk(store, workspace, rel, text):
    dest = store.workspace_dir(workspace).joinpath(*rel.split("/"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return dest


def _bump_mtime(path, seconds=5):
    later = time.time() + seconds
    os.utime(path, (later, later))


def test_search_finds_file_placed_on_disk(store, harbor):
    _on_disk(store, harbor, "_system/changelog.md", "# Changelog\n\nThe tide gauge moved.\n")
    hits = store.search(harbor, "gauge")
    assert [h["path"] for h in hits] == ["_system/changelog.md"]


def test_search_sees_disk_edit_of_written_file(store, harbor):
    store.write_working(harbor, "notes.md", "# Notes\n\nThe hatch seals.\n")
    dest = _on_disk(store, harbor, "notes.md", "# Notes\n\nThe mooring holds.\n")
    _bump_mtime(dest)
    assert [h["path"] for h in store.search(harbor, "mooring")] == ["notes.md"]
    assert store.search(harbor, "hatch") == []


def test_search_drops_file_deleted_on_disk(store, harbor):
    store.write_working(harbor, "notes.md", "# Notes\n\nThe hatch seals.\n")
    store.workspace_dir(harbor).joinpath("notes.md").unlink()
    assert store.search(harbor, "hatch") == []


def test_reindex_leaves_unchanged_files_alone(store, harbor):
    store.write_working(harbor, "notes.md", "# Notes\n\nThe hatch seals.\n")
    store.reindex(harbor)
    assert store.reindex(harbor) == 0


def test_get_pack_counts_reindexed_and_shows_disk_sitting(store, harbor):
    _on_disk(store, harbor, "sittings/2026-09-18-dropped-in.md", "# Dropped in\n\nBy hand.\n")
    pack = store.get_pack(harbor)
    assert pack["reindexed"] == 1
    assert pack["recent_sittings"][0]["path"] == "sittings/2026-09-18-dropped-in.md"
    assert store.get_pack(harbor)["reindexed"] == 0


def test_reindex_stays_in_its_workspace(store, harbor, river):
    _on_disk(store, river, "ledger.md", "# Ledger\n\nThe gauge reads low.\n")
    assert store.search(harbor, "gauge") == []
    assert [h["path"] for h in store.search(river, "gauge")] == ["ledger.md"]
