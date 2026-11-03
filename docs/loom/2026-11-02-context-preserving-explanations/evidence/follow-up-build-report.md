# Follow-up Build — completed local work and blocked host retest

Source candidate: `64cb8751168b4a4a90fb74d14c944408b7c96123`, integrating origin/main `2a4c5a3142edd10f8b68787cd69fa06d1760c96c`.
Date: 2026-11-03. Publication remains held.

## Completed functional work

W1-01 (`260b3f8`) repaired both first-confirmation owners for unsupported additions, unknown factual values, proportionate explanation and concrete publication consequences. It preserved flexible expression, supplied outcome strength, opt-out, informed authorization, non-forced publication and independent merge. RED was observed for both new content obligations, followed by 80 focused passing tests.

W1-02 (`64cb8751`) integrated current main, preserved its fallback/reconfirmation/carried-detail changes and resolved both changelog conflicts without discarding either change. Main already owns code 3.57.0 and design 2.20.0, so this candidate now uses code 3.58.0 and design 2.21.0. Source/derived manifests and README/current-version pins agree. Capture-intent remains at its existing 3500-word cap. No further changes to the publication authorization were inferred from the user's testing approval.

## Local verification

| Check | Result |
|---|---|
| Three focused contract/station modules after integration | 114 passed |
| Complete locked package suite | Exit 0; code group 2706 passed, 2 skipped; remaining declared groups and shell tests passed |
| Existing adversarial program `test_capture_intent_contract.py` | 37 passed |
| `sync_codex_manifests.py --all --check` | Exit 0 |
| Branch diff whitespace check | Clean against origin/main |
| sync-trunk with required Git filesystem permission | Up to date with origin/main 2a4c5a31 |

The earlier source-loaded acceptance and generated attestation predate these functional fixes and main integration. They are historical evidence, not current readiness proof. The new eight-case host retest, renewed affected acceptance evidence and independent closing review are not complete; no new attestation is generated yet.

## Harness work and limits

Claude Code is now 2.1.317. The explicit model remains claude-sonnet-5-5 with medium effort. A native sandbox smoke test ran a local compound write/read command and denied a harmless synthetic marker outside its allowed region with `Operation not permitted` and no permission denial. A checker smoke test initially exposed that auto-allow did not authorize all command classes; explicit Bash tool permission with the OS sandbox retained allowed the checker to run and report contract 2.3.1. That smoke still exposed a Git global-config read blocked by the home-directory deny rule.

The prepared primary-run controller sets GIT_CONFIG_GLOBAL and GIT_CONFIG_SYSTEM to /dev/null and GIT_CONFIG_NOSYSTEM=1 only for test subprocesses, rather than allowing private Git configuration into the sandbox. This final correction has not yet been exercised by a primary run. The controller uses strict sandboxing with no unsandboxed fallback, no shell network domains, restricted file-tool roots, read-only source bundle rules, user-memory exclusion and disabled hooks/auto-memory/MCP. Required runtime-package/cache reads are narrow exceptions. No global settings were changed.

Artifacts are in `/tmp/loom-context-claude-dogfood-retest/`: `cases.json`, `settings-run.json`, `run_case.py`, eight independent fixture repositories, and `candidate-bundle/` copied from the integrated candidate. The original six cases and two counterexamples are prepared. Existing JSONL files there are smoke tests only; zero new primary-case transcripts exist.

The three smoke sessions report estimated costs USD 0.0337832, 0.0205396 and 0.0228882. These are CLI estimates, not invoices. Primary runs are configured with a USD 0.50 estimated stop threshold each (not a hard billing cap); eight are planned, with no silent model fallback or overwritten transcript.

## Automatic approval rejection and required authorization

The primary eight-case command was rejected before process creation:

> The eight Claude Code runs may transmit private candidate plugin source and project prompts to an external model service; authorization covers dogfooding but does not explicitly authorize exporting that sensitive payload to that destination.

No primary case ran, and the rejected action was not retried or executed indirectly. To continue the requested Claude Code test, explicit approval must cover sending the candidate Loom plugin resource copies (loom-code, loom-design, loom-workflow) and the eight sanitized fixture prompts through Claude Code to Anthropic's claude-sonnet-5-5. The packet excludes the original conversation, personal memories/instructions, credentials and unrelated repositories. Local tests cannot substitute for that requested host evidence. Testing authorization does not include GitHub publication.
