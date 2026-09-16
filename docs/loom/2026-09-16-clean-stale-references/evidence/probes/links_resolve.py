"""Adversarial probe: every relative link in the changed prose resolves on disk.

Scope: the frozen-store section of docs/loom/README.md, and the whole of
loom-code/docs/examples/README.md and the distill-sessions codex-tools.md.
Run from the repository root: python3 <this file>. Exit 1 on any dead link.
"""
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
LINK = re.compile(r"\]\(([^)\s]+)\)")


def frozen_section(text):
    start = text.index("These are the pre-1.0 stores.")
    end = text.index("\n## ", start)
    return text[start:end]


def targets():
    readme = ROOT / "docs/loom/README.md"
    yield readme, frozen_section(readme.read_text(encoding="utf-8"))
    for rel in ("loom-code/docs/examples/README.md",
                "loom-workflow/skills/distill-sessions/references/codex-tools.md"):
        path = ROOT / rel
        yield path, path.read_text(encoding="utf-8")


def dead_links(path, text):
    dead = []
    for href in LINK.findall(text):
        if re.match(r"^[a-z]+:", href) or href.startswith("#"):
            continue
        target = (path.parent / href.split("#")[0]).resolve()
        if not target.exists():
            dead.append(href)
    return dead


def test_changed_prose_relative_links_all_exist():
    """Every relative link in the changed prose points at an existing path."""
    failures = [(str(p.relative_to(ROOT)), h) for p, t in targets() for h in dead_links(p, t)]
    assert not failures, failures


if __name__ == "__main__":
    try:
        test_changed_prose_relative_links_all_exist()
    except AssertionError as exc:
        print("RED dead links:", exc)
        sys.exit(1)
    print("GREEN")
