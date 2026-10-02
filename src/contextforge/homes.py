"""Pick the nexus store an address names.

CONTEXTFORGE_ROOT is the install root. Each nexus folder holds
`_contextforge/`. The workspace slug stays the folder basename. With no
registry, one store at CONTEXTFORGE_HOME behaves as before.
"""

from __future__ import annotations

from pathlib import Path

from contextforge.address import Located, load_tree, registry_root, resolve
from contextforge.address import derive_key
from contextforge.storage import Storage, default_home

_STORE = "_contextforge"


class UnknownAddress(ValueError):
    def __init__(self, address: str):
        self.address = address
        super().__init__(f"unknown address: {address}")


class Homes:
    def __init__(self, registry: Path | None, fallback: Path | None):
        self.registry = registry
        self._fallback = Storage(fallback) if registry is None else None
        self._stores: dict[Path, Storage] = {}

    def close(self) -> None:
        if self._fallback is not None:
            self._fallback.close()
        for store in self._stores.values():
            store.close()
        self._stores.clear()

    def open_address(self, address: str) -> tuple[Storage, Located]:
        if self.registry is None:
            raise RuntimeError("open_address requires a registry")
        tree = load_tree(self.registry)
        if tree is None:
            raise UnknownAddress(address)
        located = resolve(tree, address)
        if located is None:
            raise UnknownAddress(address)
        return self._store(located.nexus_dir / _STORE), located

    def open_path(self, path: str) -> tuple[Storage, Located]:
        if self.registry is None:
            raise RuntimeError("open_path requires a registry")
        key = derive_key(self.registry, Path(path))
        if key is None:
            raise UnknownAddress(path)
        return self.open_address(key)

    def fallback(self) -> Storage:
        if self._fallback is None:
            raise RuntimeError("no fallback store")
        return self._fallback

    def _store(self, home: Path) -> Storage:
        resolved = home.resolve()
        found = self._stores.get(resolved)
        if found is None:
            found = Storage(resolved)
            self._stores[resolved] = found
        return found


def load_homes() -> Homes:
    registry = registry_root()
    if registry is not None:
        return Homes(registry, None)
    return Homes(None, default_home())


def same_chair(workspace: str, located: Located) -> bool:
    text = workspace.strip().replace("\\", "/").casefold()
    if text == located.address or text == located.slug.casefold():
        return True
    bare = located.address.split("/")[-1]
    return text == bare
