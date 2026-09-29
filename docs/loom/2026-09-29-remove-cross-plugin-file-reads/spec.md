# Each plugin uses only its own files — spec
intent: 2026-09-29-remove-cross-plugin-file-reads@879dd3a9
pre-build-review: not-required — plugin-internal skill prose, template copies, one test and one repo check; no security, data, public API or cross-system risk, and every step is reversible by revert

## Requirements
REQ-1 — No runtime read of loom-code files
  WHEN any loom-design or loom-workflow skill, reference, script or hook runs, it shall neither read nor execute a file inside the loom-code plugin; the loom-design checker calls are deleted and loom-code's write-plan runs the checks instead (carried: 「刪掉這些呼叫，改由 loom-code 自己的 write-plan 檢查」), decision-map drops its version check (carried: 「刪掉版本確認」), and distill-sessions stops resolving loom-code skill files → Acceptance #1
REQ-2 — Template copies stay identical
  The loom-design copies of loom-code's contract templates and the inlined requirement-ID grammar shall match their loom-code originals, and a repository test shall fail when either side changes alone (carried: 「複製一份到 loom-design，加一支測試確認兩份一致」; 「把格式直接寫進來，由同一支一致性測試守著」) → Acceptance #2
REQ-3 — Boundary check blocks new cross-plugin reads
  WHEN a runtime file under loom-design or loom-workflow gains a reference that reads or runs a loom-code file, including in a Python script or through a `<loom-code>` path form, the repository boundary check shall fail (carried: 「擴大邊界檢查，也掃 .py、contract/ 和 <loom-code> 這類寫法」) → Acceptance #3
REQ-4 — write-plan runs the intent checks
  WHEN loom-code's write-plan receives an intent already confirmed elsewhere, it shall run the intent check (schema, product-no-identifiers, needs-design reason with its commit-body match, needs-design recompute) before planning and stop on any failure → Acceptance #4
REQ-5 — Principles interview timing unchanged
  WHEN a product intent is captured in a repo whose PRINCIPLES.md is missing or unratified, capture-intent shall still run the principles interview inside the same decision point ① conversation → Acceptance #5
REQ-6 — Release bump
  The three plugins shall each carry a new version, consistent across manifests, CHANGELOGs, READMEs and pin tests → Acceptance #6

## Design decision
- agent-decided: write-plan gets an explicit `loom_checker.py intent` step on the already-confirmed path, not the rules folded into `intake`, because `intake`'s fixtures use uncommitted intents and would all break; the step sits after the branch-first instruction because `intent` exits 2 on the trunk for engineering intents.
- agent-decided: late detection is acceptable. A needs-design mismatch found at write-plan is fixed by one new commit that changes the `needs-design:` line and carries it verbatim (the deciding-commit rule reads the newest such commit), so no agent-side comparison is kept in capture-intent.
- agent-decided: capture-intent's principles check becomes an instruction to read PRINCIPLES.md for a `ratified-by: <name> <date>` line and a `## Non-negotiables` section with at least three items — the same definition the checker uses; no script, because loom-design's validator does not check the ratified-by line.
- agent-decided: template parity is one root test comparing each copy byte for byte with its loom-code original, not a sync script; the carried detail names a test, and a failing test already says which file to copy.
- agent-decided: copies live in `loom-design/skills/capture-intent/templates/` (intent, PRINCIPLES-interview, KICKOFF-DEFAULTS) and `loom-design/skills/write-spec/templates/` (spec-minimal); product-principles reads capture-intent's copy by relative path inside the plugin. `.md` files under `templates/` are excluded from the interface-surface recompute.
- agent-decided: distill-sessions drops its repo-root resolver; the agent that runs it reads the target SKILL.md from the loaded skill's own base directory. In an installed plugin the resolver already returned empty text.
- agent-decided: the byte-identical station summary tables keep their checker column; those rules still govern the intent, and write-plan now runs them.
- agent-decided: `requires-contract` in loom-design's manifest stays as declared metadata; the manifest descriptions drop "Reads loom-code's contract package".
- agent-decided: versions loom-code 3.23.0 and loom-design 2.7.0 (station guidance changes), loom-workflow 5.5.5 (tool changes only).

## Alternatives considered
- Add an OpenCode row to locate-loom-code.md — keeps the dependency; each new host adds a row.
- Loader-time path injection, merging plugins, checker as a `uvx` package, vendored checker — rejected at intent (OpenCode-only, rename cost, network and version drift, duplicated program).
- Fold intent rules into `intake write-plan` — breaks most intake fixtures (uncommitted intents) and the isolated-install test.
- Sync script with `--check` for templates — one more script for what one test already enforces.

## Current state evidence
- Forward: `loom-design/skills/capture-intent/SKILL.md:59-69` Step 0 runs `<loom-code>/scripts/loom_checker.py contract --require 2.1`; same in write-spec, product-principles, architecture-design, design-system.
- Reverse: `loom-code/skills/write-plan/SKILL.md:203-210` skips ① for a confirmed intent, so `intent` never runs there; `intake.py:20-21` imports only the kind recompute.
- Error: `loom-workflow/skills/distill-sessions/scripts/main.py:79` resolves `parents[4]`, which in an installed cache is `.../loom-workflow`, so the SKILL.md read returns "".
- Data: templates read from loom-code — `capture-intent/SKILL.md:125-126,175-190`, `second-vendor.md:19-21`, `write-spec/SKILL.md:111-112`, `product-principles/SKILL.md:40-44`.
- Boundary: `scripts/check_plugin_boundaries.py:40-45,158` scans only tracked `.md` for escaping links and `loom-<x>/(hooks|skills|scripts)/`; all three plugins pass today.

## UI flows
N/A
