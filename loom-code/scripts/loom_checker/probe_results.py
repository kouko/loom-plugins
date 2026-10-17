"""Runner rows: which probe argv a listed test runner owns, the one form it
accepts, and how many of the artifact's tests the run's own output shows
passing.

Each row answers three questions:

- `claims(argv)` -- is this argv that runner (runner identity only);
- `accepts(argv, artifact)` -- is it the row's accepted form, running the
  artifact alone with the runner's machine-readable output where it has one;
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

from loom_checker.probes import _conda_python_argv


@dataclass(frozen=True)
class Row:
    name: str
    claims: Callable[[list[str]], bool]
    accepts: Callable[[list[str], str], bool]
    passed: Callable[[str, str], int | None]


ANSI = re.compile(r"\x1b\[[0-9;]*m")


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
    return argv[:2] == ["go", "test"]


def _go_accepts(argv: list[str], artifact: str) -> bool:
    """`go test -json [-v] [-race] [-count N] [-timeout D] [-tags T] <A>`."""
    if not os.path.normpath(artifact).endswith("_test.go"):
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
    return argv[:1] == ["node"] and "--test" in argv[1:]


def _node_accepts(argv: list[str], artifact: str) -> bool:
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
    return argv[:2] == ["deno", "test"]


def _deno_accepts(argv: list[str], artifact: str) -> bool:
    """`deno test --reporter=junit [-A] [--allow-*] <A>`."""
    options = [arg for arg in argv[2:] if arg.startswith("-")]
    return (_distinct(options) and "--reporter=junit" in options
            and all(arg in {"--reporter=junit", "-A"} or DENO_ALLOW.fullmatch(arg) for arg in options)
            and _one_positional(argv[2:], artifact))


def _deno_passed(output: str, artifact: str) -> int | None:
    return _junit_passed(output, artifact, lambda case: case.get("classname"), lambda case: False)


# bun ------------------------------------------------------------------------

BUN_SUMMARY = re.compile(r"^Ran \d+ tests? across (\d+) files?\.", re.MULTILINE)
BUN_PASS = re.compile(r"^\s*(\d+) pass\s*$", re.MULTILINE)


def _bun_claims(argv: list[str]) -> bool:
    return argv[:2] == ["bun", "test"]


def _bun_accepts(argv: list[str], artifact: str) -> bool:
    """`bun test ./<A>` or an absolute `<A>`: bun reads any other positional
    as a substring filter over every test file it finds."""
    if len(argv) != 3:
        return False
    target = argv[2]
    if target.startswith("./"):
        return os.path.normpath(target) == os.path.normpath(artifact)
    return os.path.isabs(target) and _reports_artifact(target, artifact)


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


def _unittest_accepts(argv: list[str], artifact: str) -> bool:
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


ROWS: tuple[Row, ...] = (
    Row("go", _go_claims, _go_accepts, _go_passed),
    Row("unittest", _unittest_claims, _unittest_accepts, _unittest_passed),
    Row("node", _node_claims, _node_accepts, _node_passed),
    Row("deno", _deno_claims, _deno_accepts, _deno_passed),
    Row("bun", _bun_claims, _bun_accepts, _bun_passed),
)


def claiming_row(argv: list[str]) -> Row | None:
    """The row whose runner `argv` is, or None when no listed runner is."""
    return next((row for row in ROWS if row.claims(argv)), None)
