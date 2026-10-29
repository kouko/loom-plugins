from __future__ import annotations

from fnmatch import fnmatch
from loom_checker.helpers import UsageError
from loom_checker.helpers import branch_base
from loom_checker.helpers import git_maybe
from loom_checker.helpers import is_program_path
from loom_checker.helpers import kickoff_defaults
from loom_checker.helpers import kickoff_defaults_text
from loom_checker.helpers import tree_programs
from loom_checker.reviewers import committed_branch_delta
from pathlib import Path
from typing import Iterable
from repo_files import repository_files
import ast
import importlib.util
import json
import os
import re
import shlex
import subprocess
import tempfile
import tomllib


# `uv run --locked` runs in the project env and stops on a stale lock
# without rewriting it: https://docs.astral.sh/uv/reference/cli/#uv-run
TEST_COMMAND_MARKERS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("uv.lock",), "uv run --locked python -m pytest -q"),
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
        # uv run defines --isolated, --no-project, and --offline as switches;
        # --with-requirements and --with each consume the following value.
        # https://docs.astral.sh/uv/reference/cli/#uv-run
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


CARGO_TEST_FILE = re.compile(r"tests/[^/]+\.rs|tests/[^/]+/main\.rs")


def _cargo_sources(repo: Path, revision: str | None) -> tuple[str | None, set[str], str]:
    """The root Cargo.toml text (None, with the reason, when unreadable) and
    the `tests/*.rs` and `tests/*/main.rs` files, from the working tree or,
    given a revision, from that commit alone."""
    if revision is not None:
        # `<rev>:<path>` names the blob at that path in the commit:
        # https://git-scm.com/docs/gitrevisions#_specifying_revisions;
        # ls-tree -r --name-only -z prints one NUL-terminated path per file:
        # https://git-scm.com/docs/git-ls-tree#_options
        text = git_maybe(repo, "show", f"{revision}:Cargo.toml")
        listed = git_maybe(repo, "ls-tree", "-r", "--name-only", "-z", revision, "--", "tests")
        files = {path for path in (listed or "").split("\0") if CARGO_TEST_FILE.fullmatch(path)}
        return text, files, f"Cargo.toml could not be read at {revision}"
    try:
        text = (repo / "Cargo.toml").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, set(), f"Cargo.toml could not be read: {exc}"
    tests = repo / "tests"
    files = {f"tests/{file.relative_to(tests).as_posix()}"
             for file in [*tests.glob("*.rs"), *tests.glob("*/main.rs")] if file.is_file()}
    return text, files, ""


def cargo_test_targets(repo: Path, revision: str | None = None) -> tuple[list[tuple[str, str, bool]] | None, str]:
    """The root Cargo.toml's test targets as `(name, path, runs)`, or None
    and the reason when the manifest cannot be read. Each `[[test]]` entry is
    a target even under `autotests = false`; its `path` defaults to
    `tests/<name>.rs`, or `tests/<name>/main.rs` when only that exists, and
    its name to the path's stem:
    https://doc.rust-lang.org/cargo/reference/cargo-targets.html#test-targets
    An undeclared `tests/<name>.rs` or `tests/<name>/main.rs` is a target
    named `<name>` unless `[package] autotests = false`; a declared entry of
    the same path or the same name replaces it:
    https://doc.rust-lang.org/cargo/reference/cargo-targets.html#target-auto-discovery
    `runs` is whether plain `cargo test` runs it: not `test = false`, and
    every `required-features` entry listed directly in `[features] default`
    (a feature another default feature enables is not followed, so such a
    target is refused):
    https://doc.rust-lang.org/cargo/reference/cargo-targets.html#the-test-field
    https://doc.rust-lang.org/cargo/reference/cargo-targets.html#the-required-features-field
    https://doc.rust-lang.org/cargo/reference/features.html#the-default-feature
    Given a `revision`, the manifest and test files are read from that commit
    and never from the working tree.
    revision=None reads the working tree (build-time collection checks); validation always passes a sha."""
    text, files, error = _cargo_sources(repo, revision)
    if text is None:
        return None, error
    try:
        manifest = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return None, f"Cargo.toml could not be read: {exc}"
    package = manifest.get("package")
    # A virtual workspace root (no [package]) tests its members, never tests/.
    if not isinstance(package, dict):
        return [], ""
    targets = []
    features = manifest.get("features")
    default = features.get("default") if isinstance(features, dict) else None
    default = {item for item in default if isinstance(item, str)} if isinstance(default, list) else set()
    declared = manifest.get("test")
    for entry in declared if isinstance(declared, list) else []:
        if not isinstance(entry, dict):
            continue
        name, path = entry.get("name"), entry.get("path")
        if isinstance(path, str):
            path = os.path.normpath(path)
        elif isinstance(name, str):
            path = f"tests/{name}.rs"
            if path not in files and f"tests/{name}/main.rs" in files:
                path = f"tests/{name}/main.rs"
        else:
            continue
        name = name if isinstance(name, str) else Path(path).stem
        required = entry.get("required-features") or []
        enabled = isinstance(required, list) and all(
            isinstance(item, str) and item in default for item in required)
        targets.append((name, path, entry.get("test") is not False and enabled))
    if package.get("autotests") is not False:
        known = {item for name, path, _runs in targets for item in (name, path)}
        found = [(Path(path).stem, path) for path in sorted(files) if path.count("/") == 1]
        found += [(Path(path).parent.name, path) for path in sorted(files) if path.count("/") == 2]
        targets += [(name, path, True) for name, path in found if name not in known and path not in known]
    return targets, ""


def _cargo_collects(repo: Path, wanted: str) -> tuple[bool | None, str]:
    """Plain `cargo test` at the root runs `wanted` when it is the path of a
    test target `cargo_test_targets` says it runs."""
    if not (wanted.endswith(".rs") and (repo / wanted).is_file()):
        return False, ""
    targets, error = cargo_test_targets(repo)
    if targets is None:
        return None, error
    return any(path == wanted and runs for _name, path, runs in targets), ""


def _go_collects(repo: Path, wanted: str, tokens: list[str]) -> tuple[bool | None, str]:
    """Whether one declared Go package suite selects this test file."""
    if not wanted.endswith("_test.go") or not (repo / wanted).is_file():
        return False, ""
    args = tokens[2:]
    selectors = [arg for arg in args if not arg.startswith("-")]
    if (len(selectors) != 1 or any(arg.startswith("-") for arg in args if arg not in {"-race", "-v", "-count=1"})
            or (selectors[0] != "." and not selectors[0].startswith("./"))):
        return False, ""
    parent = Path(wanted).parent
    package = "." if parent == Path(".") else "./" + parent.as_posix()
    selector = selectors[0]
    if selector not in {"./...", package}:
        subtree = selector.removesuffix("/...")
        if not selector.endswith("/...") or not package.startswith(subtree + "/"):
            return False, ""
    try:
        # go list -json reports Dir and selected TestGoFiles/XTestGoFiles;
        # file lists are names relative to Dir. https://pkg.go.dev/cmd/go#hdr-List_packages_or_modules
        result = subprocess.run(["go", "list", "-json", package], cwd=repo,
                                capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout) if result.returncode == 0 else {}
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return None, str(exc)
    if not isinstance(data, dict) or not data:
        return None, result.stderr.strip() or "go list returned no package"
    selected = data.get("TestGoFiles", []) + data.get("XTestGoFiles", [])
    return (Path(data.get("Dir", "")).resolve() == (repo / parent).resolve()
            and Path(wanted).name in selected), ""


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
        declared, _source = declared_test_command(repo)
        try:
            tokens = argv_for(declared) if declared else []
        except ValueError:
            tokens = []
        # `cargo nextest run` builds and runs the same test targets.
        if ((tokens[:2] == ["cargo", "test"] and set(tokens[2:]) <= CARGO_TEST_FLAGS)
                or (tokens[:3] == ["cargo", "nextest", "run"] and set(tokens[3:]) <= {"--release"})):
            return _cargo_collects(repo, wanted)
        if tokens[:2] == ["go", "test"]:
            return _go_collects(repo, wanted, tokens)
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
            if (repo / target).resolve() in wanted_path.parents:
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


def stored_probe_programs(repo: Path, head_sha: str, change_id: str) -> int:
    """How many adversarial programs the change holds outside its records:
    committed under its probe store, or graduated into the package suite."""
    return len(set(committed_probe_programs(repo, head_sha, change_id))
               | set(graduated_probe_programs(repo, head_sha, change_id)))


def missing_adversarial_execution(
    count: int, skip: set[str], no_program: list = (), stored: int = 0,
) -> str | None:
    """The refusal reason when the adversarial step, not skipped, left no
    outcome -- neither its programs nor a no-program outcome -- else None.

    One predicate for both places that ask it -- finalize-review over its
    review input, and the attestation validator over the recorded
    executions -- so the two can never answer with different words.

    `no_program` holds the reasons of recorded no-program outcomes: the
    adversary attacked and found no program worth committing. A no-program
    outcome with a one-line, trimmed, comment-free reason, and nothing else recorded or stored
    beside it, satisfies the step.

    `stored` counts the programs the change holds from another source
    (`stored_probe_programs`). It is kept apart from `count`, which counts
    executed records: a stored program does not satisfy the step, but it
    does contradict a record saying the adversary committed none.
    """
    if no_program:
        if len(no_program) > 1 or count or stored:
            return ("a no-program outcome contradicts another adversarial "
                    "record or a program stored for this change")
        reason = no_program[0]
        # Publish splits the body with str.splitlines() and matches the
        # disclosed line exactly, after stripping the line and its HTML
        # comments: only a reason that survives all three can.
        if (not isinstance(reason, str) or not reason or reason != reason.strip()
                or len(reason.splitlines()) != 1 or "<!--" in reason):
            return ("a no-program outcome needs a reason on one line, with no "
                    "surrounding whitespace or HTML comment")
        return None
    if count < 1 and "adversarial" not in skip:
        return ("the adversarial step left no outcome: record its programs, "
                "or a no-program outcome with its reason")
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


# `subprocess.run` receives argv without a shell, so `$` is a literal byte.
# Go's exact `-run ^TestName$` selection needs that end anchor.
SHELL_METACHARACTERS = re.compile(r"[;&|<>()`*?\[\]{}\n]")


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


CARGO_TEST_FLAGS = frozenset({"--release", "-q", "--quiet"})


def _python_argv(tokens: list[str]) -> list[str]:
    """The python argv a conda-run pytest or `uv run` command wraps.

    Relied on: `conda run -n ENV CMD...` runs CMD in that environment
    (https://docs.conda.io/projects/conda/en/stable/commands/run.html) and
    `uv run [OPTIONS] COMMAND` runs COMMAND in the project environment
    (https://docs.astral.sh/uv/reference/cli/#uv-run)."""
    if _conda_pytest_argv(tokens):
        tokens = tokens[4:]
    # `uv run [opts] python ...` is checked as the python argv it wraps.
    if tokens[:2] == ["uv", "run"]:
        tokens = next((tokens[i:] for i in range(2, len(tokens))
                       if Path(tokens[i]).name.startswith("python")), [""])
    return tokens


def runs_pytest(command: str) -> bool:
    """True when argv is a (wrapped) `python -m pytest` command."""
    tokens = _python_argv(argv_for(command))
    return Path(tokens[0]).name.startswith("python") and tokens[1:3] == ["-m", "pytest"]


def direct_pytest_style_failure(command: str, artifact: str, source: str) -> str | None:
    """Why a bare `python <artifact>` run of a pytest-style file proves
    nothing, or None. Such a run imports the module and exits 0 without
    calling a test, so a file whose top-level statements define a `test*`
    function or a `Test*` class (pytest's default collection prefixes) must
    run under `python -m pytest`; a file that does not parse is refused
    rather than trusted.

    Relied on: pytest's default `python_functions = test*` and
    `python_classes = Test*`:
    https://docs.pytest.org/en/stable/explanation/goodpractices.html#conventions-for-python-test-discovery"""
    if Path(artifact).suffix.lower() != ".py" or runs_pytest(command):
        return None
    try:
        body = ast.parse(source).body
    except (SyntaxError, ValueError):
        return f"{artifact} does not parse; record `python -m pytest {artifact}` for a test file"
    if any((isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test"))
           or (isinstance(node, ast.ClassDef) and node.name.startswith("Test"))
           for node in body):
        return (f"{artifact} defines pytest tests that a bare python run never calls; "
                f"record `python -m pytest {artifact}`")
    return None


def command_executes_artifact(command: str, artifact: str) -> bool:
    """True when argv directly executes the named Python, shell, or
    executable file. Other runners' rows live in `probe_results`."""
    tokens = argv_for(command)
    wanted = os.path.normpath(artifact)
    suffix = Path(artifact).suffix.lower()
    if suffix == ".py":
        tokens = _python_argv(tokens)
        args = tokens[1:]
        # `python -m pytest ... X ...`: every option, in any position, must be
        # on the allowlist, and X must be the sole positional argument, so no
        # other file runs in the probe's place.
        if args[:2] == ["-m", "pytest"]:
            args = pytest_positionals(args[2:]) or []
            if len(args) != 1:
                return False
        return (Path(tokens[0]).name.startswith("python") and bool(args)
                and os.path.normpath(args[0]) == wanted)
    if suffix == ".sh":
        return len(tokens) >= 2 and Path(tokens[0]).name in {"bash", "sh"} and os.path.normpath(tokens[1]) == wanted
    return os.path.normpath(tokens[0]) in {wanted, os.path.join(".", wanted)}


def declared_test_command(repo: Path, revision: str | None = None) -> tuple[str | None, str]:
    """The repo's own package-test command, and where it was read from.

    A recorded probe is compared against THIS, so that a command which
    exits 0 without running the suite cannot stand in for the suite. The
    repo's own KICKOFF-DEFAULTS line wins, because only the repo knows;
    otherwise the same markers the build station reads are read here.

    The test-file scan asks `repo_files.repository_files` which files are
    the repo's own: a walk of the directory also sees a linked worktree
    checked out inside it, or ignored build output, and would report a
    test command for a suite that is not this repository's.

    With `revision`, all three are read from that commit instead of the
    working tree, so validating a commit never depends on uncommitted files.
    revision=None reads the working tree (build-time collection checks); validation always passes a sha."""
    if revision is None:
        defaults = kickoff_defaults(repo)
        has_file = lambda marker: (repo / marker).is_file()  # noqa: E731
        names = None
    else:
        # `<rev>:<path>` and ls-tree -r --name-only -z, cited at _cargo_sources:
        # https://git-scm.com/docs/gitrevisions#_specifying_revisions
        # https://git-scm.com/docs/git-ls-tree#_options
        text = git_maybe(repo, "show", f"{revision}:docs/loom/KICKOFF-DEFAULTS.md")
        defaults = kickoff_defaults_text(text) if text is not None else {}
        listed = (git_maybe(repo, "ls-tree", "-r", "--name-only", "-z", revision) or "").split("\0")
        committed = {path for path in listed if path}
        has_file = committed.__contains__
        names = [Path(path).name for path in committed]
    declared = defaults.get("package-tests", "").strip()
    if declared:
        return declared, "docs/loom/KICKOFF-DEFAULTS.md"
    for markers, command in TEST_COMMAND_MARKERS:
        if any(has_file(marker) for marker in markers):
            return command, f"detected {markers[0]}"
    if names is None:
        names = [path.name for path in repository_files(repo)]
    for pattern in ("test_*.py", "*_test.py"):
        if any(fnmatch(name, pattern) for name in names):
            return "python3 -m pytest -q", f"detected {pattern} files"
    return None, ""
