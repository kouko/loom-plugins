"""The runner row table in `loom_checker.probe_results`: a row claims an argv
by runner identity, accepts only its documented form, and reads the run's own
output -- a count of passing, non-skipped tests from the artifact, 0 for a
readable run that shows none, None for output the row cannot read.

Every output constant below is real output captured from the installed
runner (go 1.27, node 26, deno 2.9, bun 1.4.3, python 3.12, jest 30.5.2,
vitest 4.1.12 and 5.0.5, mocha 12.0.3, rspec 3.13.6, ruby 2.6 minitest
5.11.3, phpunit 12.5.40 on php 8.5, cargo 1.99, cargo-nextest 0.9.148) on a
one-file probe; only the absolute scratch directory (shortened to
`/work/repo`) and the probe file's path (so one artifact constant serves each
row) were edited. bun prints its summary on stderr, so its constants are
stdout then stderr; so are cargo's, and nextest prints only on stderr. The
jest, vitest, mocha and rspec constants are their stdout, where the JSON
report goes.
"""
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

import pytest

from loom_checker.probe_results import ROWS, claiming_row
from loom_checker.attestation import adversarial_route

GO = "probes/add_test.go"
NODE = "probes/attack.test.mjs"
DENO = "probes/attack_test.ts"
BUN = "probes/p.test.ts"
UNITTEST = "probes/probe_pass.py"
JS = "probes/attack.test.js"
VITEST = "probes/attack.test.mjs"
RSPEC = "spec/attack_spec.rb"
MINITEST = "probes/attack_test.rb"
PHPUNIT = "tests/AttackTest.php"
RUST = "tests/attack.rs"
RUST_MAPPED = "probes/mapped.rs"

CARGO_TOML = """\
[package]
name = "demo"
version = "0.1.0"

[[test]]
name = "mapped"
path = "probes/mapped.rs"
"""


@pytest.fixture(scope="module")
def repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A repository root whose Cargo.toml maps `--test mapped` to a non-default
    path, with an auto-discovered `tests/dir/main.rs` target named `dir`."""
    root = tmp_path_factory.mktemp("repo")
    (root / "Cargo.toml").write_text(CARGO_TOML, encoding="utf-8")
    (root / "tests/dir").mkdir(parents=True)
    (root / "tests/dir/main.rs").write_text("#[test]\nfn t() {}\n", encoding="utf-8")
    return root

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

# deno 2.9.7, a `t.step` parent whose only step is ignored: the parent case
# carries no <skipped/> of its own.
DENO_IGNORED_STEPS = """\
Check probes/attack_test.ts
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="deno test" tests="2" failures="0" errors="0" time="0.002">
    <testsuite name="./probes/attack_test.ts" tests="2" disabled="1" errors="0" failures="0">
        <testcase name="steps" classname="./probes/attack_test.ts" time="0.000" line="1" col="6">
        </testcase>
        <testcase name="steps &gt; s" classname="./probes/attack_test.ts" time="0.000" line="1" col="43">
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

JEST_PASS = """\
{"numFailedTestSuites":0,"numFailedTests":0,"numPassedTestSuites":1,"numPassedTests":1,"numPendingTestSuites":0,"numPendingTests":0,"numRuntimeErrorTestSuites":0,"numTodoTests":0,"numTotalTestSuites":1,"numTotalTests":1,"openHandles":[],"snapshot":{"added":0,"didUpdate":false,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0},"startTime":1792213235055,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"duration":0,"failing":false,"failureDetails":[],"failureMessages":[],"fullName":"adds","invocations":1,"location":null,"numPassingAsserts":1,"retryMessages":[],"retryReasons":[],"status":"passed","title":"adds","startAt":1792213235251}],"endTime":1792213235252,"message":"","name":"/work/repo/probes/attack.test.js","startTime":1792213235130,"status":"passed","summary":""}],"wasInterrupted":false}
"""

JEST_SKIP = """\
{"numFailedTestSuites":0,"numFailedTests":0,"numPassedTestSuites":0,"numPassedTests":0,"numPendingTestSuites":1,"numPendingTests":1,"numRuntimeErrorTestSuites":0,"numTodoTests":0,"numTotalTestSuites":1,"numTotalTests":1,"openHandles":[],"snapshot":{"added":0,"didUpdate":false,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0},"startTime":1792213468574,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"duration":null,"failing":false,"failureDetails":[],"failureMessages":[],"fullName":"adds","invocations":1,"location":null,"numPassingAsserts":0,"retryMessages":[],"retryReasons":[],"status":"pending","title":"adds","startAt":1792213468675}],"coverage":{},"endTime":1792213468677,"message":"","name":"/work/repo/probes/attack.test.js","startTime":1792213468677,"status":"skipped","summary":""}],"wasInterrupted":false}
"""

JEST_OTHER = """\
{"numFailedTestSuites":0,"numFailedTests":0,"numPassedTestSuites":1,"numPassedTests":1,"numPendingTestSuites":0,"numPendingTests":0,"numRuntimeErrorTestSuites":0,"numTodoTests":0,"numTotalTestSuites":1,"numTotalTests":1,"openHandles":[],"snapshot":{"added":0,"didUpdate":false,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0},"startTime":1792213236502,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"duration":0,"failing":false,"failureDetails":[],"failureMessages":[],"fullName":"other","invocations":1,"location":null,"numPassingAsserts":1,"retryMessages":[],"retryReasons":[],"status":"passed","title":"other","startAt":1792213236660}],"endTime":1792213236661,"message":"","name":"/work/repo/probes/other.test.js","startTime":1792213236559,"status":"passed","summary":""}],"wasInterrupted":false}
"""

# jest without --json: the summary goes to stderr and names no test.
JEST_PLAIN = """\
Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
Time:        0.134 s, estimated 1 s
Ran all test suites within paths "probes/attack.test.js".
"""

VITEST_PASS = """\
{"numTotalTestSuites":1,"numPassedTestSuites":1,"numFailedTestSuites":0,"numPendingTestSuites":0,"numTotalTests":1,"numPassedTests":1,"numFailedTests":0,"numPendingTests":0,"numTodoTests":0,"snapshot":{"added":0,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0,"didUpdate":false},"startTime":1792213286270,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"fullName":"adds","status":"passed","title":"adds","duration":0.4820409999999953,"failureMessages":[],"meta":{},"tags":[]}],"startTime":1792213286424,"endTime":1792213286424.482,"status":"passed","message":"","name":"/work/repo/probes/attack.test.mjs"}]}
"""

VITEST_SKIP = """\
{"numTotalTestSuites":1,"numPassedTestSuites":1,"numFailedTestSuites":0,"numPendingTestSuites":0,"numTotalTests":1,"numPassedTests":0,"numFailedTests":0,"numPendingTests":1,"numTodoTests":0,"snapshot":{"added":0,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0,"didUpdate":false},"startTime":1792213286951,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"fullName":"adds","status":"skipped","title":"adds","failureMessages":[],"meta":{},"tags":[]}],"startTime":1792213286951,"endTime":1792213286951,"status":"passed","message":"","name":"/work/repo/probes/attack.test.mjs"}]}
"""

VITEST_OTHER = """\
{"numTotalTestSuites":1,"numPassedTestSuites":1,"numFailedTestSuites":0,"numPendingTestSuites":0,"numTotalTests":1,"numPassedTests":1,"numFailedTests":0,"numPendingTests":0,"numTodoTests":0,"snapshot":{"added":0,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0,"didUpdate":false},"startTime":1792213287647,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"fullName":"other","status":"passed","title":"other","duration":0.5883329999999987,"failureMessages":[],"meta":{},"tags":[]}],"startTime":1792213287794,"endTime":1792213287794.5884,"status":"passed","message":"","name":"/work/repo/probes/other.test.mjs"}]}
"""

# vitest 5 with `--outputFile=/dev/stdout`: the report, then where it went.
VITEST5_PASS = """\
{"numTotalTestSuites":1,"numPassedTestSuites":1,"numFailedTestSuites":0,"numPendingTestSuites":0,"numTotalTests":1,"numPassedTests":1,"numFailedTests":0,"numPendingTests":0,"numTodoTests":0,"snapshot":{"added":0,"failure":false,"filesAdded":0,"filesRemoved":0,"filesRemovedList":[],"filesUnmatched":0,"filesUpdated":0,"matched":0,"total":0,"unchecked":0,"uncheckedKeysByFile":[],"unmatched":0,"updated":0,"didUpdate":false},"startTime":1792213936659,"success":true,"testResults":[{"assertionResults":[{"ancestorTitles":[],"fullName":"adds","status":"passed","title":"adds","duration":0.5542919999999967,"failureMessages":[],"meta":{},"tags":[],"benchmarks":[]}],"startTime":1792213936815,"endTime":1792213936815.5542,"status":"passed","message":"","name":"/work/repo/probes/attack.test.mjs"}]}JSON report written to /dev/stdout
"""

# vitest 5 without `--outputFile` writes the JSON report to a file and prints
# only where it went.
VITEST5_FILE_REPORT = "JSON report written to /work/repo/.vitest/json/output.json\n"

MOCHA_PASS = """\
{
  "stats": {
    "suites": 0,
    "tests": 1,
    "passes": 1,
    "pending": 0,
    "failures": 0,
    "start": "2026-10-17T05:01:39.223Z",
    "end": "2026-10-17T05:01:39.225Z",
    "duration": 2
  },
  "tests": [
    {
      "title": "adds",
      "fullTitle": "adds",
      "file": "/work/repo/probes/attack.test.js",
      "duration": 0,
      "currentRetry": 0,
      "speed": "fast",
      "err": {}
    }
  ],
  "pending": [],
  "failures": [],
  "passes": [
    {
      "title": "adds",
      "fullTitle": "adds",
      "file": "/work/repo/probes/attack.test.js",
      "duration": 0,
      "currentRetry": 0,
      "speed": "fast",
      "err": {}
    }
  ]
}"""

MOCHA_SKIP = """\
{
  "stats": {
    "suites": 0,
    "tests": 1,
    "passes": 0,
    "pending": 1,
    "failures": 0,
    "start": "2026-10-17T05:01:39.395Z",
    "end": "2026-10-17T05:01:39.396Z",
    "duration": 1
  },
  "tests": [
    {
      "title": "adds",
      "fullTitle": "adds",
      "file": "/work/repo/probes/attack.test.js",
      "currentRetry": 0,
      "err": {}
    }
  ],
  "pending": [
    {
      "title": "adds",
      "fullTitle": "adds",
      "file": "/work/repo/probes/attack.test.js",
      "currentRetry": 0,
      "err": {}
    }
  ],
  "failures": [],
  "passes": []
}"""

MOCHA_OTHER = """\
{
  "stats": {
    "suites": 0,
    "tests": 1,
    "passes": 1,
    "pending": 0,
    "failures": 0,
    "start": "2026-10-17T05:01:39.573Z",
    "end": "2026-10-17T05:01:39.574Z",
    "duration": 1
  },
  "tests": [
    {
      "title": "other",
      "fullTitle": "other",
      "file": "/work/repo/probes/other.test.js",
      "duration": 0,
      "currentRetry": 0,
      "speed": "fast",
      "err": {}
    }
  ],
  "pending": [],
  "failures": [],
  "passes": [
    {
      "title": "other",
      "fullTitle": "other",
      "file": "/work/repo/probes/other.test.js",
      "duration": 0,
      "currentRetry": 0,
      "speed": "fast",
      "err": {}
    }
  ]
}"""

MOCHA_SPEC_REPORTER = """\


  ✔ adds

  1 passing (1ms)

"""

RSPEC_PASS = '{"version":"3.13.6","examples":[{"id":"./spec/attack_spec.rb[1:1]","description":"adds","full_description":"math adds","status":"passed","file_path":"./spec/attack_spec.rb","line_number":2,"run_time":0.000434,"pending_message":null}],"summary":{"duration":0.001086,"example_count":1,"failure_count":0,"pending_count":0,"errors_outside_of_examples_count":0},"summary_line":"1 example, 0 failures"}'

RSPEC_SKIP = '{"version":"3.13.6","examples":[{"id":"./spec/attack_spec.rb[1:1]","description":"adds","full_description":"math adds","status":"pending","file_path":"./spec/attack_spec.rb","line_number":2,"run_time":3.2e-05,"pending_message":"not now"}],"summary":{"duration":0.000563,"example_count":1,"failure_count":0,"pending_count":1,"errors_outside_of_examples_count":0},"summary_line":"1 example, 0 failures, 1 pending"}'

RSPEC_OTHER = '{"version":"3.13.6","examples":[{"id":"./spec/other_spec.rb[1:1]","description":"holds","full_description":"other holds","status":"passed","file_path":"./spec/other_spec.rb","line_number":2,"run_time":0.000326,"pending_message":null}],"summary":{"duration":0.000868,"example_count":1,"failure_count":0,"pending_count":0,"errors_outside_of_examples_count":0},"summary_line":"1 example, 0 failures"}'

RSPEC_PROGRESS = """\
.

Finished in 0.00219 seconds (files took 0.05392 seconds to load)
1 example, 0 failures

"""

MINITEST_PASS = """\
Run options: --seed 32141

# Running:

.

Finished in 0.000180s, 5555.5555 runs/s, 5555.5555 assertions/s.

1 runs, 1 assertions, 0 failures, 0 errors, 0 skips
"""

MINITEST_SKIP = """\
Run options: --seed 53938

# Running:

S

Finished in 0.000168s, 5952.3810 runs/s, 0.0000 assertions/s.

1 runs, 0 assertions, 0 failures, 0 errors, 1 skips

You have skipped tests. Run with --verbose for details.
"""

# A file that never loads minitest/autorun prints no summary at all.
MINITEST_NO_AUTORUN = "no tests here\n"

PHPUNIT_PASS = """\
PHPUnit 12.5.40 by Sebastian Bergmann and contributors.

Runtime:       PHP 8.5.11

.                                                                   1 / 1 (100%)

Time: 00:00, Memory: 28.06 MB

OK (1 test, 1 assertion)
"""

PHPUNIT_SKIP = """\
PHPUnit 12.5.40 by Sebastian Bergmann and contributors.

Runtime:       PHP 8.5.11

S                                                                   1 / 1 (100%)

Time: 00:00, Memory: 28.06 MB

OK, but some tests were skipped!
Tests: 1, Assertions: 0, Skipped: 1.
"""

# `phpunit --no-output` (also settable in phpunit.xml) prints nothing.
PHPUNIT_SILENT = ""

CARGO_PASS = """\

running 1 test
test adds ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running tests/attack.rs (/work/repo/target/debug/deps/attack-ed7edd16ae06ba46)
"""

CARGO_QUIET_PASS = """\

running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

"""

CARGO_IGNORED = """\

running 1 test
test adds ... ignored

test result: ok. 0 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.00s

    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.01s
     Running tests/attack.rs (/work/repo/target/debug/deps/attack-2538617edb793ee5)
"""

CARGO_COMPILE_ERROR = """\
error[E0425]: cannot find value `two` in this scope
 --> tests/attack.rs:3:23
  |
3 |     assert_eq!(1 + 1, two);
  |                       ^^^ not found in this scope

For more information about this error, try `rustc --explain E0425`.
error: could not compile `demo` (test "attack") due to 1 previous error
"""

NEXTEST_PASS = """\
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
────────────
 Nextest run ID e4948f7b-7b89-4e0d-bf27-5ab175ad2a21 with nextest profile: default
    Starting 1 test across 1 binary
        PASS [   0.007s] (1/1) demo::attack adds
────────────
     Summary [   0.007s] 1 test run: 1 passed, 0 skipped
"""

NEXTEST_IGNORED = """\
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
────────────
 Nextest run ID 2c4e84cf-8f19-4c1b-a817-1afc123690c6 with nextest profile: default
    Starting 0 tests across 1 binary (1 test skipped)
────────────
     Summary [   0.000s] 0 tests run: 0 passed, 1 skipped
error: no tests to run
(hint: use `--no-tests` to customize)
"""

NEXTEST_COMPILE_ERROR = """\
   Compiling demo v0.1.0 (/work/repo)
error[E0425]: cannot find value `two` in this scope
 --> tests/attack.rs:3:23
  |
3 |     assert_eq!(1 + 1, two);
  |                       ^^^ not found in this scope

For more information about this error, try `rustc --explain E0425`.
error: could not compile `demo` (test "attack") due to 1 previous error
error: command `/opt/homebrew/bin/cargo '--color=auto' test --no-run --message-format json-render-diagnostics --test attack` exited with code 101
"""


def row_for(command: str, artifact: str, repo: Path | None = None):
    """The row claiming `command`, asserted to accept it."""
    argv = shlex.split(command)
    row = claiming_row(argv)
    assert row is not None, command
    assert row.accepts(argv, artifact, repo), command
    return row


def test_go_json_passing_test_accepted() -> None:
    row = row_for(f"go test -json -v -race -count 1 -timeout=30s -tags integration {GO}", GO)
    assert row.passed(GO_PASS, GO) == 1


def test_go_package_probe_uses_siblings_and_exact_artifact_test(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "go-repo"
    package = root / "internal/pipeline"
    package.mkdir(parents=True)
    (root / "go.mod").write_text("module example.test/probe\n\ngo 1.23\n", encoding="utf-8")
    (package / "extraction.go").write_text(
        "package pipeline\nfunc extractWithFallback() string { return \"article\" }\n", encoding="utf-8")
    (package / "extraction_test.go").write_text(
        'package pipeline\nfunc stubExtractor() string { return extractWithFallback() }\n',
        encoding="utf-8")
    artifact = "internal/pipeline/adversarial_test.go"
    (root / artifact).write_text(
        'package pipeline\nimport "testing"\n'
        'func TestAdversarial(t *testing.T) { if stubExtractor() != "article" { t.Fatal("wrong") } }\n',
        encoding="utf-8")
    (package / "other_test.go").write_text(
        'package pipeline\nimport "testing"\nfunc TestOther(t *testing.T) {}\n',
        encoding="utf-8")
    monkeypatch.setenv("GOCACHE", str(tmp_path / "go-cache"))
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", "fixture"], cwd=root, check=True)
    command = "go test -json -count=1 -run '^TestAdversarial$' ./internal/pipeline"
    route, row = adversarial_route(command, artifact, root)
    assert route == "parsed" and row is not None
    result = subprocess.run(shlex.split(command), cwd=root, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert row.passed(result.stdout, artifact) == 1
    single = subprocess.run(["go", "test", artifact], cwd=root, text=True, capture_output=True)
    assert single.returncode != 0
    assert "undefined" in single.stdout + single.stderr

    other = 'go test -json -count=1 -run "^TestOther$" ./internal/pipeline'
    assert adversarial_route(other, artifact, root)[0] == "not-accepted"
    assert adversarial_route(command.replace("-count=1 ", ""), artifact, root)[0] == "not-accepted"
    assert adversarial_route(command.replace("./internal/pipeline", "./..."), artifact, root)[0] == "not-accepted"
    assert row.passed(GO_SKIP.replace("TestAdd", "TestAdversarial"), artifact) == 0
    assert row.passed(GO_PASS.replace("TestAdd", "TestOther"), artifact) == 0

    original = (root / artifact).read_text(encoding="utf-8")
    (root / artifact).write_text("//go:build never\n\n" + original, encoding="utf-8")
    subprocess.run(["git", "add", artifact], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", "excluded artifact"], cwd=root, check=True)
    assert adversarial_route(command, artifact, root)[0] == "not-accepted"
    (root / artifact).write_text(original, encoding="utf-8")
    subprocess.run(["git", "add", artifact], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", "restore artifact"], cwd=root, check=True)

    (package / "duplicate_test.go").write_text(
        'package pipeline_test\nimport tt "testing"\nfunc TestAdversarial(t *tt.T) {}\n',
        encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", "duplicate test name"], cwd=root, check=True)
    assert adversarial_route(command, artifact, root)[0] == "not-accepted"


def test_go_package_names_and_skipped_parent_follow_go_discovery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "go-names"
    root.mkdir()
    (root / "go.mod").write_text("module example.test/names\n\ngo 1.23\n", encoding="utf-8")
    artifact = "adversarial_test.go"
    (root / artifact).write_text(
        'package names\nimport tt "testing"\n'
        'func Test(t *tt.T) {}\n'
        'func Test1(t *tt.T) {}\n'
        'func TestΩ(t *tt.T) {}\n'
        'func TestSkipParent(t *tt.T) {\n'
        '  t.Run("passed_child", func(t *tt.T) {})\n'
        '  t.Skip("parent skipped")\n}\n', encoding="utf-8")
    monkeypatch.setenv("GOCACHE", str(tmp_path / "cache"))
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", "fixture"], cwd=root, check=True)
    for name in ("Test", "Test1", "TestΩ", "TestSkipParent"):
        command = f"go test -json -count=1 -run '^{name}$' ."
        route, row = adversarial_route(command, artifact, root)
        assert route == "parsed" and row is not None, name
        result = subprocess.run(shlex.split(command), cwd=root, text=True, capture_output=True)
        assert result.returncode == 0, result.stderr
        assert row.passed(result.stdout, artifact) == (0 if name == "TestSkipParent" else 1)
    for pattern in ("^Test1|TestΩ$", "^Test.*$", "^Testicular$"):
        assert adversarial_route(
            f"go test -json -count=1 -run '{pattern}' .", artifact, root,
        )[0] != "parsed"


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"go test -json {GO}", GO, GO_SKIP),
    (f"node --test --test-reporter=junit {NODE}", NODE, NODE_SKIP),
    (f"deno test --reporter=junit {DENO}", DENO, DENO_SKIP),
    (f"deno test --reporter=junit {DENO}", DENO, DENO_IGNORED_STEPS),
    (f"/opt/homebrew/bin/go test -json {GO}", GO, GO_SKIP),
    (f"bun test ./{BUN}", BUN, BUN_SKIP),
    (f"bun test ./{BUN}", BUN, BUN_MULTI_FILE),
    (f"python3 -m unittest -v {UNITTEST}", UNITTEST, UNITTEST_SKIP),
    (f"npx jest --json --runTestsByPath {JS}", JS, JEST_SKIP),
    (f"vitest run --reporter=json --outputFile=/dev/stdout {VITEST}", VITEST, VITEST_SKIP),
    (f"mocha --reporter json {JS}", JS, MOCHA_SKIP),
    (f"rspec --format json {RSPEC}", RSPEC, RSPEC_SKIP),
    (f"ruby {MINITEST}", MINITEST, MINITEST_SKIP),
    (f"phpunit {PHPUNIT}", PHPUNIT, PHPUNIT_SKIP),
    ("cargo test --test attack", RUST, CARGO_IGNORED),
    ("cargo nextest run --test attack", RUST, NEXTEST_IGNORED),
])
def test_listed_runner_no_passing_test_counts_zero(command: str, artifact: str, output: str, repo: Path) -> None:
    """A readable run with no passing test of the artifact -- all skipped, or
    a bun summary covering more than one file -- counts 0, a refusal."""
    assert row_for(command, artifact, repo).passed(output, artifact) == 0


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"node --test --test-reporter=junit --experimental-strip-types {NODE}", NODE, NODE_PASS),
    (f"deno test --reporter=junit -A --allow-read=. {DENO}", DENO, DENO_PASS),
    (f"bun test ./{BUN}", BUN, BUN_PASS),
    (f"python3 -m unittest -v {UNITTEST}", UNITTEST, UNITTEST_PASS),
    (f"uv run --isolated python -m unittest -q {UNITTEST}", UNITTEST, UNITTEST_PASS),
    (f"conda run -n env python3.12 -m unittest {UNITTEST}", UNITTEST, UNITTEST_PASS),
])
def test_node_deno_bun_unittest_passing_accepted(command: str, artifact: str, output: str) -> None:
    assert row_for(command, artifact).passed(output, artifact) == 1


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"npx jest --json --runTestsByPath {JS}", JS, JEST_PASS),
    (f"pnpm exec vitest run --reporter=json --outputFile=/dev/stdout {VITEST}", VITEST, VITEST_PASS),
    (f"npx vitest run --outputFile /dev/stdout --reporter=json {VITEST}", VITEST, VITEST5_PASS),
    (f"yarn mocha --reporter json {JS}", JS, MOCHA_PASS),
    (f"bundle exec rspec --format json {RSPEC}", RSPEC, RSPEC_PASS),
    (f"bundle exec ruby -Ilib -Itest {MINITEST}", MINITEST, MINITEST_PASS),
    (f"vendor/bin/phpunit {PHPUNIT}", PHPUNIT, PHPUNIT_PASS),
    (f"/usr/local/bin/phpunit {PHPUNIT}", PHPUNIT, PHPUNIT_PASS),
    ("cargo test --test attack", RUST, CARGO_PASS),
    ("cargo test --release -q --test=attack", RUST, CARGO_QUIET_PASS),
    ("cargo test --test mapped", RUST_MAPPED, CARGO_PASS),
    ("cargo test --test dir", "tests/dir/main.rs", CARGO_PASS),
    ("cargo nextest run --release --no-tests=fail --test attack", RUST, NEXTEST_PASS),
    ("cargo nextest run --no-tests fail --test mapped", RUST_MAPPED, NEXTEST_PASS),
])
def test_js_ruby_php_rust_passing_accepted(command: str, artifact: str, output: str, repo: Path) -> None:
    assert row_for(command, artifact, repo).passed(output, artifact) == 1


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"env go test -json {GO}", GO, GO_PASS),
    (f"env A=1 B=2 go test -json {GO}", GO, GO_PASS),
    (f"npx --yes jest --json --runTestsByPath {JS}", JS, JEST_PASS),
    (f"env CI=1 pnpm jest --json --runTestsByPath {JS}", JS, JEST_PASS),
])
def test_env_go_npx_yes_pnpm_jest_parsed(command: str, artifact: str, output: str) -> None:
    """A leading `env NAME=value...` and the `npx --yes` / bare `pnpm`
    launchers reach the row the bare runner would."""
    assert row_for(command, artifact).passed(output, artifact) == 1


@pytest.mark.parametrize("command", [
    f"env -i go test -json {GO}",
    f"env -u HOME A=1 go test -json {GO}",
    "env",
    "env A=1",
    f"pnpm test {JS}",
])
def test_env_option_or_pnpm_script_name_refused_or_confirmed(command: str) -> None:
    """An `env` option, an `env` with no command, or a pnpm script name is
    claimed by no row: a reviewer confirms it."""
    assert claiming_row(shlex.split(command)) is None, command


@pytest.mark.parametrize(("command", "artifact"), [
    (f"env GOFLAGS=-run=X go test -json {GO}", GO),
    (f"env CI=1 NODE_OPTIONS=--test-name-pattern=x node --test --test-reporter=junit {NODE}", NODE),
])
def test_env_runner_configuration_variable_refused(command: str, artifact: str) -> None:
    """A runner-configuration assignment can filter what the form refuses:
    claimed by the row, and refused."""
    argv = shlex.split(command)
    row = claiming_row(argv)
    assert row is not None and not row.accepts(argv, artifact), command


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"jest --json --runTestsByPath {JS}", JS, JEST_OTHER),
    (f"npx vitest run --reporter=json --outputFile=/dev/stdout {VITEST}", VITEST, VITEST_OTHER),
    (f"npx mocha --reporter json {JS}", JS, MOCHA_OTHER),
    (f"rspec --format json {RSPEC}", RSPEC, RSPEC_OTHER),
])
def test_results_from_another_file_refused(command: str, artifact: str, output: str) -> None:
    assert row_for(command, artifact).passed(output, artifact) == 0


@pytest.mark.parametrize("command", [
    "cargo nextest run --test attack --no-tests=warn",
    "cargo nextest run --no-tests pass --test attack",
    "cargo nextest run --no-tests=fail --no-tests=warn --test attack",
    "cargo nextest run --no-tests --test attack",
])
def test_nextest_no_tests_not_fail_refused(command: str, repo: Path) -> None:
    argv = shlex.split(command)
    row = claiming_row(argv)
    assert row is not None and not row.accepts(argv, RUST, repo), command


def test_bun_absolute_target_refused(repo: Path, tmp_path: Path) -> None:
    """An absolute bun target is refused inside the repository or out: the
    recorded command must re-run from another checkout."""
    inside = ["bun", "test", str(repo / BUN)]
    row = claiming_row(inside)
    assert not row.accepts(inside, BUN, repo)
    assert not row.accepts(["bun", "test", str(tmp_path / "other-checkout" / BUN)], BUN, repo)


def test_node_empty_file_level_case_refused() -> None:
    row = row_for(f"node --test --test-reporter=junit {NODE}", NODE)
    assert row.passed(NODE_EMPTY, NODE) == 0


@pytest.mark.parametrize(("command", "artifact"), [
    (f"go test {GO}", GO),
    (f"go test -json {GO} probes/helper_test.go", GO),
    (f"go test -json -run TestNothing {GO}", GO),
    (f"/opt/homebrew/bin/go test -json -run X {GO}", GO),
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
    (f"npx jest --runTestsByPath {JS}", JS),
    (f"npx jest --json {JS}", JS),
    (f"npx jest --json --runTestsByPath {JS} -t adds", JS),
    (f"vitest --reporter=json --outputFile=/dev/stdout {VITEST}", VITEST),
    (f"vitest run --reporter=json --outputFile=/dev/stdout {VITEST} probes/other.test.mjs", VITEST),
    (f"vitest run --reporter=json {VITEST}", VITEST),
    (f"vitest run --reporter=json --outputFile=out.json {VITEST}", VITEST),
    (f"mocha {JS}", JS),
    (f"mocha --reporter json --grep adds {JS}", JS),
    (f"rspec {RSPEC}", RSPEC),
    (f"rspec --format json --dry-run {RSPEC}", RSPEC),
    (f"ruby {MINITEST} -n test_adds", MINITEST),
    (f"ruby -e 1 {MINITEST}", MINITEST),
    (f"phpunit --filter testAdds {PHPUNIT}", PHPUNIT),
    (f"phpunit {PHPUNIT} tests/OtherTest.php", PHPUNIT),
    (f"/usr/local/bin/phpunit {PHPUNIT} tests/OtherTest.php", PHPUNIT),
    ("cargo test --test attack some_case", RUST),
    ("cargo test --test attack -- --ignored", RUST),
    ("cargo test --no-run --test attack", RUST),
    ("cargo test --test other", RUST),
    ("cargo test --test attack --test attack", RUST),
    ("cargo test --doc --test attack", RUST),
    ("cargo test --test mapped", "tests/mapped.rs"),
    ("cargo nextest list --test attack", RUST),
    ("cargo nextest run --test attack -E all()", RUST),
    (f"go vet -json {GO}", GO),
    (f"go run {GO}", GO),
    (f"deno check --reporter=junit {DENO}", DENO),
    (f"deno run {DENO}", DENO),
    (f"bun build --target=bun ./{BUN}", BUN),
    (f"bun ./{BUN}", BUN),
    ("cargo build --test attack", RUST),
    ("cargo run", RUST),
])
def test_listed_runner_without_output_flag_or_extra_file_refused(
    command: str, artifact: str, repo: Path
) -> None:
    """Any other subcommand of go, deno, bun or cargo is that runner in
    another form: claimed by exactly one row, and refused."""
    argv = shlex.split(command)
    row = claiming_row(argv)
    assert row is not None, command
    assert [r.name for r in ROWS if r.claims(argv)] == [row.name], command
    assert not row.accepts(argv, artifact, repo), command


@pytest.mark.parametrize(("command", "artifact", "output"), [
    (f"go test -json {GO}", GO, GO_PLAIN),
    (f"node --test --test-reporter=junit {NODE}", NODE, NODE_SPEC_REPORTER),
    (f"deno test --reporter=junit {DENO}", DENO, DENO_PRETTY),
    (f"bun test ./{BUN}", BUN, BUN_NO_SUMMARY),
    (f"python3 -m unittest {UNITTEST}", UNITTEST, UNITTEST_TRUNCATED),
    (f"npx jest --json --runTestsByPath {JS}", JS, JEST_PLAIN),
    (f"npx vitest run --reporter=json --outputFile=/dev/stdout {VITEST}", VITEST, VITEST5_FILE_REPORT),
    (f"npx mocha --reporter json {JS}", JS, MOCHA_SPEC_REPORTER),
    (f"rspec --format json {RSPEC}", RSPEC, RSPEC_PROGRESS),
    (f"ruby {MINITEST}", MINITEST, MINITEST_NO_AUTORUN),
    (f"phpunit {PHPUNIT}", PHPUNIT, PHPUNIT_SILENT),
    ("cargo test -q --test attack", RUST, CARGO_COMPILE_ERROR),
    ("cargo nextest run --no-tests=fail --test attack", RUST, NEXTEST_COMPILE_ERROR),
])
def test_unreadable_output_needs_confirmation(command: str, artifact: str, output: str, repo: Path) -> None:
    assert row_for(command, artifact, repo).passed(output, artifact) is None
