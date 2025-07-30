"""
Command-line entry points

1. Single prompt (non-interactive):
   $ python -m ai_poet poem "quantum computing"

2. Interactive REPL:
   $ python -m ai_poet repl
"""
from __future__ import annotations

import argparse
import logging
import sys
from typing import Any

from .generator import generate_poem


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(levelname)s | %(message)s", force=True
    )


# ─────────────────────────── sub-command handlers ──────────────────────────
def _cmd_poem(args: argparse.Namespace) -> None:  # noqa: ANN001
    poem = generate_poem(args.topic)
    print("\n" + poem + "\n")


def _cmd_repl(_: argparse.Namespace) -> None:  # noqa: D401, ANN001
    print("AI-Poet interactive mode. Type 'exit' or Ctrl-D to quit.\n")
    try:
        while True:
            topic = input("Topic ➜ ").strip()
            if topic.lower() in {"exit", "quit", ""}:
                break
            print()
            print(generate_poem(topic))
            print()
    except (EOFError, KeyboardInterrupt):
        print("\nGood-bye!")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai_poet", description="Euron AI-Poet CLI")
    p.add_argument("-v", "--verbose", action="store_true", help="debug logging")

    sub = p.add_subparsers(dest="command", required=True)

    # p_poem = sub.add_parser("poem", help="Generate a single poem")
    # p_poem.add_argument("topic", help="Topic of the poem")
    # p_poem.set_defaults(func=_cmd_poem)

    p_article = sub.add_parser("article", help="Generate a single article")
    p_article.add_argument("topic", help="Topic of the article")
    p_article.set_defaults(func=_cmd_poem)

    p_repl = sub.add_parser("repl", help="Interactive chat")
    p_repl.set_defaults(func=_cmd_repl)

    return p


def run_cli(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)  # default picks up sys.argv
    _configure_logging(args.verbose)
    args.func(args)


if __name__ == "__main__":  # `python ai_poet/cli.py poem "AI"`
    run_cli()