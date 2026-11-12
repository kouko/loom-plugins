# Withdrawal of unproved fixture repairs

## Decision and scope

W5-01 withdraws this branch's incidental native-shell rewrites of
`loom-code/tests/test_external_review.py` and
`loom-code/tests/test_external_review_adversarial.py`. Both complete files
are restored to the exact blob bytes at
`391fd01723efedfada3447673b1b99c3894af859`; no production code, assertion,
deadline or coverage changes remain relative to that baseline.

The native fixtures also failed in the original full workload. The bounded
instrumented diagnostic passed (2833 passed, 2 skipped) without reproducing
the blocked-input failure, so it did not locate a cause or establish a
reliability benefit. Earlier repair and mutation receipts remain historical
observations; they do not demonstrate a shipped fix. Preflight timing remains
an unresolved uncertainty. The retained candidate is the requested research
guidance and release work. This withdrawal resets no task or review count.

## Mechanical verification

The restoration read each original file with `git show` and applied the
resulting changes through `apply_patch`. No restore/reset/discard command
was used. A direct Python byte comparison of each restored file with
`git show 391fd01723efedfada3447673b1b99c3894af859:<path>` returned
`exact_bytes=True` for both files. SHA-256 values:

- `test_external_review.py`:
  `82a62069791fd92d002c9b426ef82c1fdafecfeaecb9fea8c51ad11e3909a937`
- `test_external_review_adversarial.py`:
  `da875e872dd67a53312f06fa99bea1e9ef52a77eadfdcfcfc63daa1da6518c25`

`git diff --exit-code 391fd01723efedfada3447673b1b99c3894af859 --
loom-code/tests/test_external_review.py
loom-code/tests/test_external_review_adversarial.py` exited 0 with empty
output. Complete-file equality preserves the original checks exactly;
there are no new tests or harnesses.

## Focused verification and limits

Command: `python3 -m pytest -q loom-code/tests/test_external_review.py
loom-code/tests/test_external_review_adversarial.py
loom-code/tests/test_adversarial_external_review_progress.py`.

Result: 146 passed in 50.77s.

The complete package suite and terminal review remain the orchestrator's
required follow-up. Focused success cannot establish timing reliability
under the original workload or substitute for those checks.
