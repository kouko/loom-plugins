# Worker implementation and focused verification

Date: 2026-11-14. This records implementer checks, not independent acceptance,
closing-review verdicts, CI, or full-suite evidence. The confirmed intent and
spec own the bounded scope; the earlier rollout proposal remains historical.

## Implemented content and measured delta

| Task | Commit/content | Measured change |
|---|---|---|
| W1-01 | `1f350fbbb115a93632405e66bafb627dbd31e82d` | One 115-line production script; 127 new test lines plus 11 existing-runtime test lines, net 138 test lines |
| W2-01 | `0bc40067e5e292676130480b1c5485e75123d318` | Five documentation files, 177 insertions and 57 deletions, net +120 lines; no source/test edits |
| W3-01/02 | This release packet | Canonical 3.77.0 version and three derived manifests, dated changelog, README/version-pin parity and this worker record |

The historical proposal estimated roughly 40–80 source and 40–80 verification
lines for a first consumer batch. Actual W1 is 115/138: source exceeds its upper
estimate by 35 lines, tests by 58. These are physical maintained lines including
blank lines/docstrings, not time, token or monetary cost. The final design
retains one bounded script for two callers, no new checker command, registry,
dependency or general recovery framework. No speed or efficiency improvement
was measured or claimed.

## RED and GREEN observations

The focused runner uses the existing repository dependency lock and cached uv
artifacts, offline and isolated:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest <focused-files> -q -rs
```

The initial attempt to use an assumed uv project could not run pytest: there
is no project manifest, and `--locked` has no effect there. A cache sandbox
denial was resolved through authorized execution with the existing host cache;
no fresh cache or dependency download was introduced. These infrastructure
attempts are not counted as RED behavior evidence.

| Observation | Actual result | Local execution log |
|---|---|---|
| W1 new public entry before implementation | 2 failed: real CLI missing and public `main` unavailable | `/private/tmp/loom-consume-json-w1-red.txt` |
| W1 child interpreter isolation regression | 1 failed: real launcher under poisoned `PYTHONHOME`/`PYTHONPATH` returned consumer error instead of passed contract | `/private/tmp/loom-consume-json-w1-isolation-red.txt` |
| W1 compatible extension preservation regression | 1 failed, 1 passed: valid unknown `1e999`/high-precision data rejected by re-encoding | `/private/tmp/loom-consume-json-w1-extras-red.txt` |
| W1 final focused consumer + producer + runtime files | 19 passed | `/private/tmp/loom-consume-json-w1-green.txt` |
| W2 existing station safeguards | 79 passed | `/private/tmp/loom-consume-json-w2-tests.txt` |
| W3 existing current-release guard after pin change, before metadata | 1 failed: canonical version still 3.76.0 | `/private/tmp/loom-consume-json-w3-red.txt` |
| W3-01 before localized parity update | 2 failed, 41 passed: JA and zh-TW versions still 3.76.0 | `/private/tmp/loom-consume-json-w3-localized-red.txt` |

W1 focused files were `test_checked_readonly.py`, `test_preparation_json.py`
and `test_loom_python_runtime.py` under `loom-code/tests/`. The first file uses
public `main`, real CLI calls and the subprocess seam, never a direct private
validator test; it reuses the existing repository fixture. The other files
retain producer and runtime protections.

W2 focused files were `test_write_plan_station_text.py`,
`test_simplified_station_text.py` and `test_closing_review_recovery_rules.py`
under the same test directory. No new prose-pin tests were added.

### Corrected assumptions and precommit defect classes

- One initial test incorrectly rejected an arbitrary nonblank current contract
  version. It was corrected to reject whitespace; the consumer must not
  duplicate compatibility policy or require a second manifest value.
- A numeric boundary exploration initially treated unknown `1e999` as invalid
  (`/private/tmp/loom-consume-json-w1-numeric-red.txt`: 1 failed, 1 passed).
  That expectation was superseded: `1e999` is syntactically valid JSON, unlike
  literal NaN/Infinity. The retained public-entry test now requires accepting
  that extension and preserving numeric precision.
- Defect class: the child interpreter lost launcher import isolation. The
  orchestrator searched all three W1 files and cumulative intent/spec/plan and
  research/proposal surfaces for subprocess/interpreter/Python-environment
  handling, finding one production instance in `checked_readonly.main`.
  The regression went RED before adding `-E -s`; environment values remain
  present while Python ignores their import configuration.
- Defect class: re-encoding accepted extension data introduced failures and
  precision loss. The same bounded W1/documentation search identified one
  production normalization instance in `main` and the mistaken numeric test.
  After RED, the consumer emits strictly validated original JSON with only
  outer whitespace and the terminal newline normalized. This removes the
  unnecessary encoder instead of adding a numeric traversal/framework.

The two final defect-class reproductions provide behavior-level RED evidence
beyond the initial missing-entry failure. Initial failed attempts and historical
logs remain separate; none is described as passing evidence.

## Worker replay of documented calls

`/private/tmp/loom-consume-json-w2-examples.py` reuses the existing clean-repo
fixture and invokes the actual launcher/consumer, without mocking validation.
Its output is `/private/tmp/loom-consume-json-w2-examples.txt`. The first call
uses `--repair` against the already ready cached runtime; subsequent calls use
`--ready`. No install or installed-plugin update was performed.

| Real consumer operands | Exit and observation | Permitted interpretation |
|---|---|---|
| `contract --require 2.1` | 0, passed, compatible true | Compatibility prerequisite established |
| `contract --require 2.99` | 1, blocked, compatible false, `contract.requires` | Stop compatibility prerequisite; report actual diagnostic |
| `contract --require bad` | 2, error/usage, null known data | Stop; input failure is not incompatibility |
| exact script `--help` | 0, help text | Discovery only |
| `reviewer-count " example id "` on clean ordinary fixture | 0, passed, unchanged ID, floor 2 | Request two distinct reviewers; not completed review |
| Same call after committed narrow docs delta | 0, passed, floor 1 | Request one independent reviewer; no waiver |
| Same call after creating an untracked dirty file | 2, error/usage, null known data | No dispatch and no default floor |

Unit fault injection additionally covers malformed/contradictory JSON,
duplicate keys, wrong request identity, unexpected stderr, timeout and startup
86. This is not an actual 30-second elapsed-time measurement or an arbitrary
failure-recovery claim. Well-formed incorrect computational values can still
pass structural checks.

## Release and remaining verification

The orchestrator rechecked remote main as
`6fe61c99ea1981f238f8a8550abbd1e36e93cfab` before selecting 3.77.0. The worker
derives manifests with `python3 scripts/sync_codex_manifests.py --all` and checks
with `python3 scripts/sync_codex_manifests.py --all --check`. Localized edits
change version strings only. Historical changelog sections are preserved.

Final W3 verification ran the complete existing
`loom-code/tests/test_write_plan_station_text.py`: 43 passed in 0.20 seconds,
recorded in `/private/tmp/loom-consume-json-w3-green.txt`. Manifest sync check
and `git diff --check` also exited 0. This is focused release verification,
not the complete package suite.

Pending at this worker handoff: end-of-Build trunk synchronization, fresh
independent adversary, complete configured package suite, adversarial programs,
independent fresh-copy acceptance, closing reviewers, final attestation and CI.
No paid outside CLI/model, plugin refresh, live-host parity validation,
publication or merge was performed by these tasks. Five commands provide
direct JSON and two station consumers are checked; the remaining migration
work stays explicit in the portable CLI result inventory.

## End-of-Build repair: stale runtime station expectations

The subsequent complete-suite attempt failed, rather than establishing a full
pass: its code group reported 2 failed and 2,847 passed, and the runner exited
1 (`/private/tmp/loom-consume-json-build-suite.txt`). Both failures were in
`test_loom_runtime_skill_commands.py`, lines 23 and 41 at that time. They still
required the superseded direct contract invocation and old outdated-contract
sentence after W2 adopted checked observations.

Defect class: existing station expectations lagged the intended consumer
migration. The orchestrator searched all cumulative changed paths and the
Acceptance #2/#5 surfaces: all loom-code tests, write-plan/closing-review trees,
CLI result reference, READMEs, intent/spec/plan/research/evidence/proposal. The
search used old repair-contract/repair-reviewer invocations, the old Only
sentence and `contract.requires`. Exactly these two stale actionable instances
were found. Direct-producer runtime assertions and current valid rule references
were intentionally retained.

The worker reran the whole existing test file before editing: 2 failed, 1 passed
(`/private/tmp/loom-consume-json-runtime-alignment-red.txt`). The minimal repair
updates the launcher expectation and checks the accepted-blocked rule semantics
instead of pinning the replacement paragraph verbatim. Its inline affirmative
and negated synthetic examples protect the prose assertion's polarity, and
startup failure diagnostics remain separate. No production or adversary-owned
file changed; the W2 Files row records this discovered repair surface.

The same whole-file command after repair reported 3 passed in 0.01 seconds
(`/private/tmp/loom-consume-json-runtime-alignment-green.txt`):

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_runtime_skill_commands.py -q -rs
```

This focused GREEN does not replace the failed complete-suite result. The
orchestrator still owes a new complete-suite run and remaining independent
verification on the repaired content.
