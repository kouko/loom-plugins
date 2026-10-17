"""The runner row table in `loom_checker.probe_results`: a row claims an argv
by runner identity, accepts only its documented form, and reads the run's own
output -- a count of passing, non-skipped tests from the artifact, 0 for a
readable run that shows none, None for output the row cannot read.

Every output constant below is real output captured from the installed
runner (go 1.27, node 26, deno 2.9, bun 1.4.3, python 3.12) on a one-file
probe; only the absolute scratch directory (shortened to `/work/repo`) and
the probe file's name (so one artifact constant serves each row) were edited.
bun prints its summary on stderr, so its constants are stdout then stderr.
"""
from __future__ import annotations

import shlex

import pytest

from loom_checker.probe_results import claiming_row
from loom_checker.probes import command_executes_artifact
from loom_checker.probes import command_names_artifact

GO = "probes/add_test.go"
NODE = "probes/attack.test.mjs"
DENO = "probes/attack_test.ts"
BUN = "probes/p.test.ts"
UNITTEST = "probes/probe_pass.py"

GO_PASS = """\
{"Time":"2026-10-17T12:52:42.771241+08:00","Action":"start","Package":"command-line-arguments"}
{"Time":"2026-10-17T12:52:43.028724+08:00","Action":"run","Package":"command-line-arguments","Test":"TestAdd"}
{"Time":"2026-10-17T12:52:43.028877+08:00","Action":"output","Package":"command-line-arguments","Test":"TestAdd","Output":"=== RUN   TestAdd\\n","OutputType":"frame"}
{"Time":"2026-10-17T12:52:43.029016+08:00","Action":"output","Package":"command-line-arguments","Test":"TestAdd","Output":"--- PASS: TestAdd (0.00s)\\n","OutputType":"frame"}
{"Time":"2026-10-17T12:52:43.029033+08:00","Action":"pass","Package":"command-line-arguments","Test":"TestAdd","Elapsed":0}
{"Time":"2026-10-17T12:52:43.029058+08:00","Action":"output","Package":"command-line-arguments","Output":"PASS\\n","OutputType":"frame"}
{"Time":"2026-10-17T12:52:43.029449+08:00","Action":"output","Package":"command-line-arguments","Output":"ok  \\tcommand-line-arguments\\t0.258s\\n"}
{"Time":"2026-10-17T12:52:43.029485+08:00","Action":"pass","Package":"command-line-arguments","Elapsed":0.258}
"""

GO_SKIP = """\
{"Time":"2026-10-17T12:52:43.220817+08:00","Action":"start","Package":"command-line-arguments"}
{"Time":"2026-10-17T12:52:43.483859+08:00","Action":"run","Package":"command-line-arguments","Test":"TestAdd"}
{"Time":"2026-10-17T12:52:43.483999+08:00","Action":"output","Package":"command-line-arguments","Test":"TestAdd","Output":"=== RUN   TestAdd\\n","OutputType":"frame"}
{"Time":"2026-10-17T12:52:43.484088+08:00","Action":"output","Package":"command-line-arguments","Test":"TestAdd","Output":"    add_test.go:6: not now\\n"}
{"Time":"2026-10-17T12:52:43.484129+08:00","Action":"output","Package":"command-line-arguments","Test":"TestAdd","Output":"--- SKIP: TestAdd (0.00s)\\n","OutputType":"frame"}
{"Time":"2026-10-17T12:52:43.484143+08:00","Action":"skip","Package":"command-line-arguments","Test":"TestAdd","Elapsed":0}
{"Time":"2026-10-17T12:52:43.484163+08:00","Action":"output","Package":"command-line-arguments","Output":"PASS\\n","OutputType":"frame"}
{"Time":"2026-10-17T12:52:43.484805+08:00","Action":"output","Package":"command-line-arguments","Output":"ok  \\tcommand-line-arguments\\t0.264s\\n"}
{"Time":"2026-10-17T12:52:43.484842+08:00","Action":"pass","Package":"command-line-arguments","Elapsed":0.264}
"""

GO_PLAIN = "ok  \tcommand-line-arguments\t0.058s\n"

NODE_PASS = """\
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
\t<testcase name="adds" time="0.000269" classname="test" file="/work/repo/probes/attack.test.mjs"/>
\t<!-- tests 1 -->
\t<!-- suites 0 -->
\t<!-- pass 1 -->
\t<!-- fail 0 -->
\t<!-- cancelled 0 -->
\t<!-- skipped 0 -->
\t<!-- todo 0 -->
\t<!-- duration_ms 107.167042 -->
</testsuites>
"""

NODE_SKIP = """\
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
\t<testcase name="adds" time="0.000230" classname="test" file="/work/repo/probes/attack.test.mjs">
\t\t<skipped type="skipped" message="true"/>
\t</testcase>
\t<!-- tests 1 -->
\t<!-- suites 0 -->
\t<!-- pass 0 -->
\t<!-- fail 0 -->
\t<!-- cancelled 0 -->
\t<!-- skipped 1 -->
\t<!-- todo 0 -->
\t<!-- duration_ms 99.70725 -->
</testsuites>
"""

# A file that defines no test still reports one passing case named after it.
NODE_EMPTY = """\
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
\t<testcase name="probes/attack.test.mjs" time="0.095788" classname="test" file="/work/repo/probes/attack.test.mjs"/>
\t<!-- tests 1 -->
\t<!-- suites 0 -->
\t<!-- pass 1 -->
\t<!-- fail 0 -->
\t<!-- cancelled 0 -->
\t<!-- skipped 0 -->
\t<!-- todo 0 -->
\t<!-- duration_ms 98.857917 -->
</testsuites>
"""

NODE_SPEC_REPORTER = """\
✔ adds (0.245375ms)
ℹ tests 1
ℹ suites 0
ℹ pass 1
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 105.866625
"""

DENO_PASS = """\
\x1b[0m\x1b[32mCheck\x1b[0m probes/attack_test.ts
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="deno test" tests="1" failures="0" errors="0" time="0.001">
    <testsuite name="./probes/attack_test.ts" tests="1" disabled="0" errors="0" failures="0">
        <testcase name="adds" classname="./probes/attack_test.ts" time="0.000" line="1" col="6">
        </testcase>
    </testsuite>
</testsuites>
"""

DENO_SKIP = """\
\x1b[0m\x1b[32mCheck\x1b[0m probes/attack_test.ts
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="deno test" tests="1" failures="0" errors="0" time="0.001">
    <testsuite name="./probes/attack_test.ts" tests="1" disabled="1" errors="0" failures="0">
        <testcase name="adds" classname="./probes/attack_test.ts" time="0.000" line="1" col="6">
            <skipped/>
        </testcase>
    </testsuite>
</testsuites>
"""

DENO_PRETTY = """\
\x1b[0m\x1b[38;5;245mrunning 1 test from ./probes/attack_test.ts\x1b[0m
adds ... \x1b[0m\x1b[32mok\x1b[0m \x1b[0m\x1b[38;5;245m(189µs)\x1b[0m

\x1b[0m\x1b[32mok\x1b[0m | 1 passed | 0 failed \x1b[0m\x1b[38;5;245m(1ms)\x1b[0m

"""

BUN_PASS = """\
bun test v1.4.3 (26aa4e1a9)

 1 pass
 0 fail
 1 expect() calls
Ran 1 test across 1 file. [66.00ms]
"""

BUN_SKIP = """\
bun test v1.4.3 (26aa4e1a9)

 0 pass
 1 skip
 0 fail
Ran 1 test across 1 file. [3.00ms]
"""

# `bun test p.test.ts` treats the positional as a filter and ran three files.
BUN_MULTI_FILE = """\
bun test v1.4.3 (26aa4e1a9)

 2 pass
 1 skip
 0 fail
 2 expect() calls
Ran 3 tests across 3 files. [4.00ms]
"""

BUN_NO_SUMMARY = "bun test v1.4.3 (26aa4e1a9)\n"

UNITTEST_PASS = """\
test_adds (probe_pass.T.test_adds) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
"""

UNITTEST_SKIP = """\
test_adds (probe_skip.T.test_adds) ... skipped 'not now'

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK (skipped=1)
"""

UNITTEST_TRUNCATED = "test_adds (probe_pass.T.test_adds) ... ok\n"


def row_for(command: str, artifact: str):
    """The row claiming `command`, asserted to accept it."""
    argv = shlex.split(command)
    row = claiming_row(argv)
    assert row is not None, command
    assert row.accepts(argv, artifact), command
    return row


def test_go_json_passing_test_accepted() -> None:
    row = row_for(f"go test -json -v -race -count 1 -timeout=30s -tags integration {GO}", GO)
    assert row.passed(GO_PASS, GO) == 1


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"go test -json {GO}", GO, GO_SKIP),
    (f"node --test --test-reporter=junit {NODE}", NODE, NODE_SKIP),
    (f"deno test --reporter=junit {DENO}", DENO, DENO_SKIP),
    (f"bun test ./{BUN}", BUN, BUN_SKIP),
    (f"bun test ./{BUN}", BUN, BUN_MULTI_FILE),
    (f"python3 -m unittest -v {UNITTEST}", UNITTEST, UNITTEST_SKIP),
])
def test_go_all_skipped_refused(command: str, artifact: str, output: str) -> None:
    """A readable run with no passing test of the artifact -- all skipped, or
    a bun summary covering more than one file -- counts 0, a refusal."""
    assert row_for(command, artifact).passed(output, artifact) == 0


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"node --test --test-reporter=junit --experimental-strip-types {NODE}", NODE, NODE_PASS),
    (f"deno test --reporter=junit -A --allow-read=. {DENO}", DENO, DENO_PASS),
    (f"bun test ./{BUN}", BUN, BUN_PASS),
    (f"bun test /work/repo/{BUN}", BUN, BUN_PASS),
    (f"python3 -m unittest -v {UNITTEST}", UNITTEST, UNITTEST_PASS),
    (f"uv run --isolated python -m unittest -q {UNITTEST}", UNITTEST, UNITTEST_PASS),
    (f"conda run -n env python3.12 -m unittest {UNITTEST}", UNITTEST, UNITTEST_PASS),
])
def test_node_deno_bun_unittest_passing_accepted(command: str, artifact: str, output: str) -> None:
    assert row_for(command, artifact).passed(output, artifact) == 1


def test_node_empty_file_level_case_refused() -> None:
    row = row_for(f"node --test --test-reporter=junit {NODE}", NODE)
    assert row.passed(NODE_EMPTY, NODE) == 0


@pytest.mark.parametrize(("command", "artifact"), [
    (f"go test {GO}", GO),
    (f"go test -json {GO} probes/helper_test.go", GO),
    (f"go test -json -run TestNothing {GO}", GO),
    (f"go test -json ./... ", GO),
    (f"node --test {NODE}", NODE),
    (f"node --test --test-reporter=junit {NODE} probes/other.test.mjs", NODE),
    (f"node --test --test-reporter=junit --watch {NODE}", NODE),
    (f"deno test {DENO}", DENO),
    (f"deno test --reporter=junit --filter adds {DENO}", DENO),
    (f"bun test {BUN}", BUN),
    (f"bun test ./{BUN} ./probes/other.test.ts", BUN),
    (f"python3 -m unittest {UNITTEST} probes/other.py", UNITTEST),
    (f"python3 -m unittest -k adds {UNITTEST}", UNITTEST),
])
def test_listed_runner_without_output_flag_or_extra_file_refused(command: str, artifact: str) -> None:
    argv = shlex.split(command)
    row = claiming_row(argv)
    assert row is not None, command
    assert not row.accepts(argv, artifact), command


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"go test -json {GO}", GO, GO_PLAIN),
    (f"node --test --test-reporter=junit {NODE}", NODE, NODE_SPEC_REPORTER),
    (f"deno test --reporter=junit {DENO}", DENO, DENO_PRETTY),
    (f"bun test ./{BUN}", BUN, BUN_NO_SUMMARY),
    (f"python3 -m unittest {UNITTEST}", UNITTEST, UNITTEST_TRUNCATED),
])
def test_unreadable_output_needs_confirmation(command: str, artifact: str, output: str) -> None:
    assert row_for(command, artifact).passed(output, artifact) is None


# cargo test keeps its shape-only mapping in `probes` until it gets a row.
RUST = "tests/attack.rs"


def accepted(command: str, artifact: str) -> bool:
    return command_names_artifact(command, artifact) and command_executes_artifact(command, artifact)


@pytest.mark.parametrize("command", [
    "cargo test --test attack",
    "cargo test --release -q --test=attack",
    "cargo test --quiet --test attack",
])
def test_cargo_accepted(command: str) -> None:
    assert accepted(command, RUST)


@pytest.mark.parametrize("command", [
    "cargo test --test attack some_case",
    "cargo test --test attack -- --ignored",
    "cargo test --no-run --test attack",
    "cargo test --test other",
    "cargo test --test attack --test attack",
    "cargo build --test attack",
    "cargo test --doc --test attack",
])
def test_cargo_name_filter_refused(command: str) -> None:
    assert not accepted(command, RUST)
