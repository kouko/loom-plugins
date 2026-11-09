# Probe A activation findings (advisory)

Native Codex host-adapted raw-skill discovery; not Claude Skill() fidelity, installation parity, or full Loom hooks. Requested model gpt-6.1-sol, first-party OpenAI, medium. Corpus labels/rationales withheld from actors. 20 positive and 5 negative cases, two fresh runs each; repetitions are not independent production reliability samples.

Designer limitation: the orchestrator accidentally displayed the first 30 body lines while extracting frontmatter before corpus creation. Actors remain blind until actual native tool reads; the corpus designer is partially informed.

All work projects are isolated in /private/tmp. Each receives the genuine current scripts/run_package_tests.py as its only source fixture. Only selected raw skill packages and that source slice are available. No vault or private sessions. Temporary auth is symlinked locally, never read as prompt content.

## Execution stopped after one completed preflight

Planned: 50 runs (25 cases × 2). Actually launched/completed: 1, P01-r1; 49 unrun. The native preflight escalation was approved. Before the full batch, the parent reported an automatic approval review rejection for the equivalent Probe B skill/repository-source transfer to OpenAI, and explicitly stopped all external execution. The preflight had already completed; a graceful cancellation check found no remaining harness process. No fallback or alternative service was used. `EXECUTION_STOPPED` now prevents accidental rerun.

### Successful observation (not a general result)

P01-r1 read the target body in the native Codex tool stream: `cat .../home/skills/engineering-research/SKILL.md`, exit 0, [events.jsonl line 6](runs/P01-r1/events.jsonl). The initial [catalog](runs/P01-r1/catalog.json) contained the exact target description and all five adjacent descriptions, and excluded the target body sentinel. This was native discovery, not a forced skill-selection menu. [Receipt](runs/P01-r1/receipt.json) confirms normal exit after 25.416 seconds and removal of the auth symlink. [Answer](runs/P01-r1/answer.txt) bounded its source conclusion and explicitly identified missing CI/execution evidence.

No trigger defect is confirmed. No true-positive or true-negative rate is reported: one preflight cannot estimate either, and negatives were not run. Nothing here supports a dogfood-pass verdict.

### Corpus and reproducibility

[corpus.json](corpus.json) freezes 20 positive + 5 negative queries, labels and rationales before actor execution. Each actor receives only its own query in [prompt.txt](runs/P01-r1/prompt.txt), never labels/rationale. Same-plugin adjacent descriptions are critique, independent-advisor and project-retro; cross-plugin adjacent descriptions are write-plan and capture-intent. Their genuine current source packages are copied verbatim for native discovery. The only repository fixture is scripts/run_package_tests.py; [source-manifest.json](source-manifest.json) records hashes without exposing unrelated repository content. [harness.py](harness.py) records orchestration, three-worker cap, 120-second timeout, event filtering and finally-block auth cleanup.

Generic engineering-decision prompts P10, P11, P15, P16, P18, P19 and P20 remain sensitivity cases: their consequential gaps fit the second description sentence, while the first explicitly names Loom stages. They were labelled positive from that reading before execution; no post-result relabelling was performed. Any future full result should report those separately from explicit-stage cases.

### Limits

This is Codex raw skill discovery, not Claude `Skill()` event fidelity or installed-plugin/full-hook parity. The initial catalog also contains the native host's system skills; its exact content is retained. Requested model/provider/effort are pinned in each isolated config; retained events do not independently disclose a server-confirmed model revision. The corpus designer was partially informed by an accidental initial body excerpt, whereas the actor initial catalog remained body-blind. The fixture is genuine but incomplete, so no end-to-end code or shipping result follows. No hidden reasoning events were retained (zero encountered in this preflight). Local Git provenance records HEAD and existing origin/main without asserting a live remote refresh.

### Catalog isolation audit

The actual initial catalog has 10 skills: the intended six plus four native host system skills (imagegen, openai-docs, skill-creator, skill-installer). There are no additional plugin skills in the catalog. [catalog-audit.json](catalog-audit.json) records exact names, aliased paths, catalog byte count and marker checks. No memory-summary, vault-path or rollout-summary markers were present in that initial catalog; target body sentinel was absent. The 60,083 input-token usage is cumulative across the actor's several model turns and does not imply 60,083 tokens in the initial catalog (70,398 bytes).

Further native execution is paused pending explicit resolution of the payload-to-OpenAI authorization issue. No additional model calls were made after the stop.

## Authorized continuation — 2026-11-08

The user explicitly replied 同意 to the concrete skill/source/prompt/output transfer disclosure for first-party OpenAI gpt-6.1-sol; [authorization-resume.json](../../authorization-resume.json) records consent and exclusions. The original stop marker, harness, summary and receipts are preserved under [history/2026-11-08-pre-resume/](history/2026-11-08-pre-resume/). Continue the same frozen corpus, preserving completed P01-r1 and its costs; run only remaining49.

Context change for resumed actors: target bundle remains actual and complete, but the five adjacent skills contain their genuine frontmatter descriptions plus a neutral no-workflow stub, rather than full bundles. Web search, apps and multi-agent features are explicitly disabled. P01-r1 had full sibling bundles available on demand and default capability configuration; this prevents treating all50 contexts as identical. Initial catalog still must contain target description, exclude target body, and include the five adjacent descriptions. The four native system descriptions remain a known host boundary. No prior result is reset.

## Final completed activation results

All50 planned runs completed normally: 40/40 positive runs read the target body (100% true-positive rate for this corpus), and 10/10 negative runs did not (100% true-negative rate). No trigger-miss, over-trigger, timeout, or harness error was observed. Every case has two fresh runs. Explicit-stage positives:26/26; predeclared boundary-sensitive positives:14/14. The resumed-context subset alone is39/39 positives and10/10 negatives; the preserved preflight adds one positive. No behavioural defect is confirmed by Probe A. These are descriptive corpus results, not a production reliability estimate or dogfood-pass.

[results.md](results.md) provides the per-case table; [per-case.json](per-case.json) retains labels/rationales and raw answer/event hashes; [final-summary.json](final-summary.json) contains overall and sensitivity statistics. All raw prompts, initial catalogs, actual command events, answers and receipts are under runs/. [raw-output-hashes.json](raw-output-hashes.json) records every raw artifact hash; [source-manifest.json](source-manifest.json) records original sources, and each resumed receipt records actual target/stub file hashes.

### Final local verification

All50 initial catalogs contain the same intended six + four system skills and exclude the target body sentinel. All50 auth symlinks were removed; no web tool calls occurred. The actual target bundle hashes match the frozen input for all49 resumed actors. Original source hashes and the full P01-r1 receipt remain unchanged. [final-verification.json](final-verification.json) records these assertions; [all-run-audit.json](all-run-audit.json) exposes actual command trajectories. Event filtering encountered zero reasoning-content events; server usage metadata does report reasoning-token counts, which are retained as cost metadata without reasoning content.

### Scope and costs

Total retained usage, including original preflight:2,349,328 input tokens (1,757,824 cached input tokens),30,690 output tokens,1,159 reasoning output tokens as service-reported metadata; summed actor elapsed time1,214.205 seconds (parallel wall time differs). No monetary price was inferred. Corpus focus is one genuine runner fixture, consequential engineering uncertainty, EN/繁中/JA phrasing and five adjacent jobs. It does not directly test live external version research or broad cross-domain sources; repeated semantic variants and the partially informed corpus designer limit generalization. The native host and stub differences documented above remain material limits.
