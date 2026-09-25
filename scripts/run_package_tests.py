#!/usr/bin/env python3
"""Run one pytest session per `--then`-separated group of arguments.

`--loom-family [--only <group>]` runs the whole Loom test surface instead. Tests
live in `tests/` folders apart from the code they test, and the inventory is
discovered rather than listed: any pytest file placed in one of those folders
runs without editing this file, and a `tests/local/` folder -- tests that only
make sense on a developer's machine -- is skipped. The groups, which CI selects
with `--only`, are:

- `code`: the repository-level `tests/` and `loom-code/tests/`, one xdist session.
- `design`: `loom-design/tests/`, its own session, because loom-design carries
  its own pytest.ini (importlib import mode); a single session that also names
  loom-code paths adopts that ini, and the loom-code modules that rely on bare
  sibling imports fail to collect.
- `workflow-python`: `loom-workflow/tests/`, one session for its top level and
  one per subfolder that holds tests, because per-skill subfolders repeat test
  basenames and carry their own conftest.py or pytest.ini.
- `workflow-shell`: every `loom-workflow/tests/test-*.sh`.
- `workflow-mermaid`: the Mermaid validator and its negative check.

A plugin whose tests have not moved into its `tests/` folder yet is still run
from where they are (`LEGACY_*` below); an entry goes when its tests move, and a
folder that no longer holds tests is dropped on its own.

Whole directories are handed to pytest, and a nested git repository placed
inside one of them -- a linked worktree, a clone dropped in `vendor/`, a
submodule -- would have its test files collected and run as this repository's.
Every pytest session therefore carries `--ignore=<path>` for each such subtree.
The exclusions are the union of `repo_files.nested_repositories` (the opaque
directory entries git collapsed, which is the same answer the scanners use for
"not ours") and `repo_files.nested_worktrees` (which still sees a worktree that
a `.gitignore` hides from the first). A repository-root `pytest.ini` would also apply to a bare
`pytest` run at the root, which is known to abort on dbt-wiki collection, so
the exclusion is passed per command instead. Where the worktrees are is a git
question, and git questions live in `loom-code/scripts/repo_files.py`, imported
via sys.path the way `loom-design/scripts/spec/test_write_spec_contract.py`
reaches across trees.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "loom-code" / "scripts"))

from repo_files import nested_repositories, nested_worktrees  # noqa: E402

LOCAL = "local"
LEGACY_CODE = ("loom-code/scripts",)
LEGACY_DESIGN = ("loom-design/scripts",)
LEGACY_WORKFLOW = ("loom-workflow/scripts", "loom-workflow/skills/*/scripts")
GROUPS = {"code", "design", "workflow-python", "workflow-shell", "workflow-mermaid"}


def split_groups(argv: list[str]) -> list[list[str]]:
    groups: list[list[str]] = [[]]
    for token in argv:
        if token == "--then":
            groups.append([])
        else:
            groups[-1].append(token)
    return [g for g in groups if g]


def _holds_tests(folder: Path, skip: tuple[Path, ...] = ()) -> bool:
    """True when pytest would find a test file under `folder` outside `skip`."""
    return folder.is_dir() and any(
        "node_modules" not in path.parts and not any(s in path.parents for s in skip)
        for path in folder.rglob("test_*.py")
    )


def _legacy(repo: Path, patterns: tuple[str, ...]) -> list[Path]:
    return [f for p in patterns for f in sorted(repo.glob(p)) if _holds_tests(f)]


def _tests_session(repo: Path, folders: list[Path]) -> list[str]:
    """Targets and `tests/local/` ignores for the folders that hold tests."""
    targets, ignores = [], []
    for folder in folders:
        local = folder / LOCAL
        if _holds_tests(folder, (local,)):
            targets.append(folder.relative_to(repo).as_posix())
            if local.exists():
                ignores.append(f"--ignore={local.resolve()}")
    return [*targets, *ignores] if targets else []


def _workflow_sessions(repo: Path) -> list[list[str]]:
    tests = repo / "loom-workflow" / "tests"
    local = tests / LOCAL
    subfolders = sorted(
        d for d in tests.iterdir()
        if d.is_dir() and d != local and d.name != "node_modules"
        and not d.name.startswith((".", "_")) and _holds_tests(d)
    ) if tests.is_dir() else []
    sessions = []
    if _holds_tests(tests, (local, *subfolders)):
        sessions.append([
            tests.relative_to(repo).as_posix(),
            *(f"--ignore={p.resolve()}" for p in (local, *subfolders) if p.exists()),
        ])
    sessions += [[d.relative_to(repo).as_posix()] for d in subfolders]
    sessions += [[d.relative_to(repo).as_posix()] for d in _legacy(repo, LEGACY_WORKFLOW)]
    return sessions


def loom_family_commands(
    repo: Path, verbosity: str = "-q", only: str | None = None
) -> list[list[str]]:
    """Return the complete Loom test surface as isolated commands."""
    pytest = [sys.executable, "-m", "pytest"]
    sessions: list[list[str]] = []
    commands: list[list[str]] = []
    if only in {None, "code"}:
        code = _tests_session(repo, [repo / "tests", repo / "loom-code" / "tests"])
        legacy = [f.relative_to(repo).as_posix() for f in _legacy(repo, LEGACY_CODE)]
        if code or legacy:
            commands.append([*pytest, *legacy, *code, verbosity, "-n", "auto"])
    if only in {None, "design"}:
        sessions += [s for s in [_tests_session(repo, [repo / "loom-design" / "tests"])] if s]
        sessions += [[f.relative_to(repo).as_posix()] for f in _legacy(repo, LEGACY_DESIGN)]
    if only in {None, "workflow-python"}:
        sessions += _workflow_sessions(repo)
    commands += [[*pytest, *session, verbosity] for session in sessions]
    if only in {None, "workflow-shell"}:
        commands.extend(
            [["bash", test.as_posix()]
             for test in sorted((repo / "loom-workflow/tests").glob("test-*.sh"))]
        )
    if only in {None, "workflow-mermaid"}:
        # No skip path: a missing node or npm fails the group.
        commands.extend([
            ["npm", "ci", "--prefix", "loom-workflow/tests/mermaid"],
            ["node", "loom-workflow/tests/mermaid/validate_mermaid.mjs"],
            ["bash", "loom-workflow/tests/mermaid-validator-negative.sh"],
        ])
    foreign = sorted({*nested_repositories(repo), *nested_worktrees(repo)})
    ignores = [f"--ignore={path.resolve()}" for path in foreign]
    for command in commands:
        if command[:3] == pytest:
            command.extend(ignores)
    return commands


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--loom-family":
        verbosity = "-v" if "-v" in argv[1:] else "-q"
        if "--only" in argv and argv.index("--only") + 1 >= len(argv):
            print("run_package_tests: --only needs a group", file=sys.stderr)
            return 2
        only = argv[argv.index("--only") + 1] if "--only" in argv else None
        if only is not None and only not in GROUPS:
            print(f"run_package_tests: unknown Loom group {only!r}", file=sys.stderr)
            return 2
        for command in loom_family_commands(Path.cwd(), verbosity, only):
            code = subprocess.call(command)
            if code != 0:
                return code
        return 0
    groups = split_groups(argv)
    if not groups:
        print("run_package_tests: no path group given", file=sys.stderr)
        return 2
    for group in groups:
        code = subprocess.call([sys.executable, "-m", "pytest", *group])
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
