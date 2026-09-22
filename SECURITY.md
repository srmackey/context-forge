# Security

## Reporting

Report a vulnerability privately with a GitHub Security Advisory on this repository. Do not open a public issue for a path escape, a vault leak, or a bug that exposes another workspace's files.

## Trust boundary

- Transport is stdio. The host starts a local process as the user who launched it.
- The process reads and writes only under the vault: `CONTEXTFORGE_HOME`, or `~/.contextforge` when that is unset.
- Binding a workspace stores that folder's path. The server does not read or write the folder's files.
- It does not use the network and it does not take a credential.
- It does write markdown and a derived SQLite index inside the vault.
- A path that escapes the workspace (`..`, or an absolute path) is refused.
