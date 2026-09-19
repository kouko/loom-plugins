"""Mutation harness for the adversarial probes of 2026-09-19-loom-flow-recovery-loop.

Every mutating probe here extracts the committed tree with `git archive`,
edits the extracted copy, and runs the *committed* implementer probe program
unchanged inside that copy. Running the real program inside a copy of the tree
exercises its own assertions; a reimplementation of its logic would prove
nothing about it.

No discard command (`git checkout --`, `git restore`, `git reset --hard`,
`git clean`, `git worktree remove --force`) is used: the throwaway tree is a
`git archive` extract in a temp directory, so nothing in the working tree is
ever at risk.
"""

import os
import subprocess
import sys
import tarfile
import tempfile

REPO = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    capture_output=True,
    text=True,
    check=True,
).stdout.strip()

BUILD_SKILL = "loom-code/skills/build/SKILL.md"
CR_SKILL = "loom-code/skills/closing-review/SKILL.md"
BUILD_PROBES = "loom-code/skills/build/probes/test_recovery_rules.py"
CR_PROBES = "loom-code/skills/closing-review/probes/test_recovery_rules.py"


def extract(ref="HEAD"):
    """Extract the committed tree into a fresh temp directory and return it."""
    tmp = tempfile.mkdtemp(prefix="adv-recovery-")
    archive = os.path.join(tmp, "tree.tar")
    with open(archive, "wb") as fh:
        subprocess.run(["git", "archive", ref], cwd=REPO, stdout=fh, check=True)
    root = os.path.join(tmp, "tree")
    os.makedirs(root)
    with tarfile.open(archive) as tar:
        tar.extractall(root)
    os.remove(archive)
    return root


def read(root, relpath):
    with open(os.path.join(root, relpath), "r", encoding="utf-8") as fh:
        return fh.read()


def write(root, relpath, text):
    with open(os.path.join(root, relpath), "w", encoding="utf-8") as fh:
        fh.write(text)


def mutate(root, relpath, old, new):
    """Replace `old` with `new` exactly once. Raises if it does not match once."""
    text = read(root, relpath)
    hits = text.count(old)
    if hits != 1:
        raise AssertionError(
            f"mutation anchor occurs {hits} times in {relpath}, expected 1: {old!r}"
        )
    write(root, relpath, text.replace(old, new))


def run_probes(root, relpath):
    """Run a committed probe program unchanged inside the extracted copy.

    Returns (exit_code, combined_output). The probe programs open their target
    by a repo-relative path, so cwd is the extracted root.
    """
    proc = subprocess.run(
        [sys.executable, relpath],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def report(probe, verdict, detail):
    """Print one probe result. `verdict` is BROKE, HELD or FINDING."""
    print(f"{probe} {verdict}: {detail}")


def expect(probe, observed, recorded, detail):
    """Assert the behaviour the adversary recorded is still what happens.

    These programs are re-runnable evidence, not gates on the product. Exit 0
    means "the recorded observation reproduces". Exit 1 means the behaviour
    changed since the adversary ran — read the line, then update the record.
    """
    if observed == recorded:
        print(f"{probe} REPRODUCED: {detail}")
        sys.exit(0)
    print(f"{probe} CHANGED: expected {recorded!r}, observed {observed!r} — {detail}")
    sys.exit(1)
