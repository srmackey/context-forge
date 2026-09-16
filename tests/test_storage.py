from __future__ import annotations

import pytest

from contextforge.storage import safe_relpath


def test_bind_defaults_slug_to_folder_name(store, tmp_path):
    folder = tmp_path / "harbor-notes"
    folder.mkdir()
    meta = store.bind_workspace(str(folder))
    assert meta["workspace"] == "harbor-notes"
    assert meta["sensitive"] is False
    assert meta["always_include"] == []
    assert (store.workspace_dir("harbor-notes") / "sittings").is_dir()


def test_write_sitting_defaults_layer(store, harbor):
    doc = store.write(
        harbor,
        "sittings/2026-09-16-first.md",
        "---\ntitle: Harbor docking\ndate: 2026-09-16\n---\n\n# Harbor docking\n\nThe hatch seals.\n",
    )
    assert doc["layer"] == "sittings"
    assert doc["title"] == "Harbor docking"


def test_search_finds_sitting(store, harbor):
    store.write(
        harbor,
        "sittings/2026-09-16-first.md",
        "# Harbor docking\n\nThe hatch seals against weather.\n",
    )
    hits = store.search(harbor, "hatch")
    assert len(hits) == 1
    assert hits[0]["path"] == "sittings/2026-09-16-first.md"


def test_get_pack_lists_dropped(store, harbor):
    store.write(harbor, "sittings/2026-09-16-a.md", "# Alpha hatch\n")
    store.write(harbor, "sittings/2026-09-16-b.md", "# Beta hatch\n")
    store.write(harbor, "sittings/2026-09-16-c.md", "# Gamma hatch\n")
    pack = store.get_pack(harbor, query="hatch", limit=2)
    assert len(pack["sittings"]) == 2
    assert len(pack["dropped"]) == 1
    assert pack["dropped"][0].startswith("sittings/")


def test_refuses_escape_paths():
    with pytest.raises(ValueError):
        safe_relpath("../secret.md")
    with pytest.raises(ValueError):
        safe_relpath("/tmp/x.md")


def test_write_refuses_escape(store, harbor):
    with pytest.raises(ValueError):
        store.write(harbor, "../outside.md", "nope")
