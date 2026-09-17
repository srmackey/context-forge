# Install drop-ins

These files ship with the Context Forge *server*, not inside a user's vault.

Two layers. Do not mix them.

**Host seed** (`routers/`). Tiny, placed once, user-global. Tells a new agent the MCP exists and when to call it. Does not contain DESIGN, tool schemas, or vault data.

Copy or symlink:

- `routers/cursor.mdc` → `~/.cursor/rules/contextforge-router.mdc` (`alwaysApply: true`)
- `routers/claude.md` → `~/.claude/rules/contextforge-router.md`
- `routers/grok.md` → `~/.grok/rules/contextforge-router.md`

**MCP json** (`mcp.json.examples.md`). Tells the host to spawn the server process. Without this, the tools are missing. Without the seed, a connected server still goes unused.

**Public contract** is `articles/methodology/use-context-forge.md`, listed from `provisions/pack.yaml`. Harvest onto Insitu is a later install step. The host seed does not wait on that.
