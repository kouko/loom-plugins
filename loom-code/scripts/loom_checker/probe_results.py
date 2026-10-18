"""Runner rows: which probe argv a listed test runner owns, the one form it
accepts, and how many of the artifact's tests the run's own output shows
passing.

Each row answers three questions:

- `claims(argv)` -- is this argv that runner (runner identity only);
- `accepts(argv, artifact, repo=None)` -- is it the row's accepted form,
  running the artifact alone with the runner's machine-readable output where
  it has one; only the cargo rows read `repo` (its Cargo.toml maps a test
  target name to a file) and refuse without it;
- `passed(output, artifact)` -- passing, non-skipped tests from the artifact
  in the combined stdout+stderr, 0 when the output is readable but shows none
  (or shows tests from another file), None when the row cannot read it.

A claimed argv the row does not accept is refused; an argv no row claims, or
output a row cannot read, needs a reviewer's confirmation instead. Adding a
runner is one more row here plus its fixtures.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree
import json
import os
import re

from loom_checker.probes import CARGO_TEST_FLAGS
from loom_checker.probes import cargo_test_targets
from loom_checker.probes import _conda_python_argv


@dataclass(frozen=True)
class Row:
    name: str
    claims: Callable[[list[str]], bool]
    accepts: Callable[[list[str], str, Path | None], bool]
    passed: Callable[[str, str], int | None]


ANSI = re.compile(r"\x1b\[[0-9;]*m")
ENV_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=.*")
# Variables a runner reads as options or test filters. A denylist: a variable
# it misses is a residual risk, bounded by the per-file result parsing.
RUNNER_ENV = re.compile(
    r"(?:GOFLAGS|NODE_OPTIONS|NODE_TEST_\w*|JEST_\w*|VITEST_\w*|MOCHA_\w*|BUN_\w*"
    r"|DENO_\w*|CARGO_\w*|RUSTFLAGS|RUSTDOCFLAGS|NEXTEST_\w*|SPEC_OPTS|TESTOPTS"
    r"|RUBYOPT|PHPUNIT_\w*|PYTEST_ADDOPTS)=.*")


def _env_split(argv: list[str]) -> tuple[list[str], list[str]]:
    """The `NAME=value` assignments of a leading `env` and the argv after
    them; `[]` when no command follows. Any `env` option keeps the argv
    whole, so no row claims it."""
    if not argv or Path(argv[0]).name != "env":
        return [], argv
    index = 1
    while index < len(argv) and ENV_ASSIGNMENT.fullmatch(argv[index]):
        index += 1
    if index < len(argv) and argv[index].startswith("-"):
        return [], argv
    return argv[1:index], argv[index:]


def _env_stripped(argv: list[str]) -> list[str]:
    return _env_split(argv)[1]


def _env_accepts(accepts: Callable[[list[str], str, Path | None], bool],
                 argv: list[str], artifact: str, repo: Path | None) -> bool:
    """`accepts` on the argv after `env`, refusing a runner-configuration assignment."""
    assignments, rest = _env_split(argv)
    return not any(RUNNER_ENV.fullmatch(arg) for arg in assignments) and accepts(rest, artifact, repo)


def _named(argv: list[str]) -> list[str]:
    """`argv` with its command reduced to its base name, so
    `/opt/homebrew/bin/go` is `go`."""
    return [Path(argv[0]).name, *argv[1:]] if argv else argv


def _one_positional(args: list[str], artifact: str) -> bool:
    positionals = [arg for arg in args if not arg.startswith("-")]
    return len(positionals) == 1 and os.path.normpath(positionals[0]) == os.path.normpath(artifact)


def _distinct(options: list[str]) -> bool:
    return len(options) == len(set(options))


def _reports_artifact(reported: str, artifact: str) -> bool:
    """A runner-reported path (relative, `./`-prefixed or absolute) is the artifact."""
    wanted = os.path.normpath(artifact)
    path = os.path.normpath(reported)
    return path == wanted or path.endswith(os.sep + wanted)


# go -----------------------------------------------------------------------

GO_FLAGS = frozenset({"-json", "-v", "-race"})
GO_VALUE_FLAGS = frozenset({"-count", "-timeout", "-tags"})


def _go_claims(argv: list[str]) -> bool:
    """`go` with any subcommand: `go vet` or `go run` is go in another form."""
    return _named(argv)[:1] == ["go"]


def _go_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`go test -json [-v] [-race] [-count N] [-timeout D] [-tags T] <A>`."""
    if argv[1:2] != ["test"] or not os.path.normpath(artifact).endswith("_test.go"):
        return False
    options, positionals, rest = [], [], argv[2:]
    while rest:
        arg = rest.pop(0)
        if not arg.startswith("-"):
            positionals.append(arg)
        elif arg in GO_FLAGS:
            options.append(arg)
        elif arg in GO_VALUE_FLAGS:
            if not rest or rest[0].startswith("-"):
                return False
            options.append(arg)
            rest.pop(0)
        elif "=" in arg and arg.split("=", 1)[0] in GO_VALUE_FLAGS and arg.split("=", 1)[1]:
            options.append(arg.split("=", 1)[0])
        else:
            return False
    return "-json" in options and _distinct(options) and _one_positional(positionals, artifact)


def _go_passed(output: str, artifact: str) -> int | None:
    """Leaf tests with a `pass` event; a parent whose subtests all skipped
    passes too, so only tests without subtests count."""
    events = []
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and isinstance(event.get("Action"), str):
            events.append(event)
    if not events:
        return None
    tests = {event["Test"] for event in events if isinstance(event.get("Test"), str)}
    passed = {event["Test"] for event in events
              if event["Action"] == "pass" and isinstance(event.get("Test"), str)}
    return sum(1 for name in passed if not any(other.startswith(name + "/") for other in tests))


# JUnit XML (node, deno) -----------------------------------------------------

NOT_PASSED = frozenset({"skipped", "failure", "error"})


def _junit_cases(output: str) -> list[ElementTree.Element] | None:
    """The <testcase> elements of the one <testsuites> report in `output`.

    The slice starts at <testsuites, so a DOCTYPE (and any entity it would
    declare) is never parsed."""
    start = output.find("<testsuites")
    end = output.rfind("</testsuites>")
    if start < 0 or end < start:
        return None
    try:
        root = ElementTree.fromstring(output[start:end + len("</testsuites>")])
    except ElementTree.ParseError:
        return None
    return list(root.iter("testcase"))


def _junit_passed(output: str, artifact: str, source: Callable[[ElementTree.Element], str | None],
                  file_level: Callable[[ElementTree.Element], bool]) -> int | None:
    cases = _junit_cases(output)
    if cases is None:
        return None
    count = 0
    for case in cases:
        reported = source(case)
        if not reported:
            return None
        if not _reports_artifact(reported, artifact):
            return 0
        if any(child.tag in NOT_PASSED for child in case) or file_level(case):
            continue
        count += 1
    return count


NODE_REQUIRED = frozenset({"--test", "--test-reporter=junit"})
NODE_ALLOWED = NODE_REQUIRED | {"--experimental-strip-types"}


def _node_claims(argv: list[str]) -> bool:
    return _named(argv)[:1] == ["node"] and "--test" in argv[1:]


def _node_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`node --test --test-reporter=junit [--experimental-strip-types] <A>`."""
    options = [arg for arg in argv[1:] if arg.startswith("-")]
    return (_distinct(options) and NODE_REQUIRED <= set(options) <= NODE_ALLOWED
            and _one_positional(argv[1:], artifact))


def _node_file_level(case: ElementTree.Element) -> bool:
    """A file that defines no test still reports one passing case named by
    the path it was given; it is not a test."""
    return Path(case.get("name", "")).name == Path(case.get("file", "")).name


def _node_passed(output: str, artifact: str) -> int | None:
    return _junit_passed(output, artifact, lambda case: case.get("file"), _node_file_level)


DENO_ALLOW = re.compile(r"--allow-[a-z-]+(=\S+)?")


def _deno_claims(argv: list[str]) -> bool:
    """`deno` with any subcommand: `deno check` or `deno run` is deno in another form."""
    return _named(argv)[:1] == ["deno"]


def _deno_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`deno test --reporter=junit [-A] [--allow-*] <A>`."""
    options = [arg for arg in argv[2:] if arg.startswith("-")]
    return (argv[1:2] == ["test"] and _distinct(options) and "--reporter=junit" in options
            and all(arg in {"--reporter=junit", "-A"} or DENO_ALLOW.fullmatch(arg) for arg in options)
            and _one_positional(argv[2:], artifact))


def _deno_passed(output: str, artifact: str) -> int | None:
    """Leaf cases only: a `t.step` parent is its own case, beside one case per
    step named `<parent> > <step>`, and passes even when every step was ignored."""
    names = [case.get("name", "") for case in _junit_cases(output) or []]
    return _junit_passed(output, artifact, lambda case: case.get("classname"),
                         lambda case: any(name.startswith(case.get("name", "") + " > ") for name in names))


# bun ------------------------------------------------------------------------

BUN_SUMMARY = re.compile(r"^Ran \d+ tests? across (\d+) files?\.", re.MULTILINE)
BUN_PASS = re.compile(r"^\s*(\d+) pass\s*$", re.MULTILINE)


def _bun_claims(argv: list[str]) -> bool:
    """`bun` with any subcommand: `bun build` or `bun <file>` is bun in another form."""
    return _named(argv)[:1] == ["bun"]


def _bun_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`bun test ./<A>` only: bun reads any other positional as a substring
    filter over every test file it finds, and an absolute path names one
    machine's checkout, so the recorded command could not re-run elsewhere."""
    if len(argv) != 3 or argv[1] != "test" or not argv[2].startswith("./"):
        return False
    return os.path.normpath(argv[2]) == os.path.normpath(artifact)


def _bun_passed(output: str, artifact: str) -> int | None:
    """bun's summary names no file, so only a run `across 1 file` counts."""
    text = ANSI.sub("", output)
    summary, passes = BUN_SUMMARY.findall(text), BUN_PASS.findall(text)
    if not summary or not passes:
        return None
    return int(passes[-1]) if summary[-1] == "1" else 0


# python -m unittest -----------------------------------------------------------

UNITTEST_RAN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
UNITTEST_STATUS = re.compile(r"^(?:OK|FAILED)(?: \(([^)]*)\))?\s*$", re.MULTILINE)


def _python_argv(argv: list[str]) -> list[str]:
    """The python argv inside the same conda/uv launchers pytest accepts."""
    if _conda_python_argv(argv):
        argv = argv[4:]
    if argv[:2] == ["uv", "run"]:
        argv = next((argv[i:] for i in range(2, len(argv)) if Path(argv[i]).name.startswith("python")), [])
    return argv if argv and Path(argv[0]).name.startswith("python") else []


def _unittest_claims(argv: list[str]) -> bool:
    return _python_argv(argv)[1:3] == ["-m", "unittest"]


def _unittest_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`python -m unittest [-v] [-q] <A>`."""
    args = _python_argv(argv)[3:]
    options = [arg for arg in args if arg.startswith("-")]
    return (artifact.endswith(".py") and _distinct(options) and set(options) <= {"-v", "-q"}
            and _one_positional(args, artifact))


def _unittest_passed(output: str, artifact: str) -> int | None:
    text = ANSI.sub("", output)
    ran = UNITTEST_RAN.findall(text)
    if not ran:
        return None
    if int(ran[-1]) == 0:
        return 0
    status = UNITTEST_STATUS.findall(text)
    if not status:
        return None
    counts = {}
    for item in filter(None, (part.strip() for part in status[-1].split(","))):
        key, _, value = item.partition("=")
        if not value.isdigit():
            return None
        counts[key] = int(value)
    not_passed = sum(counts.get(key, 0) for key in ("failures", "errors", "skipped", "expected failures"))
    return max(int(ran[-1]) - not_passed, 0)


# JSON reports (jest, vitest, mocha, rspec) -------------------------------------

# Longer prefixes first: the first launcher an argv starts with is stripped.
JS_LAUNCHERS = (("npx", "--yes"), ("npx",), ("pnpm", "exec"), ("pnpm",), ("yarn",))
RUBY_LAUNCHERS = (("bundle", "exec"),)


def _launched(argv: list[str], launchers: tuple[tuple[str, ...], ...]) -> list[str]:
    """`argv` without the one allowed launcher prefix it starts with, its
    launcher and the runner it reaches both named by base name."""
    argv = _named(argv)
    for launcher in launchers:
        if tuple(argv[:len(launcher)]) == launcher:
            return _named(argv[len(launcher):])
    return argv


def _only_pair_and_artifact(args: list[str], flag: str, value: str, artifact: str) -> bool:
    """`args` is exactly `flag value` plus the artifact, in any order."""
    if args.count(flag) != 1:
        return False
    index = args.index(flag)
    if args[index + 1:index + 2] != [value]:
        return False
    rest = args[:index] + args[index + 2:]
    return len(rest) == 1 and _one_positional(rest, artifact)


def _json_report(output: str, key: str) -> dict | None:
    """The first JSON object starting a line of `output` that carries `key`."""
    decoder = json.JSONDecoder()
    for match in re.finditer(r"^\{", output, re.MULTILINE):
        try:
            report, _end = decoder.raw_decode(output, match.start())
        except ValueError:
            continue
        if isinstance(report, dict) and key in report:
            return report
    return None


def _per_file(entries: object, artifact: str, file_key: str,
              counted: Callable[[dict], int]) -> int | None:
    """Sum `counted` over report entries that each name their file; 0 as soon
    as one names another file, None when an entry is not readable."""
    if not isinstance(entries, list):
        return None
    total = 0
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get(file_key), str):
            return None
        if not _reports_artifact(entry[file_key], artifact):
            return 0
        total += counted(entry)
    return total


def _jest_claims(argv: list[str]) -> bool:
    return _launched(argv, JS_LAUNCHERS)[:1] == ["jest"]


def _jest_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`[w] jest --json --runTestsByPath <A>`."""
    args = _launched(argv, JS_LAUNCHERS)[1:]
    options = sorted(arg for arg in args if arg.startswith("-"))
    return options == ["--json", "--runTestsByPath"] and _one_positional(args, artifact)


def _vitest_claims(argv: list[str]) -> bool:
    return _launched(argv, JS_LAUNCHERS)[:1] == ["vitest"]


VITEST_STDOUT = "--outputFile=/dev/stdout"


def _vitest_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`[w] vitest run --reporter=json --outputFile=/dev/stdout <A>` (or
    `--outputFile /dev/stdout`): vitest 5 writes the JSON report to a file
    unless the output file is stdout."""
    args = _launched(argv, JS_LAUNCHERS)[1:]
    if args[:1] != ["run"]:
        return False
    rest = args[1:]
    if rest.count("--outputFile") == 1:
        index = rest.index("--outputFile")
        if rest[index + 1:index + 2] != ["/dev/stdout"]:
            return False
        rest = rest[:index] + [VITEST_STDOUT] + rest[index + 2:]
    options = sorted(arg for arg in rest if arg.startswith("-"))
    return options == [VITEST_STDOUT, "--reporter=json"] and _one_positional(rest, artifact)


def _assertions_passed(result: dict) -> int:
    cases = result.get("assertionResults")
    return sum(1 for case in cases if isinstance(case, dict) and case.get("status") == "passed") \
        if isinstance(cases, list) else 0


def _jest_passed(output: str, artifact: str) -> int | None:
    """jest's (and vitest's jest-shaped) report: one result per test file."""
    report = _json_report(output, "testResults")
    return None if report is None else _per_file(report["testResults"], artifact, "name", _assertions_passed)


def _mocha_claims(argv: list[str]) -> bool:
    return _launched(argv, JS_LAUNCHERS)[:1] == ["mocha"]


def _mocha_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`[w] mocha --reporter json <A>`."""
    return _only_pair_and_artifact(_launched(argv, JS_LAUNCHERS)[1:], "--reporter", "json", artifact)


def _mocha_passed(output: str, artifact: str) -> int | None:
    report = _json_report(output, "passes")
    if report is None:
        return None
    tests = _per_file(report.get("tests"), artifact, "file", lambda test: 1)
    passes = _per_file(report["passes"], artifact, "file", lambda test: 1)
    if tests is None or passes is None:
        return None
    return passes if tests else 0


def _rspec_claims(argv: list[str]) -> bool:
    return _launched(argv, RUBY_LAUNCHERS)[:1] == ["rspec"]


def _rspec_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`[w] rspec --format json <A>`. A `--dry-run` from an `.rspec` file
    reports every example `passed` in the same JSON; that stays a residual
    risk, since the argv cannot show it."""
    return _only_pair_and_artifact(_launched(argv, RUBY_LAUNCHERS)[1:], "--format", "json", artifact)


def _rspec_passed(output: str, artifact: str) -> int | None:
    report = _json_report(output, "examples")
    return None if report is None else _per_file(
        report["examples"], artifact, "file_path", lambda example: int(example.get("status") == "passed"))


# minitest, phpunit (console summary; one file by their positional) -----------

MINITEST_FILE = re.compile(r"(?:.+_test|test_.+)\.rb")
MINITEST_SUMMARY = re.compile(
    r"^(\d+) runs, \d+ assertions, (\d+) failures, (\d+) errors, (\d+) skips\s*$", re.MULTILINE)


def _minitest_claims(argv: list[str]) -> bool:
    args = _launched(argv, RUBY_LAUNCHERS)
    return args[:1] == ["ruby"] and any(
        not arg.startswith("-") and MINITEST_FILE.fullmatch(Path(arg).name) for arg in args[1:])


def _minitest_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`[w] ruby [-I<dir>]... <A>`: nothing after the file, where minitest
    would read `-n`/`-e` filters."""
    args = _launched(argv, RUBY_LAUNCHERS)[1:]
    return (bool(args) and bool(MINITEST_FILE.fullmatch(Path(artifact).name))
            and os.path.normpath(args[-1]) == os.path.normpath(artifact)
            and all(arg.startswith("-I") and len(arg) > 2 for arg in args[:-1]))


def _minitest_passed(output: str, artifact: str) -> int | None:
    summary = MINITEST_SUMMARY.findall(ANSI.sub("", output))
    if not summary:
        return None
    runs, failures, errors, skips = map(int, summary[-1])
    return max(runs - failures - errors - skips, 0)


PHPUNIT_OK = re.compile(r"^OK \((\d+) tests?, \d+ assertions?\)\s*$", re.MULTILINE)
PHPUNIT_COUNTS = re.compile(r"^Tests: (\d+), Assertions: \d+((?:, [A-Za-z ]+: \d+)*)\.\s*$", re.MULTILINE)
PHPUNIT_NOT_PASSED = ("Errors", "Failures", "Skipped", "Incomplete", "Risky")


def _phpunit_claims(argv: list[str]) -> bool:
    """`phpunit` by base name: `vendor/bin/phpunit`, `/usr/local/bin/phpunit`."""
    return _named(argv)[:1] == ["phpunit"]


def _phpunit_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`<phpunit> <A>`."""
    return len(argv) == 2 and os.path.normpath(argv[1]) == os.path.normpath(artifact)


def _phpunit_passed(output: str, artifact: str) -> int | None:
    text = ANSI.sub("", output)
    if ok := PHPUNIT_OK.findall(text):
        return int(ok[-1])
    if counts := PHPUNIT_COUNTS.findall(text):
        tests, details = counts[-1]
        found = dict(item.split(": ") for item in details.split(", ")[1:])
        return max(int(tests) - sum(int(found.get(key, 0)) for key in PHPUNIT_NOT_PASSED), 0)
    return 0 if "No tests executed!" in text else None


# cargo test, cargo nextest (one test target by --test <n>) ---------------------

NEXTEST_FLAGS = frozenset({"--release", "--no-tests=fail"})
CARGO_RESULT = re.compile(r"^test result: \w+\. (\d+) passed; ", re.MULTILINE)
NEXTEST_SUMMARY = re.compile(r"^\s*Summary \[[^\]]*\] \d+ tests? run: (\d+) passed", re.MULTILINE)


def _cargo_target_name(args: list[str], flags: frozenset[str]) -> str | None:
    """`<n>` of the one `--test <n>` (or `--test=<n>`) among `flags`, or None
    for any other argument -- a test-name filter, `--` arguments, or
    `--no-run` can exit 0 without running the file's tests."""
    names, rest = [], list(args)
    while rest:
        arg = rest.pop(0)
        if arg in flags:
            continue
        if arg == "--test" and rest and not rest[0].startswith("-"):
            names.append(rest.pop(0))
        elif arg.startswith("--test=") and len(arg) > len("--test="):
            names.append(arg[len("--test="):])
        else:
            return None
    return names[0] if len(names) == 1 else None


def _cargo_test_path(repo: Path | None, name: str) -> str | None:
    """The file `--test <name>` builds: the Cargo.toml `[[test]]` entry of
    that name (named, or named by its path's stem), else `tests/<name>.rs`.
    An explicit `--test` runs a `test = false` target too. None when the
    manifest cannot be read."""
    if repo is None:
        return None
    targets, _error = cargo_test_targets(repo)
    if targets is None:
        return None
    return next((path for target, path, _runs in targets if target == name), f"tests/{name}.rs")


def _cargo_names(name: str | None, artifact: str, repo: Path | None) -> bool:
    return name is not None and _cargo_test_path(repo, name) == os.path.normpath(artifact)


def _cargo_claims(argv: list[str]) -> bool:
    """`cargo` with any subcommand but `nextest`, the nextest row's: `cargo
    build` or `cargo run` is cargo in another form."""
    return _named(argv)[:1] == ["cargo"] and argv[1:2] != ["nextest"]


def _cargo_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`cargo test [--release] [-q] --test <n>`, `<n>` resolving to `<A>`."""
    return argv[1:2] == ["test"] and _cargo_names(_cargo_target_name(argv[2:], CARGO_TEST_FLAGS), artifact, repo)


def _cargo_passed(output: str, artifact: str) -> int | None:
    results = CARGO_RESULT.findall(ANSI.sub("", output))
    return sum(map(int, results)) if results else None


def _nextest_claims(argv: list[str]) -> bool:
    return _named(argv)[:2] == ["cargo", "nextest"]


def _nextest_accepts(argv: list[str], artifact: str, repo: Path | None = None) -> bool:
    """`cargo nextest run [--release] [--no-tests=fail] --test <n>`; any other
    `--no-tests` value lets an empty run pass."""
    if argv[2:3] != ["run"]:
        return False
    args, rest = [], argv[3:]
    while rest:
        arg = rest.pop(0)
        if arg == "--no-tests" and rest[:1] == ["fail"]:
            arg = "--no-tests=" + rest.pop(0)
        args.append(arg)
    return _cargo_names(_cargo_target_name(args, NEXTEST_FLAGS), artifact, repo)


def _nextest_passed(output: str, artifact: str) -> int | None:
    summary = NEXTEST_SUMMARY.findall(ANSI.sub("", output))
    return int(summary[-1]) if summary else None


def _row(name: str, claims: Callable[[list[str]], bool],
         accepts: Callable[[list[str], str, Path | None], bool],
         passed: Callable[[str, str], int | None]) -> Row:
    """A row that sees every argv without its `env NAME=value...` prefix."""
    return Row(name, lambda argv: claims(_env_stripped(argv)),
               lambda argv, artifact, repo=None: _env_accepts(accepts, argv, artifact, repo), passed)


ROWS: tuple[Row, ...] = (
    _row("go", _go_claims, _go_accepts, _go_passed),
    _row("unittest", _unittest_claims, _unittest_accepts, _unittest_passed),
    _row("node", _node_claims, _node_accepts, _node_passed),
    _row("deno", _deno_claims, _deno_accepts, _deno_passed),
    _row("bun", _bun_claims, _bun_accepts, _bun_passed),
    _row("jest", _jest_claims, _jest_accepts, _jest_passed),
    _row("vitest", _vitest_claims, _vitest_accepts, _jest_passed),
    _row("mocha", _mocha_claims, _mocha_accepts, _mocha_passed),
    _row("cargo test", _cargo_claims, _cargo_accepts, _cargo_passed),
    _row("nextest", _nextest_claims, _nextest_accepts, _nextest_passed),
    _row("rspec", _rspec_claims, _rspec_accepts, _rspec_passed),
    _row("minitest", _minitest_claims, _minitest_accepts, _minitest_passed),
    _row("phpunit", _phpunit_claims, _phpunit_accepts, _phpunit_passed),
)


def claiming_row(argv: list[str]) -> Row | None:
    """The row whose runner `argv` is, or None when no listed runner is."""
    return next((row for row in ROWS if row.claims(argv)), None)
