# Build verification — advisory next steps

## Scope and identity

Worker verification on 2026-11-14 in the isolated change worktree, branch
`feat/2026-11-14-cli-next-guidance`, based on
`c271cc43d2bff6b34cd7012e260e58eeb42f0eaf`.
W1 implementation is commit `2211166988bff99732f43e4b75e64642a7f519fd`;
W2 guidance is commit `3e18c94471a31a866f85494f4095839f4bb63aa1`.
W3 checks below ran on that content plus the uncommitted release packet.
The orchestrator rechecked remote main at the same base before selecting
loom-code 3.78.0. Only the canonical Claude manifest was edited by hand;
the Codex, Antigravity and OpenCode manifests were generated from it.

These are implementer checks, not independent acceptance testing or a review
verdict. No installed plugin was updated, outside model invoked, publication
performed or efficiency gain measured. Installed-session behavior and host
installation parity remain unverified by this packet.

## Commands and observed results

All pytest calls used this existing locked environment prefix:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest
```

| Packet | Arguments after the prefix | Observed result | Retained local log |
|---|---|---|---|
| W1 RED | `loom-code/tests/test_preparation_json.py loom-code/tests/test_checked_readonly.py loom-code/tests/test_loom_checker_cli.py -q -rs` | 4 failed, 44 passed before implementation; missing advice fields/help caused the new assertions to fail | `/private/tmp/loom-next-w1-red.txt` |
| W1 GREEN | Same three complete files | 48 passed | `/private/tmp/loom-next-w1-green.txt` |
| W2 | `loom-code/tests/test_loom_runtime_skill_commands.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_closing_review_recovery_rules.py -q -rs` | 48 passed; no test edits | `/private/tmp/loom-next-w2-tests.txt` |
| W3 RED | `loom-code/tests/test_write_plan_station_text.py -q -rs` | 1 failed, 42 passed: pin expected 3.78.0 while canonical manifest still had 3.77.0 | `/private/tmp/loom-next-w3-red.txt` |
| W3 GREEN | Same complete file after release/localized parity | 43 passed | `/private/tmp/loom-next-w3-green.txt` |

The first W1 invocation could not acquire the existing uv cache lock under
the sandbox. The authorized cache-access invocation then produced the retained
behavioral RED above; a cache failure was not counted as a behavioral failure.
No packages were installed into a conda base environment.

Manifest derivation and verification:

```sh
python3 scripts/sync_codex_manifests.py --all
python3 scripts/sync_codex_manifests.py --all --check
git diff --check
```

Both manifest commands exited 0, retaining logs at
`/private/tmp/loom-next-w3-sync.txt` and
`/private/tmp/loom-next-w3-manifest-check.txt`. The diff check passed.
Historical changelog sections remain; localized README edits only change the
current version strings.

## Real source replay

The external temporary program `/private/tmp/loom-next-w2-replay.py` reused
`make_intent_state_repo` from the existing CLI tests. It ran the actual source
`loom-code/scripts/loom-python --ready --script checked_readonly.py` with:

| Operands / repository condition | Exit | Observation |
|---|---|---|
| `contract --require 2.1` | 0 | Passed, compatible true, null suggestion |
| `contract --require 2.99` | 1 | Blocked; original producer-update diagnostic and advice |
| `contract --require 0.5` | 1 | Blocked; original consuming-plugin diagnostic and advice |
| `contract --require bad` | 2 | Usage error with unavailable domain data and input advice |
| `reviewer-count fixture`, initial clean change | 0 | Reviewer floor 2, null suggestion |
| Same call after a committed usage clarification | 0 | Reviewer floor 1, null suggestion |
| Same call with outstanding work | 2 | Usage error, null domain data and work-preserving advice |

Replay command:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-next-w2-replay.py
```

All seven observations passed, with empty consumer stderr and a single JSON
stdout object per accepted observation. The retained combined log is
`/private/tmp/loom-next-w2-replay.txt`. This uses temporary fixtures and a ready
local runtime; it is not independent dogfood or a clean-install proof.
W1 tests separately exercised text/JSON parity, late internal faults, legacy
and unusable hints, raw numeric precision, invalid core results, startup 86,
execution faults and timeout. These remain worker-run tests.

## Measured delta and remaining verification

| Packet | Actual net lines | Earlier rough estimate |
|---|---|---|
| W1 source | +39 (41 added, 2 removed), three existing modules | +30–70 |
| W1 tests | +27 (33 added, 6 removed), three existing test modules | +40–100 |
| W2 guidance | +73 (75 added, 2 removed), five existing documents | +40–100 |

The estimates were not limits or measured effort. Extending existing cases
kept test growth below the estimate; no new source or test module, registry,
action framework or domain-policy change was introduced. Release metadata and
this evidence note are additional maintained content, not a claimed reduction.

Independent adversarial execution, the complete configured package suite,
clean-copy acceptance testing, distinct fresh-context reviewers, finalization
and CI remain pending at this worker handoff. Focused green checks do not
establish semantic acceptance, published availability or merge authorization.
