#!/usr/bin/env python3
"""Client check for loom-visualization.

Reads environment markers and prints one JSON object:
{client, mermaid, remote_viewer, obsidian_vault, reason}.

`mermaid` is false for every client this script can detect: each one is
documented or reported to show Mermaid source raw, or is unverified. See
references/client-matrix.md for the sources.

`obsidian_vault` is true when the --target path, or the current working
directory when no --target is given, or an ancestor of it holds a
`.obsidian/` directory; false otherwise.

Stdlib only.
"""

import argparse
import json
import os
import sys

CODEX_MARKERS = ("CODEX_THREAD_ID", "CODEX_SANDBOX", "CODEX_CI")


def _is_obsidian_vault(target):
    """True when target, or an existing ancestor of it, holds a .obsidian/ dir."""
    path = os.path.abspath(target)
    while True:
        if os.path.isdir(os.path.join(path, ".obsidian")):
            return True
        parent = os.path.dirname(path)
        if parent == path:
            return False
        path = parent


def detect(env=None, target=None):
    """Return the client check result for env (defaults to os.environ)."""
    if env is None:
        env = os.environ
    entrypoint = env.get("CLAUDE_CODE_ENTRYPOINT", "")
    remote_viewer = bool(env.get("CLAUDE_CODE_BRIDGE_SESSION_ID")) or entrypoint.startswith("remote")

    if env.get("CLAUDECODE") == "1":
        client = "claude-code-" + (entrypoint or "unknown")
        reason = "CLAUDECODE=1; Claude Code surfaces show Mermaid source raw or are unverified"
    elif any(env.get(name) for name in CODEX_MARKERS):
        client = "codex"
        reason = "Codex marker set; Codex Mermaid rendering is unverified"
    elif env.get("GEMINI_CLI") == "1":
        client = "gemini-cli"
        reason = "GEMINI_CLI=1; Mermaid rendering is unverified"
    else:
        client = "unknown"
        reason = "no known client marker; use markdown table plus ASCII"

    if remote_viewer:
        reason += "; remote viewer attached, stay ASCII"

    return {
        "client": client,
        "mermaid": False,
        "remote_viewer": remote_viewer,
        "obsidian_vault": _is_obsidian_vault(os.getcwd() if target is None else target),
        "reason": reason,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--target", help="output path to check for an Obsidian vault "
                        "(default: the current working directory)")
    args = parser.parse_args(argv)
    json.dump(detect(target=args.target), sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
