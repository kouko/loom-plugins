# Plan: cross-host agent instruction entrypoint

## Scope

Move the existing instruction contract to `AGENTS.md`, keep `CLAUDE.md` as a
one-line import wrapper, and update the contract test to assert the single
source of truth.

## Tasks

1. Verify the moved content is byte-identical and the wrapper is exactly
   `@AGENTS.md`.
2. Run the focused citation-contract test and `git diff --check`.
3. Run Loom closing review and publish the branch through the checker.

## Risks

The only risk is a loader that does not support the import syntax; the wrapper
is intentionally explicit so that support can be tested without duplicating
the contract.

## Questions asked

- none
