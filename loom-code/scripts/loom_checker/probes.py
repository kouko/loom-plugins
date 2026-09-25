from __future__ import annotations

from fnmatch import fnmatch
from loom_checker.helpers import UsageError
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_maybe
from loom_checker.helpers import is_program_path
from loom_checker.helpers import kickoff_defaults
from loom_checker.helpers import tree_programs
from loom_checker.reviewers import committed_branch_delta
from pathlib import Path
from typing import Iterable
from repo_files import repository_files
import importlib.util
import os
import re
import shlex


TEST_COMMAND_MARKERS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("pyproject.toml", "pytest.ini", "tox.ini", "setup.cfg"), "python3 -m pytest -q"),
    (("package.json",), "npm test"),
    (("Cargo.toml",), "cargo test"),
    (("go.mod",), "go test ./..."),
)


_EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


_REGULAR_FILE_MODE = "100644"


NO_PACKAGE_TESTS = "none"


MAX_PROBE_PROGRAMS = 5


CONCERN_LINE = re.compile(
    r"^[^\S\n]*(?:#|//|--|\*)?[^\S\n]*concern:[^\S\n]*\S", re.IGNORECASE | re.MULTILINE
)


CONCERN_HEAD_LINES = 20


def probe_directory(change_id: str) -> str:
    """The one directory a change's probe programs are committed under."""
    return f"docs/loom/{change_id}/evidence/probes/"


SUITE_RUNNER = "scripts/run_package_tests.py"


PYTEST_FILE_PATTERNS = ("test_*.py", "*_test.py")


def _declared_suite_commands(repo: Path) -> list[list[str]]:
    """The commands the repository's own test runner declares it runs.

    Which programs the package suite covers is the repository's answer, not a
    list kept here: `scripts/run_package_tests.py` is the single inventory the
    declared package command drives, so it is read rather than mirrored. A
    repository without that runner declares nothing, and nothing is collected.
    """
    runner = repo / SUITE_RUNNER
    if not runner.is_file():
        return []
    spec = importlib.util.spec_from_file_location("_loom_suite_inventory", runner)
    if spec is None or spec.loader is None:
        return []
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return list(module.loom_family_commands(repo))
    except (OSError, AttributeError, ImportError, SyntaxError, TypeError, ValueError):
        return []


def _ignored(repo: Path, command: list[str], wanted: Path) -> bool:
    """True when one of the command's pytest `--ignore=` paths holds `wanted`."""
    for token in command[1:]:
        if not token.startswith("--ignore="):
            continue
        ignored = Path(token.partition("=")[2])
        ignored = (ignored if ignored.is_absolute() else repo / ignored).resolve()
        if wanted == ignored or ignored in wanted.parents:
            return True
    return False


def suite_collects(repo: Path, artifact: str) -> bool:
    """True when the declared package suite already runs `artifact`.

    A graduated probe program -- one carried out of a change's store into the
    permanent suite -- is named by a pytest path the runner declares, either
    as that path itself or as a file pytest collects under a declared
    directory. A neighbour the suite would never collect is not in the suite,
    and neither is a file under a folder the command passes to pytest as
    `--ignore=` -- that is how the runner skips every `tests/local/` folder,
    so the runner's own rule is honoured rather than restated here.
    """
    wanted = os.path.normpath(artifact)
    wanted_path = (repo / wanted).resolve()
    for command in _declared_suite_commands(repo):
        if not command:
            continue
        runs_pytest = "pytest" in command[:4]
        runs_shell = Path(command[0]).name in {"bash", "sh"}
        if not (runs_pytest or runs_shell):
            continue
        if runs_pytest and _ignored(repo, command, wanted_path):
            continue
        for token in command[1:]:
            if token.startswith("-") or token == "pytest":
                continue
            target = os.path.normpath(token)
            if not (repo / target).exists():
                continue
            if target == wanted:
                return True
            if not (runs_pytest and (repo / target).is_dir()):
                continue
            if wanted.startswith(target + os.sep) and any(
                fnmatch(Path(wanted).name, pattern) for pattern in PYTEST_FILE_PATTERNS
            ):
                return True
    return False


def committed_probe_programs(repo: Path, head_sha: str, change_id: str) -> list[str]:
    """Every program the selected commit holds under this change's store.

    Counting only `*.py`, and only under `evidence/probes/`, counted a subset
    of what the change commits and what `finalize-review` then executes: a
    shell program, or a Python program one directory up, escaped both the cap
    and the `concern:` line while still being run. What makes a file a program
    is `tree_programs`, the same question the delta-width rule asks, so an
    extension-less executable is counted here too.
    """
    prefix = f"docs/loom/{change_id}/"
    listing = git_maybe(repo, "ls-tree", "-r", "--name-only", head_sha, "--", prefix) or ""
    held = [line.strip() for line in listing.splitlines() if line.strip()]
    return sorted(tree_programs(repo, head_sha, held))


def _carries_concern(repo: Path, head_sha: str, path: str) -> bool:
    """True when the selected commit's copy of `path` states a concern."""
    text = git_maybe(repo, "show", f"{head_sha}:{path}") or ""
    head = "\n".join(text.splitlines()[:CONCERN_HEAD_LINES])
    return CONCERN_LINE.search(head) is not None


def _moved_paths(repo: Path, head_sha: str, removed: set[str]) -> set[str]:
    """Added paths git pairs as a rename of a path this branch removed.

    The shared branch delta reads with `--no-renames`, and the other rules
    keep that; the pairing is computed here only, over the same base, with
    `-M` at git's default similarity threshold of 50%
    (https://git-scm.com/docs/git-diff#Documentation/git-diff.txt--Mltngt).
    A file rewritten below that threshold is a removal plus a new file and
    stays counted. `-M` alone never reports copies, and the old path must be
    one the branch removed, so a probe copied under a new name while the
    original stays is counted too. When the pairing cannot be read, nothing
    is excluded -- the cap fails closed.
    """
    try:
        base = branch_base(repo)
    except UsageError:
        return set()
    status = git_maybe(repo, "diff", "--name-status", "-M", base, head_sha) or ""
    moved: set[str] = set()
    for line in status.splitlines():
        fields = line.split("\t")
        if len(fields) == 3 and fields[0].upper().startswith("R") and fields[1] in removed:
            moved.add(fields[2].strip())
    return moved


def graduated_probe_programs(repo: Path, head_sha: str, change_id: str) -> list[str]:
    """Probe programs this branch adds straight into the package suite.

    A probe that earned its place graduates: it leaves the change's store for
    a path the repository's own runner collects. Counting only the store
    therefore counted zero for exactly the change that produced the most
    programs, because the graduation gate empties that directory before
    finalize-review runs. These are counted with the store.

    What marks one of these files as the adversary's output rather than an
    ordinary new test is the `concern:` line the protocol requires a
    graduating probe to keep. A change that adds six ordinary test files adds
    no probe programs; a graduated probe that drops the line to duck the cap
    has stopped claiming to be a probe, and if finalize-review still executes
    it as one it is counted and answers for the line anyway.

    A test the branch only moved or renamed is not counted: it is an earlier
    change's probe, not this change's output, and counting it once refused a
    change that moved every test into `tests/` folders. See `_moved_paths`
    for how a move is told apart from a new or copied probe.
    """
    delta = committed_branch_delta(repo, change_id, head_sha)
    if delta is None:
        return []
    _paths, removed, added = delta
    moved = _moved_paths(repo, head_sha, removed)
    return sorted(
        path for path in added
        if path not in moved
        and is_program_path(path)
        and suite_collects(repo, path)
        and _carries_concern(repo, head_sha, path)
    )


def check_adversarial_proportionate(
    repo: Path, head_sha: str, change_id: str, artifacts: Iterable[str] = ()
) -> list[tuple[str, str]]:
    """Recompute the probe-program cap and the `concern:` line from the tree.

    The cap keeps the adversary's output proportionate to one change; the
    `concern:` line makes each program say what kind of defect it defends
    against, so a program that defends against nothing is visible.

    Both are recomputed over the union of three sets, because no one of them
    is the whole of what a change's adversarial step produced: the programs
    the selected commit holds under this change's store, the programs
    `finalize-review` is about to execute (``artifacts``), and the programs
    this branch graduates straight into the package suite. Reading the store
    alone made the cap unable to bind at all — graduation empties it first.

    A program the change commits somewhere else in its store is still refused
    rather than left uncounted; that check stays scoped to the store, since a
    graduated program's whole point is to live outside it.
    """
    rule = "adversarial.proportionate"
    stored = committed_probe_programs(repo, head_sha, change_id)
    expected = probe_directory(change_id)
    misplaced = [path for path in stored if not path.startswith(expected)]
    if misplaced:
        return [(rule, f"{misplaced[0]} is a program in this change's store outside "
                       f"{expected}, where the cap and the `concern:` line cannot "
                       f"see it; commit probe programs there")]
    counted = dict.fromkeys(stored)
    for path in graduated_probe_programs(repo, head_sha, change_id):
        counted[path] = None
    for artifact in artifacts:
        artifact = artifact.strip()
        if artifact:
            counted[artifact] = None
    programs = sorted(counted)
    if len(programs) > MAX_PROBE_PROGRAMS:
        return [(rule, f"{len(programs)} probe programs for this change "
                       f"(committed under its store, executed by finalize-review, "
                       f"or graduated into the package suite); at most "
                       f"{MAX_PROBE_PROGRAMS} are allowed")]
    for path in programs:
        if not _carries_concern(repo, head_sha, path):
            return [(rule, f"{path} carries no non-empty `concern:` line in its "
                           f"first {CONCERN_HEAD_LINES} lines")]
    return []


def missing_adversarial_execution(count: int, skip: set[str]) -> str | None:
    """The refusal reason when a change records no adversarial execution
    and the adversarial step was not skipped, else None.

    One predicate for both places that ask it -- finalize-review over its
    review input, and the attestation validator over the recorded
    executions -- so the two can never answer with different words.
    """
    if count < 1 and "adversarial" not in skip:
        return "at least one adversarial execution is required"
    return None


def command_names_artifact(command: str, artifact: str) -> bool:
    """True when one argument of `command` IS `artifact`.

    A substring test cannot tell `python3 attack0.py` from
    `python3 noop.py  # attack0.py`: both contain the path, only one runs
    it. The command is read the way a shell reads it -- a trailing `#`
    comment dropped, then split into arguments -- and the artifact has to
    be one of those arguments. `./x/y.py` and `x/y.py` name the same file
    and both count.
    """
    try:
        tokens = shlex.split(command, comments=True)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc
    wanted = os.path.normpath(artifact)
    return any(os.path.normpath(token) == wanted for token in tokens)


SHELL_METACHARACTERS = re.compile(r"[;&|<>()$`*?\[\]{}\n]")


PROBE_RUN_TIMEOUT = int(os.environ.get("LOOM_PROBE_RUN_TIMEOUT", "600"))


def argv_for(command: str) -> list[str]:
    """`command` as an argv list, or ValueError if a shell would be needed."""
    if SHELL_METACHARACTERS.search(command):
        raise ValueError(
            "it contains shell metacharacters; declare a plain argv command "
            "(a program and its arguments) instead"
        )
    tokens = shlex.split(command, comments=True)
    if not tokens:
        raise ValueError("it is empty")
    return tokens


def command_executes_artifact(command: str, artifact: str) -> bool:
    """True when argv directly executes the named Python, shell, or executable file."""
    tokens = argv_for(command)
    wanted = os.path.normpath(artifact)
    suffix = Path(artifact).suffix.lower()
    if suffix == ".py":
        # Handle direct python command or python -m pytest
        python = Path(tokens[0]).name.startswith("python")
        direct = len(tokens) >= 2 and os.path.normpath(tokens[1]) == wanted
        pytest_direct = (
            len(tokens) >= 4 and tokens[1:3] == ["-m", "pytest"]
            and os.path.normpath(tokens[3]) == wanted
        )
        # Handle uv run ... python ... or uv run ... python -m pytest ...
        uv_run_python = (
            len(tokens) >= 3
            and tokens[0] == "uv"
            and tokens[1] == "run"
        )
        if uv_run_python:
            # Find the python token after uv run options
            for i in range(2, len(tokens)):
                if Path(tokens[i]).name.startswith("python"):
                    python_tokens = tokens[i:]
                    python = True
                    direct = len(python_tokens) >= 2 and os.path.normpath(python_tokens[1]) == wanted
                    pytest_direct = (
                        len(python_tokens) >= 4 and python_tokens[1:3] == ["-m", "pytest"]
                        and os.path.normpath(python_tokens[3]) == wanted
                    )
                    if python and (direct or pytest_direct):
                        return True
                    break
        return python and (direct or pytest_direct)
    if suffix == ".sh":
        return len(tokens) >= 2 and Path(tokens[0]).name in {"bash", "sh"} and os.path.normpath(tokens[1]) == wanted
    return os.path.normpath(tokens[0]) in {wanted, os.path.join(".", wanted)}


def declared_test_command(repo: Path) -> tuple[str | None, str]:
    """The repo's own package-test command, and where it was read from.

    A recorded probe is compared against THIS, so that a command which
    exits 0 without running the suite cannot stand in for the suite. The
    repo's own KICKOFF-DEFAULTS line wins, because only the repo knows;
    otherwise the same markers the build station reads are read here.

    The test-file scan asks `repo_files.repository_files` which files are
    the repo's own: a walk of the directory also sees a linked worktree
    checked out inside it, or ignored build output, and would report a
    test command for a suite that is not this repository's."""
    declared = kickoff_defaults(repo).get("package-tests", "").strip()
    if declared:
        return declared, "docs/loom/KICKOFF-DEFAULTS.md"
    for markers, command in TEST_COMMAND_MARKERS:
        if any((repo / marker).is_file() for marker in markers):
            return command, f"detected {markers[0]}"
    names = [path.name for path in repository_files(repo)]
    for pattern in ("test_*.py", "*_test.py"):
        if any(fnmatch(name, pattern) for name in names):
            return "python3 -m pytest -q", f"detected {pattern} files"
    return None, ""
