# Adversarial — code

The attack recipe for changed code. Read it together with the shared
protocol in [`adversarial.md`](adversarial.md).

## Code

**If the repo declares mutation or fuzz tooling** — a `mutmut`,
`cosmic-ray`, `stryker` or fuzz target in its config — run it over the
changed modules and report survivors: a surviving mutant is a test that
asserts nothing, and a finding against `tests`.

**If it declares none** (the common case), write **at least three**
executable abuse or boundary cases against the changed behaviour, run them,
and record each one. Three is the floor, not the target. Reused and modified
cases count toward the floor. Reuse toward the floor counts only (a) the
programs the adversary committed for this change and (b) tests that exist
unchanged outside this change's branch. Any other test added or changed on the
branch, such as an implementer's pin, is named as related coverage only. Draw
them from:

| Class | The question |
|---|---|
| Empty and absent | zero items, empty string, missing file, unset variable — does it behave, or explode? |
| Boundary | one less, one more, exactly at the limit, the limit plus one |
| Hostile input | wrong type, enormous value, path traversal, injection payload, mixed encodings and non-ASCII |
| Wrong order | the second step called first; the operation run twice; two callers at once |
| Failure of a dependency | the network call fails, the disk is full, the subprocess exits non-zero — is the failure loud, or swallowed? |

Prefer cases that live as real tests afterwards. A case that only ran in
the adversary's head is not evidence.
