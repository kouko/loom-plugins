#!/usr/bin/env python3
"""Run one pytest session per `--then`-separated group of arguments.

loom-design/scripts/ carries its own pytest.ini (importlib import mode); a
single session that also names loom-code paths adopts that ini, and the
loom-code modules that rely on bare sibling imports (three files, ~90
tests) fail to collect. Two sessions, one exit code.

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


def split_groups(argv: list[str]) -> list[list[str]]:
    groups: list[list[str]] = [[]]
    for token in argv:
        if token == "--then":
            groups.append([])
        else:
            groups[-1].append(token)
    return [g for g in groups if g]


def loom_family_commands(
    repo: Path, verbosity: str = "-q", only: str | None = None
) -> list[list[str]]:
    """Return the complete Loom test surface as isolated commands."""
    commands: list[list[str]] = []
    if only in {None, "code"}:
        commands.append([sys.executable, "-m", "pytest", "loom-code/scripts/", "scripts/", ".claude/hooks/", verbosity, "-n", "auto"])
    if only in {None, "design"}:
        commands.append([sys.executable, "-m", "pytest", "loom-design/scripts/", verbosity])
    if only in {None, "workflow-python"}:
        commands.extend([
            [sys.executable, "-m", "pytest", "loom-workflow/tests/test_loom_visualization_page_scripts.py", verbosity],
            [sys.executable, "-m", "pytest", "loom-workflow/scripts", verbosity],
        ])
        for scripts_dir in sorted((repo / "loom-workflow/skills").glob("*/scripts")):
            if any(scripts_dir.glob("test_*.py")):
                commands.append([sys.executable, "-m", "pytest", scripts_dir.as_posix(), verbosity])
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
        if command[:3] == [sys.executable, "-m", "pytest"]:
            command.extend(ignores)
    return commands


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--loom-family":
        verbosity = "-v" if "-v" in argv[1:] else "-q"
        if "--only" in argv and argv.index("--only") + 1 >= len(argv):
            print("run_package_tests: --only needs a group", file=sys.stderr)
            return 2
        only = argv[argv.index("--only") + 1] if "--only" in argv else None
        if only not in {None, "code", "design", "workflow-python", "workflow-shell", "workflow-mermaid"}:
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
