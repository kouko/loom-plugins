"""Adversarial probe: no changed file names a codex-tools.md that does not exist.

Any mention of codex-tools.md in the changed files must resolve (relative to
the file, the repository root, or the plugin root), and the distill-sessions
file must not attribute a codex-tools.md to loom-code, which has none.
Run from the repository root: python3 <this file>. Exit 1 on failure.
"""
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
FILES = ["docs/loom/README.md",
         "loom-code/docs/examples/README.md",
         "loom-workflow/skills/distill-sessions/references/codex-tools.md"]
TOKEN = re.compile(r"[\w./-]*codex-tools\.md")
SELF_HEADER = re.compile(r"^#")


def resolves(path, token):
    rel = Path(path)
    candidates = [ROOT / rel.parent / token, ROOT / token, ROOT / rel.parts[0] / token]
    return any(c.resolve().is_file() for c in candidates)


def problems():
    found = []
    for rel in FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for number, para in enumerate(re.split(r"\n\s*>?\s*\n", text), 1):
            if "codex-tools" in para and "loom-code" in para:
                found.append(f"{rel} paragraph {number} attributes codex-tools to loom-code")
        for number, line in enumerate(text.splitlines(), 1):
            if SELF_HEADER.match(line):
                continue
            if "codex-tools" in line and "loom-code" in line:
                found.append(f"{rel}:{number} attributes codex-tools to loom-code")
            for token in TOKEN.findall(line):
                if not resolves(rel, token):
                    found.append(f"{rel}:{number} names missing {token}")
    return found


def test_changed_files_codex_tools_mentions_all_resolve():
    """No changed file points at a nonexistent codex-tools.md."""
    found = problems()
    assert not found, found


if __name__ == "__main__":
    try:
        test_changed_files_codex_tools_mentions_all_resolve()
    except AssertionError as exc:
        print("RED:", exc)
        sys.exit(1)
    print("GREEN")
