# Server block

Context Forge is one process and one vault. Set the vault with `CONTEXTFORGE_HOME`, or pass `--vault`. If neither is set, the server uses `~/.contextforge`.

Set `CONTEXTFORGE_ROOT` to an install that has `nexus.md` when each nexus should keep `_contextforge/` under its own folder. The workspace argument is then an address. Leave it unset to keep the single vault above. `--root` sets the same variable and wins over `--vault`.

Where this block is written is `install/README.md`. The host file, the format, and the key come from `platforms.yaml`. This page does not name them.

Replace the checkout path with this repo.

```yaml
command: uv
args:
  - run
  - --directory
  - /path/to/context-forge
  - contextforge
```

Set `CONTEXTFORGE_HOME` on `env` when the vault should not be `~/.contextforge`.

When `format` is `json`, write that as an object under the definition's `key`. When `format` is `toml`, write it as a table under that key.
