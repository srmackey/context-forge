from __future__ import annotations

import pytest


def test_get_pack_syos_absent_is_named(store, harbor):
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"] is None
    assert pack["syos_parked"] is None
    assert pack["syos_wait"] is False


def test_post_syos_waits(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Hatch seals after the last line.\njump: Quay open, next is the lantern.\n---\n",
    )
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"] == {
        "check": "Hatch seals after the last line.",
        "jump": "Quay open, next is the lantern.",
    }
    assert pack["syos_parked"] is None
    assert pack["syos_wait"] is True


def test_later_moves_current_to_parked(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Hatch seals.\njump: Quay next.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nlater: true\n---\n")
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"] is None
    assert pack["syos_parked"]["check"] == "Hatch seals."
    assert pack["syos_wait"] is False


def test_second_post_keeps_parked(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Hatch seals.\njump: Quay next.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nlater: true\n---\n")
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Lantern wick is dry.\njump: Tide mark after that.\n---\n",
    )
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"]["check"] == "Lantern wick is dry."
    assert pack["syos_parked"]["check"] == "Hatch seals."
    assert pack["syos_wait"] is True


def test_unshown_post_rewrites_current(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Hatch seals.\njump: Quay next.\n---\n",
    )
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Lantern wick is dry.\njump: Keep the quay jump.\n---\n",
    )
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"]["check"] == "Lantern wick is dry."
    assert pack["syos_parked"] is None
    assert pack["syos_wait"] is True


def test_overflow_parked_becomes_sitting(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: First brief.\njump: First jump.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nlater: true\n---\n")
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Second brief.\njump: Second jump.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nlater: true\n---\n")
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Third brief.\njump: Third jump.\n---\n",
    )
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"]["check"] == "Third brief."
    assert pack["syos_parked"]["check"] == "Second brief."
    sittings = list(
        (store.workspace_dir(harbor) / "sittings").glob("*-syos-parked*.md")
    )
    assert len(sittings) == 1
    text = sittings[0].read_text(encoding="utf-8")
    assert "First brief." in text


def test_clear_current(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Hatch seals.\njump: Quay next.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nlater: true\n---\n")
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Lantern wick is dry.\njump: Tide mark.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nclear: current\n---\n")
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"] is None
    assert pack["syos_parked"]["check"] == "Hatch seals."
    assert pack["syos_wait"] is False


def test_clear_all_removes_file(store, harbor):
    store.write_working(
        harbor,
        "syos.md",
        "---\ncheck: Hatch seals.\njump: Quay next.\n---\n",
    )
    store.write_working(harbor, "syos.md", "---\nclear: all\n---\n")
    pack = store.get_pack(harbor, query=None)
    assert pack["syos"] is None
    assert pack["syos_parked"] is None
    assert not (store.workspace_dir(harbor) / "syos.md").exists()


def test_syos_write_refuses_unknown_shape(store, harbor):
    with pytest.raises(ValueError, match="syos"):
        store.write_working(harbor, "syos.md", "# just a note\n")
