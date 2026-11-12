# Supplemental CLI dogfood — 2026-11-12

This publication evidence does not change the acceptance requirements or the reviewed functional content.

## Supplemental review

A fresh same-platform reviewer examined target `d705661a038818380bb8a2c30cd16c23608e41fd` against base `70a05fd73b86c6629a89b816fc45a3ad14a509ed`, without reading prior verdicts. Result: PASS_WITH_NOTES, no new findings; 185 tests passed with no skips. Historical RED output was unavailable. The earlier nonblocking module-entry test suggestion remains in the attestation. See [supplemental verdict](supplemental-code-review.yaml).

## Actual source execution

A fresh executor used a disposable local clone at `fe64dfa7ef283be4becfa95f4b0a3c1fce542a10`, the exact target of the authentic retained review input, with the same functional content as the delivered branch. It invoked the clone's version 3.67.0 source launcher, not the installed host plugin:

```text
./loom-code/scripts/loom-python --ready finalize-review 2026-11-11-agent-tool-efficiency --input <authentic-review-input.json>
```

The input preserved original reviewer identities, verdicts, targets and commands. Its SHA-256 was `64c8f1928c43de9d67433aad68b2fce68f20ee067f129f500cbfaec15cf489ac`.

| Observed event | Seconds | Channel | Parent alive |
|---|---:|---|---|
| package-tests started | 2.885 | stderr | yes |
| package-tests passed | 179.115 | stderr | yes |
| adversarial started | 179.116 | stderr | yes |
| adversarial passed | 231.876 | stderr | yes |
| attestation written | 232.189 | stdout | yes |

The process exited 0 after 232.194 seconds. Generated digest: `58ad98b9d6a93338be10dc1c022a3767c47859e2`. The artifact records successful execution of the complete package suite and declared adversarial command:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py
```

The first attempt unexpectedly failed during collection because sandbox access to the existing uv cache was denied, before stage start. It was preserved; scoped cache-access approval enabled the successful attempt. Expectations were classified after execution, not preregistered.

## Public CLI refusal cases

| Isolated input condition | Exit | Specific diagnostic |
|---|---:|---|
| Malformed JSON | 2 | cannot read review input |
| Dirty functional tree | 1 | BLOCK finalize.clean-tree |
| Missing authorization arguments | 2 | --intent or --confirm-authorized is required |
| Working intent authorization removed | 2 | automatic-publication authorization revoked |

No override was supplied. Both clone origins were local paths; no remote publication or plugin installation was attempted.

## Independent evidence audit and limits

A separate agent cross-checked five source hashes, launcher resolution, original input, raw streams, receipt timestamps, process liveness, command hashes and generated artifact. It recomputed the matching functional digest and freshly confirmed the original source remained clean. Result: PASS WITH NOTES within this local public CLI scope; no long-suite rerun.

This is explicit CLI operation with supplied authentic inputs, not novice command discovery, automatic skill routing, a new acceptance test or a complete agent lifecycle. Live GitHub waiting, installed-host behavior, filter speed and model latency/token savings remain untested. Timestamps measure line receipt, not exact emission. Children remain silent between stage boundaries; successful finalization does not expose captured child logs or exact pass/skip counts. Replay was inspected, not run twice. The raw local packet is retained separately; this summary does not claim a tamper-evident observer.
