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
import json
import os
import re
import shlex
import subprocess
import tempfile


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


# pytest loads -p plugins before collection, and this hook sees session.items
# after selection: https://docs.pytest.org/en/stable/how-to/writing_plugins.html
# https://docs.pytest.org/en/stable/reference/reference.html
PYTEST_COLLECTION_PLUGIN = '''import json
import os
from pathlib import Path

def pytest_collection_finish(session):
    Path(os.environ["LOOM_PYTEST_COLLECTION"]).write_text(
        json.dumps([str(item.path) for item in session.items]), encoding="utf-8"
    )
'''


def _runner_launcher(repo: Path) -> list[str] | None:
    """Python launcher used by a declared package command for this runner."""
    declared, _source = declared_test_command(repo)
    try:
        tokens = argv_for(declared) if declared else []
    except ValueError:
        return None
    runner = SUITE_RUNNER
    if _conda_python_argv(tokens) and len(tokens) > 5 and os.path.normpath(tokens[5]) == runner:
        return tokens[:5]
    if len(tokens) > 1 and Path(tokens[0]).name.startswith("python") and os.path.normpath(tokens[1]) == runner:
        return tokens[:1]
    if tokens[:2] == ["uv", "run"]:
        index = 2
        while index < len(tokens):
            if tokens[index] in {"--isolated", "--no-project", "--offline"}:
                index += 1
            elif tokens[index] in {"--with-requirements", "--with"} and index + 1 < len(tokens):
                index += 2
            else:
                break
        if (index + 1 < len(tokens) and Path(tokens[index]).name.startswith("python")
                and os.path.normpath(tokens[index + 1]) == runner):
            return tokens[:index + 1]
    return None


def _declared_suite_commands(repo: Path) -> tuple[list[list[str]] | None, str, list[str] | None]:
    """The commands the repository's own test runner declares it runs."""
    runner = repo / SUITE_RUNNER
    if not runner.is_file():
        return [], "", None
    launcher = _runner_launcher(repo)
    declared, _source = declared_test_command(repo)
    if declared and SUITE_RUNNER in declared and launcher is None:
        return None, "unsupported package-tests runner launcher", None
    if launcher:
        code = (
            "import importlib.util,json,os,sys; from pathlib import Path; "
            "path=Path(sys.argv[1]); repo=Path(sys.argv[2]); "
            "sys.path.insert(0,str(path.parent)); "
            "spec=importlib.util.spec_from_file_location('_loom_suite_inventory',path); "
            "module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); "
            "Path(os.environ['LOOM_SUITE_INVENTORY']).write_text("
            "json.dumps(module.loom_family_commands(repo)),encoding='utf-8')"
        )
        try:
            with tempfile.TemporaryDirectory(prefix="loom-suite-inventory-") as directory:
                output = Path(directory) / "commands.json"
                env = dict(os.environ, LOOM_SUITE_INVENTORY=str(output))
                result = subprocess.run(
                    [*launcher, "-c", code, str(runner), str(repo)], cwd=repo,
                    env=env, capture_output=True, text=True, timeout=60,
                )
                if result.returncode != 0:
                    return None, _collection_error(result.stderr), launcher
                commands = json.loads(output.read_text(encoding="utf-8"))
                if not isinstance(commands, list) or not all(
                    isinstance(command, list) and all(isinstance(token, str) for token in command)
                    for command in commands
                ):
                    return None, "runner inventory is malformed", launcher
                return commands, "", launcher
        except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
            return None, str(exc), launcher
    spec = importlib.util.spec_from_file_location("_loom_suite_inventory", runner)
    if spec is None or spec.loader is None:
        return None, "runner inventory could not be loaded", None
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return list(module.loom_family_commands(repo)), "", None
    except (OSError, AttributeError, ImportError, SyntaxError, TypeError, ValueError) as exc:
        return None, str(exc), None


def _collection_error(stderr: str) -> str:
    return " ".join(stderr.strip().splitlines()[-4:])[-500:] or "pytest exited without collection"


def _direct_pytest_collects(repo: Path, artifact: str) -> tuple[bool | None, str]:
    """Ask a direct package pytest command which tests it actually collects."""
    declared, _source = declared_test_command(repo)
    if not declared:
        return False, ""
    try:
        tokens = argv_for(declared)
    except ValueError:
        return False, ""
    if _conda_pytest_argv(tokens):
        pytest_command = tokens[:7]
        args = tokens[7:]
    elif tokens[0] == "pytest":
        pytest_command = tokens[:1]
        args = tokens[1:]
    elif (len(tokens) >= 3 and Path(tokens[0]).name.startswith("python")
          and tokens[1:3] == ["-m", "pytest"]):
        pytest_command = tokens[:3]
        args = tokens[3:]
    else:
        return False, ""
    if pytest_positionals(args) is None:
        return False, ""
    return _pytest_collects(repo, artifact, pytest_command, args)


def _pytest_collects(repo: Path, artifact: str, command: list[str], args: list[str]) -> tuple[bool | None, str]:
    """Check actual pytest collection under the repository's configuration."""
    # Worker count changes collection cost, not which files pytest selects.
    args = [arg for index, arg in enumerate(args)
            if arg not in {"-n", "--numprocesses"} and
            (index == 0 or args[index - 1] not in {"-n", "--numprocesses"})]
    try:
        with tempfile.TemporaryDirectory(prefix="loom-pytest-collect-") as directory:
            scratch = Path(directory)
            (scratch / "_loom_pytest_collection.py").write_text(
                PYTEST_COLLECTION_PLUGIN, encoding="utf-8"
            )
            output = scratch / "collected.json"
            env = dict(os.environ)
            env["PYTHONPATH"] = directory + os.pathsep + env.get("PYTHONPATH", "")
            env["LOOM_PYTEST_COLLECTION"] = str(output)
            result = subprocess.run(
                [*command, *args, "--collect-only", "-p", "_loom_pytest_collection"],
                cwd=repo, env=env, capture_output=True, text=True, timeout=60,
            )
            # Current conda CLI returns the child response.rc; do not infer a
            # cross-platform guarantee: https://github.com/conda/conda/blob/main/conda/cli/main_run.py
            if result.returncode != 0:
                return None, _collection_error(result.stderr)
            collected = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return None, str(exc)
    if not isinstance(collected, list) or not all(isinstance(path, str) for path in collected):
        return None, "pytest collection output is malformed"
    wanted = (repo / artifact).resolve()
    return any(Path(path).resolve() == wanted for path in collected), ""


def suite_collects(repo: Path, artifact: str) -> bool:
    return suite_collection(repo, artifact)[0] is True


def suite_collection(repo: Path, artifact: str) -> tuple[bool | None, str]:
    """Whether the declared suite collects `artifact`, or cannot determine it.

    A graduated probe program -- one carried out of a change's store into the
    permanent suite -- is collected by the direct or runner-backed pytest
    command, or named by a shell test the repository's runner declares. A
    neighbour the suite would never collect is not in the suite.

    Known limitation (user-decided 2026-09-25): a committed symlink into an
    ignored folder makes pytest collect its files again, and they go uncounted.
    """
    wanted = os.path.normpath(artifact)
    wanted_path = (repo / wanted).resolve()
    if not (repo / SUITE_RUNNER).is_file():
        return _direct_pytest_collects(repo, artifact)
    commands, error, launcher = _declared_suite_commands(repo)
    if commands is None:
        return None, error
    unavailable = ""
    for command in commands:
        if not command:
            continue
        runs_pytest = "pytest" in command[:4]
        runs_shell = Path(command[0]).name in {"bash", "sh"}
        if not (runs_pytest or runs_shell):
            continue
        for token in command[1:]:
            if token.startswith("-") or token == "pytest":
                continue
            target = os.path.normpath(token)
            if not (repo / target).exists():
                continue
            if target == wanted:
                if runs_shell:
                    return True, ""
                break
            if not (runs_pytest and (repo / target).is_dir()):
                continue
            if (repo / target).resolve() in wanted_path.parents and any(
                fnmatch(Path(wanted).name, pattern) for pattern in PYTEST_FILE_PATTERNS
            ):
                break
        else:
            continue
        if runs_pytest:
            prefix = 3 if len(command) >= 3 and command[1:3] == ["-m", "pytest"] else 1
            pytest_command = command[:prefix]
            args = command[prefix:]
            if launcher:
                if prefix == 3 or Path(command[0]).name == "pytest":
                    pytest_command = [*launcher, "-m", "pytest"]
                else:
                    return None, "unsupported runner pytest command"
            collected, reason = _pytest_collects(repo, artifact, pytest_command, args)
            if collected is True:
                return True, ""
            if collected is None:
                unavailable = reason
    return (None, unavailable) if unavailable else (False, "")


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
    original stays is counted too. The old path must also have carried a
    `concern:` line at the branch base: a pair whose source was never a probe
    is a new probe written over a plain test, and is counted. `-l0` pins the
    exhaustive pairing to unlimited ("a value of 0 is treated as unlimited",
    https://git-scm.com/docs/git-diff#Documentation/git-diff.txt--lltnumgt),
    so a local `diff.renameLimit` cannot turn moves into new files and the
    count is the same on every machine. When the pairing cannot be read,
    nothing is excluded -- the cap fails closed.
    """
    try:
        base = branch_base(repo)
    except UsageError:
        return set()
    status = git_maybe(repo, "diff", "--name-status", "-M", "-l0", base, head_sha) or ""
    moved: set[str] = set()
    for line in status.splitlines():
        fields = line.split("\t")
        if (
            len(fields) == 3
            and fields[0].upper().startswith("R")
            and fields[1] in removed
            and _carries_concern(repo, base, fields[1])
        ):
            moved.add(fields[2].strip())
    return moved


def graduated_probe_programs(repo: Path, head_sha: str, change_id: str) -> list[str]:
    """Probe programs this branch adds straight into the package suite.

    A probe that earned its place graduates: it leaves the change's store for
    a path the repository's own runner collects or cannot currently verify.
    Counting only the store
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
        and suite_collection(repo, path)[0] is not False
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


PYTEST_VALUE_OPTIONS = frozenset({
    "-p", "-k", "-m", "-o", "-c", "-W", "-r", "--deselect", "--ignore",
    "--ignore-glob", "--rootdir", "--confcutdir", "--basetemp", "--tb",
    "--maxfail", "--keyword", "--override-ini", "--config-file",
    "--pythonwarnings",
})
PYTEST_FLAGS = frozenset({
    "--quiet", "--verbose", "--exitfirst", "--no-header", "--strict-markers",
})
PYTEST_SHORT_FLAG_CLUSTER = re.compile(r"-[qvxsl]+")


def pytest_positionals(args: list[str]) -> list[str] | None:
    """The positional arguments of a pytest argv, or None when any option is
    not on the allowlist -- fail-closed, since an unlisted option may run no
    tests (`--help`, `--collect-only`) or take the artifact as its value."""
    positionals, rest = [], list(args)
    while rest:
        arg = rest.pop(0)
        if not arg.startswith("-"):
            positionals.append(arg)
        elif arg in PYTEST_VALUE_OPTIONS:
            if not rest:
                return None
            rest.pop(0)
        elif arg in PYTEST_FLAGS or PYTEST_SHORT_FLAG_CLUSTER.fullmatch(arg):
            continue
        elif arg.startswith("--") and arg.split("=", 1)[0] in PYTEST_VALUE_OPTIONS and "=" in arg:
            continue
        elif not arg.startswith("--") and arg[:2] in PYTEST_VALUE_OPTIONS and len(arg) > 2:
            continue
        else:
            return None
    return positionals


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


def _conda_python_argv(tokens: list[str]) -> bool:
    # -n selects the environment; the following executable and arguments run
    # there: https://docs.conda.io/projects/conda/en/stable/commands/run.html
    return (len(tokens) >= 5 and Path(tokens[0]).name == "conda"
            and tokens[1:3] == ["run", "-n"]
            and bool(tokens[3]) and not tokens[3].startswith("-")
            and Path(tokens[4]).name.startswith("python"))


def _conda_pytest_argv(tokens: list[str]) -> bool:
    """Recognize only `conda run -n ENV python -m pytest ...`."""
    return _conda_python_argv(tokens) and tokens[5:7] == ["-m", "pytest"]


def command_executes_artifact(command: str, artifact: str) -> bool:
    """True when argv directly executes the named Python, shell, or executable file."""
    tokens = argv_for(command)
    wanted = os.path.normpath(artifact)
    suffix = Path(artifact).suffix.lower()
    if suffix == ".py":
        if _conda_pytest_argv(tokens):
            tokens = tokens[4:]
        # `uv run [opts] python ...` is checked as the python argv it wraps.
        if tokens[:2] == ["uv", "run"]:
            tokens = next((tokens[i:] for i in range(2, len(tokens))
                           if Path(tokens[i]).name.startswith("python")), [""])
        args = tokens[1:]
        # `python -m pytest ... X ...`: every option, in any position, must be
        # on the allowlist, and the first positional argument must be X.
        if args[:2] == ["-m", "pytest"]:
            args = pytest_positionals(args[2:]) or []
        return (Path(tokens[0]).name.startswith("python") and bool(args)
                and os.path.normpath(args[0]) == wanted)
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
