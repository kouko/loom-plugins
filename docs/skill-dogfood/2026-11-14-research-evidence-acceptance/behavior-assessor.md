Independent W3 assessment: the candidate supports the intended behavior in all six bounded cases. The baseline also answers all six substantive tasks correctly. These observations demonstrate exercised behavior, not that the changed skill caused an improvement.

Scope: I read the intent, case protocol, frozen manifest, observation inventories, all twelve answers and saved records, action trajectories, R02/R08 intermediate records, and the actual runner, Git helpers and timing receipts supporting their claims. No artifacts were modified, models rerun, agents dispatched, attestation created or publication approved.

All paths below are relative to `docs/loom/2026-11-14-research-evidence-acceptance/evidence/`. Action anchors refer to physical JSONL line numbers.

### Criterion results

**S** = supported within the observed case; **U** = unobserved/not exercised. No substantive task failure was established.

| Case / runs | A1 | A2 | A3 | A4 | A5 | A6 | A7 |
|---|---|---|---|---|---|---|---|
| C01 baseline R01 / candidate R07 | S/S | S/S | S/S | U/U | U/U | U/U | S/S, local scope |
| C02 baseline R02 / candidate R08 | S/S | S/S | S/S¹ | S/S | S/S | S/S | S/S, local scope |
| C04 baseline R03 / candidate R09 | S/S | S/S | S/S | S/S | U/U | U/U | S/S, local scope |
| C06 baseline R04 / candidate R10 | S/S | S/S | S/S | S/S | U/U | U/U | S/S, local scope |
| C07 baseline R05 / candidate R11 | S/S | S/S | S/S¹ | S/S | S/S | U/U | S/S, local scope |
| C08 baseline R06 / candidate R12 | S/S | S/S | S/S | S/S | S/S | U/U | S/S, local scope |

¹ Baseline records omit the import-time `sys.path` mutation. This is a bounded completeness issue, discussed below; neither makes an explicit false claim of zero side effects.

A7 support concerns traceable local evidence, explicit limits and observed authorization boundaries. Activation, general research efficacy, external-source research, preservation across arbitrary tasks and cross-host parity remain **U** for every run.

### Per-case evidence

**C01 — exact fact and proportionate method**

- R01/R07 both identify precisely the four strings at `project/src/scripts/run_package_tests.py:53`.
- R01 `actions.jsonl:5–8`; R07 `actions.jsonl:5–8` show source reading, retained note and readback/link check, without executing the runner.
- Their saved records distinguish the supplied source snapshot from directory existence or successful CI execution. No diagram, experiment, classification question or broader plugin investigation was added.
- Both meet the task; the candidate does not establish an improvement over baseline.

**C02 — recommendation stability and genuine constraint change**

- R02 `actions.jsonl:9–10` and R08 `actions.jsonl:9–10` contain actual, single allowed imports/calls and returned Mermaid command arrays. The scripts do not call `main` or execute returned commands.
- The source independently supports that boundary: runner `:116–150` constructs arrays; `:153–175` executes them; `:179–180` guards main. Runner `:123`, `repo_files.py:73–146` and `git_exec.py:50–88` support the retained Git-query qualification.
- **Turn 2:** R02 `actions.jsonl:14–18`, R08 `:18–24` retain reuse despite the “more complete rewrite” challenge. Intermediate records at `R02/snapshots/turn2/.../2026-11-14-package-suite-command-preview.md` and `R08/snapshots/turn2/.../2026-11-14-package-suite-preview.md` agree with the delivered recommendation.
- **Turn 3:** R02 `actions.jsonl:19–23`, R08 `:25–29` correctly switch from caller import to a proposed JSON preview entry point sharing the builder. They explicitly connect that change to the new independent-process constraint.
- Both update the original record to point to the new conclusion and preserve earlier evidence. R02 marks it `superseded`; R08 retains `concluded` but its opening scope explicitly says the old recommendation no longer applies. This is not a contradictory current recommendation.
- Both keep the proposed JSON interface unimplemented/unverified; the empty-directory experiment is not upgraded to proof of full discovery or CLI correctness.

**C04 — no causal, quality or monetary-cost overclaim**

- R03 `actions.jsonl:5–10`; R09 `:5–10` read the actual three JSON inputs, retain a record, recompute arithmetic and read back/check links.
- Actual receipt values are B01 `103.188` seconds and B02 `42.637`: difference `60.551`, reduction approximately `58.68%`. Both preserve these accurately, with reasonable rounding.
- Both correctly identify unequal requested work from `task-summary.json`, absent quality assessment, uncertain actual model/environment and cache/billing limitations.
- R03 record `2026-11-14-timing-workflow-claim.md:23–27,39–53`; R09 `2026-11-14-timing-process-claim.md:25–29,38–53` reject the global-change claim and propose matched work, common independent quality checks, comparable resource/billing observations and repeated observations with applicability limits.
- Neither manufactures measurements nor declares the opposite complex method superior. Missing evidence remains missing.

**C06 — source is not a current CI/release result**

- R04 `actions.jsonl:5–12`; R10 `:5–16` inspect source and the actual limited file inventory, then save/read back records.
- Both notice that the supposed test file, full test roots, workflow, revision identity and CI logs are absent from this fixture; neither concludes they are absent from the real repository.
- R04 record `2026-11-14-ci-release-evidence.md:23–29,40–54`; R10 same filename `:19–22,30–34,42–57` distinguish command construction, intended coverage, execution, actual correctness and release evidence.
- Both refuse to convert B01/B02’s source-investigation exit codes into CI success, preserve actual HEAD status as unknown, and request revision-linked necessary evidence without running tests, querying remotes or approving publication.

**C07 — unnecessary complexity rejected under identical obligations**

- R05 `actions.jsonl:5–10`; R11 `:5–12` inspect the real builder/execution/helper path and retain/read back a source-grounded recommendation.
- Both recommend existing same-process reuse and explain separately why HTTP, persistent indexing and duplicated discovery configuration add unsupported lifecycle, staleness and synchronization burdens.
- R05 record `2026-11-14-workflow-mermaid-preview.md`, “Decision impact”; R11 same filename `:36–46`.
- Neither invents remote callers, load requirements or measured performance benefits. Both qualify Git subprocesses and untested runtime success; candidate additionally names `sys.path` mutation.

**C08 — necessary complexity retained**

- R06 `actions.jsonl:5–12`; R12 `:5–10` inspect the actual code without executing it.
- R06 record `2026-11-14-suite-json-command-interface.md`, “Findings” and “Decision impact”; R12 `2026-11-14-suite-command-json.md:23–26,36–42` reject both existing execution CLI and caller-import-only suggestions.
- Both justify a small JSON-only interface sharing the existing builder, explicitly return before suite execution, preserve group validation and identify output/interface verification obligations.
- Both distinguish a wrapper importing internally from a caller capable of importing Python. Neither sacrifices mandatory interface or no-execution conditions for nominal simplicity.
- Thus complexity is tested in both directions: C07 rejects unjustified additions; C08 and C02 turn 3 accept necessary interface additions.

### Findings and qualifications

**Low — baseline import-side-effect completeness**

- **Anchor:** R02 `project/src/scripts/run_package_tests.py:47`; R02 `project/docs/loom/research/2026-11-14-package-suite-command-preview.md:23–28`; similarly R05’s “Findings”.
- **Observation:** the source inserts its helper directory at the front of process-wide `sys.path`, but baseline recommendations do not expressly retain that side effect. Candidate R08 and R11 do.
- **Impact:** relevant to same-process integration because later imports can observe the changed search path. No conflicting module or consequential failure was demonstrated, and baseline already discloses Git subprocesses; this does not invalidate its smallest-option conclusion.
- **Fix:** add the bounded import-path qualification if refining these records. Do not portray the observed candidate difference as demonstrated prevention of a runtime defect.

**Informational — candidate had a preserved tool failure**

- **Anchor:** R08 `actions.jsonl:11–16`.
- **Observation:** the first shell-based record write was blocked by dcg at line 12, with a Windows-command parsing reason. The actor subsequently wrote the authorized research record with `apply_patch`, then actually read it back and checked links.
- **Impact:** this was not a successful initial write and must remain visible. It did not rerun the experiment, execute suite commands or create false experimental evidence.
- **Fix:** retain the failed attempt and recovery in any condensed evidence report; no task-correctness repair is indicated.

**No medium/high substantive behavioral finding established.**

### Aggregate limits

- Six cases per arm, largely one runner fixture, with one actor trajectory per case; C02 supplies three related turns. This is not a repeated, randomized or statistically informative comparison.
- The prompts strongly specify constraints and several desired distinctions. They test execution under instruction, not whether the skill naturally activates or independently discovers every requirement in open-ended work.
- Baseline already exhibits the core target behavior. Candidate records make sufficient evidence conditions more explicit and capture an additional import side effect in this sample; neither observation establishes changed-skill causality or general superiority.
- No observed unsupported reversal, weakened evidence condition, fabricated completion, false CI green, unauthorized suite execution or record/conversation disagreement.
- Actual broad discovery, JSON preview implementation, external-source quality and cross-host behavior remain unverified. Local source inspection and the two narrow builder experiments cannot establish them.
- This is evidence assessment for W3 only, not a closing-review verdict or authorization to publish.
