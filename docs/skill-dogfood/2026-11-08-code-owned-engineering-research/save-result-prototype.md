# Persisted-save result tool — bounded prototype

The local mechanism is feasible and native Claude Code can call it: the full-result response matches actual persisted content and its SHA256. Whether this improves real research completion is still untested; eight frozen private executions await their specific transmission approval.

## Question and scope

W4 improved two paired cases but F04 still read only 30 lines, omitting provenance and limitations. This experiment changes only what a save tool returns, not the research instructions or criteria. It is a test-local prototype, not a new Loom capability, gate, required MCP service or installation.

The same save_record name/schema/description, write policy, atomic save, actual disk readback and bounded local-link checks are used in both arms. Confirmation mode returns only written/path; full mode also returns actual complete persisted content, SHA256 and link observations. Baseline actors may still Read. Both arms use the same current seven runtime Markdown files.

## Completed local and public controls

| Check | Observation | Limit |
|---|---|---|
| Helper/protocol tests | 23 passed, including actual Unicode disk readback, stale/collision/no-write checks, traversal/symlink defenses, size/readback failures and malformed-link state | Not an agent-quality judgment |
| Invocation/preparation tests | Six passed; total 29 offline tests | Do not call models |
| Native confirmation control | Actual sole save tool connects, creates approved public record, rejects outside traversal write | Returns no substantive body |
| Native full-result control | Same saved record hash; complete returned body equals disk, including final limitations marker; actual local evidence link exists | Content availability, not understanding |
| Native tool/context surface | Exactly Glob/Grep/Read/scoped save_record; no custom plugins or slash commands; three public instruction canary responses absent | Session-only configuration/control evidence, not a universal hidden-context or process filesystem proof |

[Actual public calls and returned values](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/public-control/observations.json) and [verification](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/public-control/verification.json) retain both successful writes and denials. Both records share SHA256 `4105265e4f26f9e49788cf1db959f2ca8ee4d471debcb644aed3232a2896ad10`; source settings and helper dependencies remained unchanged. The two public native runs exited 0, without timeout, at 8.144 and 11.745 seconds, requesting first-party Anthropic claude-sonnet-5-5/medium; returned model labels match. These synthetic controls contain no private skill/source fixture.

The tool permits only trusted instance-authorized Markdown paths. F01 may update the original record, F04 may create a new standalone record, F06 may create only the exact approved fixture Vault note, and F03 permits no write. No source/config/instruction-file writes or tool installation are permitted. Both native read-tool confinement and helper write policy are needed; neither extends the other's scope.

## Prepared behavioral comparison

| Case | Purpose | Actors |
|---|---|---|
| F04 | New record and receipt/CI claim boundaries; reproduced residual partial readback | One confirmation/full pair |
| F01 | Update the existing same-question record | One pair |
| F06 | Exact approved copy, source preservation and provenance | One pair |
| F03 | Explicit no-write and truthful unsaved draft | One pair |

[Prospective protocol](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/prospective-protocol.md), [frozen input metadata](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/private-inputs/freeze.json), and [pair equivalence](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/private-inputs/prepare-verification.json) precede model execution. Prompts and all project files are byte-identical per pair; permissions are identical; only tool-result fields vary. The private freeze SHA is `e1ebae3a122cfebd54a13f24c0c73c372048fc20398691e49f7c9f320a4446e7`.

No private execution or independent audit of this tool intervention has run. Requested approval bounds the next phase to eight first-party Anthropic executions and two first-party OpenAI audits of their outputs/observable trajectories. Prior twelve-output permission is not treated as approval of this new data. No absent answer or preselected UI option is approval.

## Integration findings retained

The first complete package run failed two existing checks: a previous local masking function's name matched the retired-step spelling guard, and the census classified the new save helper as other. Earlier package passes preceded tracking those local files and therefore did not prove the later tracked inventory. [Original failure log](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/package-tests-first-failure.txt).

The three live identifier instances were renamed consistently without changing behavior or frozen traces; the guard and nine earlier harness tests passed (10 total). The census owner separately admitted only the exact helper path as not-prose: it has no test functions, assertions or contract-prose pins. No generic inference or rule changed. [Owner report and actual-program mutations](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/census-owner-report.json) retain restoration-to-failure, unknown-neighbor rejection, over-broad-mutation failure and prose-pin-neighbor classification. Existing census adversarial tests passed three cases unchanged. After the fixes and local files were committed, trunk synchronization was up to date and the complete package runner exited 0: 4,139 pytest passes, six skips across 15 groups, plus shell and Mermaid checks. [Full tracked-tree log](../../loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/package-tests-final.txt). This repairs integration, not the untested private behavioral comparison.

## Limits and disposition

The helper rejects note bodies over 32KiB before writing. Returned JSON also includes metadata; this is not a total response/token cap or a guarantee against caller truncation. Inspect actual received tool output. Inline local Markdown destinations are checked within the authorized root; external content, anchors, images/reference syntax and complex Markdown are not validated. Missing/outside/symlink/malformed destinations remain explicit unchecked/missing results. File existence does not prove claim support, and complete bytes do not prove the agent inspected or understood them. Readback is point-in-time and is not a hardened concurrent-process sandbox.

Official [CLI reference](https://code.claude.com/docs/en/cli-reference) explains restricted versus safe mode and explicit MCP/settings; [instruction-loading documentation](https://code.claude.com/docs/en/memory) supports the session exclusions used here. Actual public controls, not documentation alone, establish callable native integration. Settings were not installed or changed globally.

Keep the prototype test-local pending behavioral evidence. Do not claim overall dogfood pass, automatic triggering improvement, cross-host installation compatibility, semantic research correctness or production readiness from these controls. No real Vault, private session history, CI/release/deployment or publication is involved.
