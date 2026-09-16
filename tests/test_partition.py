from __future__ import annotations


def test_search_does_not_cross_workspaces(store, harbor, river):
    store.write(
        harbor,
        "sittings/2026-09-16-dock.md",
        "# Harbor docking\n\nUnique phrase quayside-lantern.\n",
    )
    store.write(
        river,
        "sittings/2026-09-16-books.md",
        "# River books\n\nLedgers only.\n",
    )
    harbor_hits = store.search(harbor, "quayside-lantern")
    river_hits = store.search(river, "quayside-lantern")
    assert len(harbor_hits) == 1
    assert river_hits == []


def test_get_pack_does_not_cross_workspaces(store, harbor, river):
    store.write(
        harbor,
        "sittings/2026-09-16-dock.md",
        "# Harbor docking\n\nUnique phrase quayside-lantern.\n",
    )
    pack = store.get_pack(river, query="quayside-lantern")
    assert pack["sittings"] == []
    assert pack["workspace"] == "river-ledger"
