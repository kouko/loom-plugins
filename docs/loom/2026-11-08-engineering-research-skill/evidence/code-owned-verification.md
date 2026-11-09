# Code-owned migration verification

Tested implementation: `927ad01a2413317abf5f5743236f288d6a25d66e` on
`feat/2026-11-08-engineering-research-skill`, in the clean delivery worktree
`/private/tmp/loom-engineering-research-delivery`.

The user explicitly accepted code ownership and required design not to directly
mention the skill. The intent at `7c1b6042` records that scope; design-specific
research remains separate future work, with no placeholder or implementation.

## Actual offline observations

- `sync-trunk` exited 0: the implementation already contains origin/main
  `d5a7f0da247214bdb9c61fe90c550256432e5f76`; no merge was added.
- Complete declared suite exited 0:
  `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
  Its 15 pytest summaries total 4139 passes and 6 skips. The same successful
  runner also executed its shell and Mermaid surfaces; these are not included
  in that pytest total. Raw output: [suite log](code-owned-package-tests.txt).
- The committed reused adversarial program was run after the suite:
  `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_check_mechanisms.py -q`;
  it exited 0 with `71 passed in 2.87s`.
- `python3 scripts/sync_codex_manifests.py --check --all` exited 0.
- A whole-directory diff against the trunk baseline reports no loom-design
  change. The former workflow skill directory is absent; code contains the
  single research package, and its router and three existing callers target it.
- All seven runtime Markdown files have the same bytes as their pre-move
  versions at `4a2fb254`; the human guide's owner backlink changed.
  [Runtime digests](code-owned-runtime-integrity.json) retain the actual checks.
- Source versions are code 3.60.0, workflow 5.20.1 and design 2.22.0. Workflow's
  patch retains a directly related README correction to nine counted tools;
  design's earlier provisional release changes were fully removed.

## Limits and retained authorization boundary

These observations verify the migrated source, registries, portable package and
mechanical suite. They do not establish automatic skill selection, research
quality, actual Vault preservation or installed-host behavior. Earlier native
activation/executor attempts produced no valid model behavior; their failed
receipts remain unchanged. The network-enabled retry was rejected by automatic
approval review because this specific skill/prompt/fixture transmission to
first-party OpenAI lacked explicit consent. The ownership agreement is not that
consent; no retry or replacement actor was executed.

No closing-review attestation or acceptance verdict is asserted here. Publication,
merge, existing plugin installation updates and live Vault writes have not been
performed. Earlier prototype results and the pre-migration suite remain scoped
to their own trees and are not a substitute for the missing behavioral evidence.
