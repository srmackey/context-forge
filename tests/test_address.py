"""A call addressed to one nexus writes only that nexus's store."""

from __future__ import annotations

from pathlib import Path

import pytest

import contextforge.server as server


def _nexus(folder: Path, name: str, rows: list[str], parent: str | None = None) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    lines = [f"# nexus: {name}", ""]
    if parent:
        lines.extend([f"parent: {parent}", ""])
    lines.extend(
        [
            "| Node | Path | Kind | Status | Sensitive | Services | Triggers |",
            "|---|---|---|---|---|---|---|",
            *rows,
        ]
    )
    (folder / "nexus.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture
def coast(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "coast"
    _nexus(
        root,
        "coast",
        [
            "| harbor | harbor/ | nexus | active | no | status | the inner harbor |",
            "| pier | pier/ | nexus | active | yes | status | the far pier |",
        ],
    )
    _nexus(
        root / "harbor",
        "harbor",
        ["| dock | dock/ | node | active | no | status | the harbor dock |"],
        parent="coast",
    )
    _nexus(
        root / "pier",
        "pier",
        [
            "| dock | dock/ | node | active | no | status | the pier dock |",
            "| skiff | skiff/ | node | active | no | status | the skiff |",
        ],
        parent="coast",
    )
    (root / "harbor" / "dock").mkdir(parents=True)
    (root / "pier" / "dock").mkdir(parents=True)
    (root / "pier" / "skiff").mkdir(parents=True)
    monkeypatch.setenv("CONTEXTFORGE_ROOT", str(root))
    monkeypatch.delenv("CONTEXTFORGE_HOME", raising=False)
    if server._homes is not None:
        server._homes.close()
    server._homes = None
    yield root
    if server._homes is not None:
        server._homes.close()
    server._homes = None


def test_addressed_write_stays_in_that_nexus_store(coast: Path) -> None:
    bound = server.bind_workspace(str(coast / "pier" / "dock"))
    assert bound["ok"] is True
    assert bound["address"] == "pier/dock"
    assert bound["workspace"] == "dock"
    assert bound["sensitive"] is True

    written = server.write("pier/dock", "sittings/2026-10-02-watch.md", "tide at the pier")
    assert written["ok"] is True
    assert written["address"] == "pier/dock"

    pier_file = (
        coast / "pier" / "_contextforge" / "workspaces" / "dock" / "sittings" / "2026-10-02-watch.md"
    )
    harbor_file = (
        coast / "harbor" / "_contextforge" / "workspaces" / "dock" / "sittings" / "2026-10-02-watch.md"
    )
    assert pier_file.is_file()
    assert "tide at the pier" in pier_file.read_text(encoding="utf-8")
    assert not harbor_file.exists()


def test_ambiguous_bare_name_is_refused(coast: Path) -> None:
    refused = server.write("dock", "sittings/2026-10-02-watch.md", "which dock")
    assert refused["ok"] is False
    assert refused["error"] == "unknown_address"
    assert not (coast / "pier" / "_contextforge").exists()
    assert not (coast / "harbor" / "_contextforge").exists()


def test_unique_bare_name_opens_that_nodes_store(coast: Path) -> None:
    bound = server.bind_workspace(str(coast / "pier" / "skiff"), slug="skiff")
    assert bound["ok"] is True
    assert bound["address"] == "pier/skiff"

    written = server.write("skiff", "sittings/2026-10-02-watch.md", "one skiff")
    assert written["ok"] is True
    assert written["address"] == "pier/skiff"
    assert (
        coast / "pier" / "_contextforge" / "workspaces" / "skiff" / "sittings" / "2026-10-02-watch.md"
    ).is_file()
    assert not (coast / "harbor" / "_contextforge").exists()
