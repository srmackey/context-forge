from __future__ import annotations

from pathlib import Path

import pytest

from contextforge.storage import Storage


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    vault = tmp_path / "vault"
    monkeypatch.setenv("CONTEXTFORGE_HOME", str(vault))
    return vault


@pytest.fixture
def store(home: Path) -> Storage:
    s = Storage(home=home)
    yield s
    s.close()


@pytest.fixture
def harbor(tmp_path: Path, store: Storage) -> str:
    folder = tmp_path / "harbor-notes"
    folder.mkdir()
    store.bind_workspace(str(folder))
    return "harbor-notes"


@pytest.fixture
def river(tmp_path: Path, store: Storage) -> str:
    folder = tmp_path / "river-ledger"
    folder.mkdir()
    store.bind_workspace(str(folder))
    return "river-ledger"
