"""Mutation probe: are moved obligations still pinned as strongly as on base?

Change 2026-09-16-loom-rule-text-consolidation moved rule sentences between
files. For each obligation this program removes or weakens the sentence in a
throwaway tree (a `git archive` extract), runs every package test that names
the mutated file, records whether any test turns RED, and restores the file.
The same mutation is applied to the base tree at the sentence's base location,
so a mutant killed on base but surviving on the branch is a weakened pin.

Usage (from the repository root):
  python3 docs/loom/2026-09-16-loom-rule-text-consolidation/evidence/probes/moved_pin_mutation.py
It adds detached worktrees for HEAD and the base commit under a fresh
temporary directory and removes them with plain `git worktree remove`.
Exit 1 when a control run is red or any mutant survives on head that base
killed.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import sys
from pathlib import Path

LENSES = "loom-code/skills/closing-review/references/lenses.md"
ADVERSARIAL = "loom-code/skills/closing-review/references/adversarial.md"
ADVERSARY = "loom-code/agents/adversary.md"
REVIEWER = "loom-code/agents/reviewer.md"
WRITE_PLAN = "loom-code/skills/write-plan/SKILL.md"

DISCARD_HEAD = ("Discard commands\n(`git checkout --`, `git restore`, `git reset --hard`, `git clean`,\n"
                "`git worktree remove --force`) are never used to undo a mutation, because host\n"
                "guards refuse them and they can destroy uncommitted work. ")
DISCARD_BASE = ("Discard commands (`git checkout --`, `git restore`,\n`git reset --hard`, `git clean`, "
                "`git worktree remove --force`) are never used\nto undo a mutation, because host guards "
                "refuse them and they can destroy\nuncommitted work.")

# name -> (head edits, base edits); an edit is (path, old, new).
MUTANTS = {
    "suite-ban-scoped-to-round-1": (
        [(LENSES, "In every round, reviewers never run", "In round 1, reviewers never run")],
        [(REVIEWER, "In every round, you never run", "In round 1, you never run")],
    ),
    "skipped-changed-test-no-longer-a-finding": (
        [(LENSES, " and a test in a changed test file the reviewer ran that is skipped or never actually "
                  "executes is a finding, since a green exit code does not show that it ran;", "")],
        [(REVIEWER, " — a test\nin a changed test file you ran that is skipped, or that never actually "
                    "executes, is a `tests`\nfinding, since a green exit code does not show that it ran.", ".")],
    ),
    "discard-command-ban-deleted": (
        [(ADVERSARIAL, DISCARD_HEAD, "")],
        [(ADVERSARY, DISCARD_BASE, ""), (ADVERSARIAL, None, None)],
    ),
    "discard-command-ban-softened": (
        [(ADVERSARIAL, "are never used to undo a mutation", "are rarely used to undo a mutation")],
        [(ADVERSARY, "are never used\nto undo a mutation", "are rarely used\nto undo a mutation")],
    ),
    "code-change-to-fail-is-not-a-case-deleted": (
        [(ADVERSARIAL, " If a case\nneeds the code changed to fail, it is not a case.", "")],
        [(ADVERSARY, " If a case needs the code\n  changed to fail, it is not a case.", "")],
    ),
    "three-is-floor-deleted": (
        [(ADVERSARIAL, " Three is the floor, not the target.", "")],
        [(ADVERSARY, "- **Stopping at three.** Three is the floor for a change with no tooling,\n"
                     "  not a quota to fill and leave.\n", "")],
    ),
    "confirm-on-users-behalf-allowed": (
        [(WRITE_PLAN, " and you do not confirm on the user's behalf", "")],
        [(WRITE_PLAN, " and you do not confirm on the user's behalf", "")],
    ),
}


def _tests_naming(tree: Path, path: str) -> list[str]:
    name = Path(path).name
    stem = Path(path).parent.name if name == "SKILL.md" else name
    found = []
    for test in sorted(tree.glob("loom-*/scripts/**/test_*.py")):
        if not test.is_file():
            continue  # a dangling symlink in an archive extract collects as an error
        text = test.read_text(encoding="utf-8", errors="ignore")
        if stem in text:
            found.append(str(test.relative_to(tree)))
    return found


def _run(tree: Path, edits) -> tuple[str, list[str]]:
    edits = [e for e in edits if e[1] is not None]
    saved = {}
    for path, old, new in edits:
        file = tree / path
        text = saved.setdefault(path, file.read_text(encoding="utf-8"))
        current = file.read_text(encoding="utf-8")
        if current.count(old) != 1:
            for p, t in saved.items():
                (tree / p).write_text(t, encoding="utf-8")
            return f"ANCHOR-COUNT-{current.count(old)}", []
        file.write_text(current.replace(old, new), encoding="utf-8")
    tests = sorted({t for path, _, _ in edits for t in _tests_naming(tree, path)})
    try:
        # One process per file: loom-code and loom-design test trees
        # collide when collected together.
        red = [t for t in tests
               if subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", t],
                                 cwd=tree, capture_output=True, text=True).returncode]
        verdict = f"KILLED({','.join(Path(t).name for t in red)})" if red else "SURVIVED"
    finally:
        for p, t in saved.items():
            (tree / p).write_text(t, encoding="utf-8")
    return verdict, tests


BASE_COMMIT = "dec4e927"
REPO = Path(__file__).resolve().parents[5]


def main() -> int:
    if len(sys.argv) == 3:
        return _compare(Path(sys.argv[1]), Path(sys.argv[2]))
    tmp = Path(tempfile.mkdtemp(prefix="moved-pin-mutation-"))
    head, base = tmp / "head", tmp / "base"
    added = []
    try:
        for tree, rev in ((head, "HEAD"), (base, BASE_COMMIT)):
            subprocess.run(["git", "-C", str(REPO), "worktree", "add", "--detach", str(tree), rev],
                           check=True, capture_output=True, text=True)
            added.append(tree)
        return _compare(head, base)
    finally:
        # Every mutation is restored inside _run, so a plain remove succeeds.
        for tree in added:
            subprocess.run(["git", "-C", str(REPO), "worktree", "remove", str(tree)], check=True)
        os.rmdir(tmp)


def _compare(head: Path, base: Path) -> int:
    weakened = 0
    for name, (head_edits, base_edits) in MUTANTS.items():
        # Control: the same test set on the unmutated tree must pass, or a
        # KILLED verdict proves nothing.
        hc, _ = _run(head, [(p, o, o) for p, o, _ in head_edits if o is not None])
        bc, _ = _run(base, [(p, o, o) for p, o, _ in base_edits if o is not None])
        if hc != "SURVIVED" or bc != "SURVIVED":
            print(f"{name}: CONTROL-RED head={hc} base={bc}")
            weakened += 1
            continue
        hv, _ = _run(head, head_edits)
        bv, _ = _run(base, base_edits)
        flag = "WEAKENED" if (bv.startswith("KILLED") and not hv.startswith("KILLED")) else ""
        weakened += bool(flag)
        print(f"{name}: head={hv} base={bv} {flag}")
    return 1 if weakened else 0


if __name__ == "__main__":
    sys.exit(main())
