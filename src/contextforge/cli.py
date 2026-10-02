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
        help="Single store. Or set CONTEXTFORGE_HOME. Default ~/.contextforge. Ignored when --root is set.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Install root that holds nexus.md. Or set CONTEXTFORGE_ROOT. Each nexus folder then holds _contextforge/.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.root:
        os.environ["CONTEXTFORGE_ROOT"] = args.root
    elif args.vault:
        os.environ["CONTEXTFORGE_HOME"] = args.vault
    from contextforge.server import main as run

    run()
