# Source CLI dogfood outcome

Date: 2026-11-17. Source: loom-code 3.84.0 at
`70325895b651dc99dd1492ed3d899a2980aa7d8b`. This is delivery-validation
evidence only; no production source or permanent tests changed.

The active Codex session built a disposable adopter at
`/private/tmp/loom-probe-dogfood/adopter`, obtained actual independent native
reviews from `/root/dogfood_review_a` and `/root/dogfood_review_b` for both
prerequisite and continuation targets, and invoked real finalizer processes.
No production function, historical validator or reviewer result was mocked.

| Run on the same continuation commit | Exit | Observation |
|---|---|---|
| Installed 3.83.0 with only the current artifact supplied | 1 | False six-program cap refusal reproduced |
| Source 3.84.0 with all six artifacts explicitly supplied | 1 | Six-program cap refusal retained |
| Source 3.84.0 with only the current artifact supplied | 0 | Package and program executed successfully; current attestation generated |

The shared target was `e35115ae29d780a786d9b6677ee06c927df31dba`.
Its prerequisite attestation was genuinely generated and committed before the
current intent, at `3b195f4cda758a2a008b555f01599ad00477b93a`.
All five prior program blobs and the historical evidence SHA-256 were
unchanged after the trials. Both attestations passed the existing validator;
the current one names only `tests/test_current.py` as its adversarial execution.
The entire six-file package was still collected and executed; independent
suite runs and both reviewers observed six passes, none skipped.

Detailed research record, exact launchers, inputs, logs, immutable hashes and
verification script are retained in the external experiment workspace:
[CLI dogfood record](/private/tmp/loom-probe-dogfood/docs/loom/2026-11-17-probe-prerequisite-attribution/research/01-cli-dogfood.md).

This establishes source-CLI protocol behavior, not an installed-plugin or
fresh-host cutover. The fixture uses supported unpinned-intent compatibility
records and synthetic arithmetic programs; it does not claim full station
routing, human confirmation or genuine adversarial-defect discovery.
No finance access, plugin-code edit, global installation, publication or
remote CI execution occurred. The experiment workspace is temporary.
