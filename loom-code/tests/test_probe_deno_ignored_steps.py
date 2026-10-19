# concern: a deno test whose steps were all ignored must not count as a passing, non-skipped test.
"""Count only leaf deno test cases, as the go row already does for subtests."""

from __future__ import annotations

from loom_checker.probe_results import claiming_row

ARTIFACT = "p/ign.test.ts"

# Captured from deno 2.9.7: `deno test --reporter=junit p/ign.test.ts` where the file is
#   Deno.test("steps", async (t) => { await t.step({name: "s", ignore: true, fn() {}}); });
OUTPUT = """\
Check p/ign.test.ts
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="deno test" tests="2" failures="0" errors="0" time="0.002">
    <testsuite name="./p/ign.test.ts" tests="2" disabled="1" errors="0" failures="0">
        <testcase name="steps" classname="./p/ign.test.ts" time="0.000" line="1" col="6">
        </testcase>
        <testcase name="steps &gt; s" classname="./p/ign.test.ts" time="0.000" line="1" col="43">
            <skipped/>
        </testcase>
    </testsuite>
</testsuites>
"""


def test_deno_passed_all_steps_ignored_counts_zero() -> None:
    """A parent whose only step was ignored ran nothing, so the row counts zero."""
    row = claiming_row(["deno", "test", "--reporter=junit", ARTIFACT])
    assert row is not None and row.name == "deno"
    assert row.passed(OUTPUT, ARTIFACT) == 0
