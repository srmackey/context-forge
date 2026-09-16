from __future__ import annotations

import argparse
import os


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="contextforge",
        description="Context Forge MCP server: workspace memory.",
    )
    parser.add_argument(
        "--vault",
        default=None,
        help="Vault root. Or set CONTEXTFORGE_HOME. Default ~/.contextforge.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.vault:
        os.environ["CONTEXTFORGE_HOME"] = args.vault
    from contextforge.server import main as run

    run()
