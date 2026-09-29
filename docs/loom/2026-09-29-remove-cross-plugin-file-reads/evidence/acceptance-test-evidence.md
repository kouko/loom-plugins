# Each plugin uses only its own files — acceptance test evidence

Tried on 2026-09-29, in a clean copy of the project at 6e360dd
(`git worktree add <scratch>/at HEAD`; the isolated-install check used
`git archive HEAD loom-design loom-workflow | tar -x` into an empty
directory with no `loom-code` sibling). Scratch copies were removed afterwards.

## Setup

- How I tried it: followed the root README "Install" section's local form
  (the plugins are plain directories; Antigravity installs from a clone), then
  ran the package suite the station named:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- What came back: exit 0. Largest pytest block `2055 passed, 2 skipped in 81.95s`;
  every other block passed (`260 passed`, `186 passed, 1 skipped`, `201 passed, 5 skipped`,
  ...); every shell block `Summary: N PASS / 0 FAIL`.
- Observation: the root README still says loom-design "Requires `loom-code`,
  whose contract package it reads" (`README.md:118-119`) and that the other two
  plugins "use its contract package and checker" (`README.md:205`). After this
  change neither statement is true at runtime. Setup itself is unaffected.

## 1. loom-design 與 loom-workflow 執行時會用到的 skill、reference、腳本與 hook 中，沒有任何一處需要讀或執行 loom-code 資料夾裡的檔案；在沒有 loom-code 檔案可讀的環境中照著它們的步驟做，不會因為找不到 loom-code 而停下。

- How I tried it:
  - Extracted only `loom-design/` and `loom-workflow/` into an empty directory.
  - `grep -rn loom-code` over both trees (excluding `tests/`), then read every
    hit that is not a `loom-code:<skill>` name hand-off. Remaining hits are
    prose attributions ("loom-code's stations consume this output"), provenance
    comments/docstrings in scripts (`map_validation.py:251`, `map_init.py:14`,
    `start_delivery.py:34`, `privacy-scan.py:9`, `hooks/visualization-card:10`),
    and the verbatim KICKOFF-DEFAULTS template copy whose
    `session-start-baseline` placeholder describes how loom-code measures it
    (`capture-intent/templates/KICKOFF-DEFAULTS.md:14`); capture-intent only
    mints that file to record `second-vendor: suggest`
    (`capture-intent/references/second-vendor.md:19-21`), it never runs the hook.
  - Read capture-intent, write-spec, product-principles, design-system,
    architecture-design, decision-map, distill-sessions SKILL.md: no step says
    to locate, read, or run a loom-code file. `references/locate-loom-code.md`
    is deleted and nothing references it. Templates are read from
    `capture-intent/templates/` and `write-spec/templates/`, which exist in the extract.
  - Ran distill-sessions in the extract on a synthetic 3-session transcript fixture
    (Skill `loom-code:write-plan` + snap-back interrupt):
    `python3 main.py --project-root <fx>/projects --facets-root <fx>/facets`
  - Ran decision-map in the extract in a temp git repo:
    `map_init.py demo-map --repo-root <repo>`, set the map active with DA-1,
    then `start_delivery.py docs/loom/maps/demo-map DA-1 2026-09-29-demo --repo-root <repo>`.
  - Hook configs: `loom-workflow/hooks/hooks.json`, `hooks-codex.json`,
    `loom-workflow/hooks.json` call only this plugin's own scripts.
- What came back:
  - distill-sessions: `rc=0`; 3 payload entries, each input
    `{'session_events': 2, 'target_skill': 'loom-code:write-plan', 'target_skill_md_content': '', 'target_skill_path': ''}`.
  - decision-map: `map-init: scaffolded ...` rc=0; `Start delivery created docs/loom/intent/2026-09-29-demo.md for DA-1` rc=0;
    MAP.md gained `- delivery-intent: DA-1 | docs/loom/intent/2026-09-29-demo.md`.
  - Boundary check on the shipped trees: `OK: loom-design is filesystem-boundary clean.`,
    `OK: loom-workflow is filesystem-boundary clean.`
- Evidence: commands and outputs above; `tests/test_loom_plugin_install_layout.py` passed (see A6 run).

## 2. loom-design 與 loom-workflow 帶的範本複本和 loom-code 的原版內容一致；任一邊改了而另一邊沒改時，測試會失敗。

- How I tried it: scratch script ran `tests/test_contract_template_copies.py`
  clean, then after each one-sided edit, restoring from a backup copy between runs:
  appended a line to loom-design's `capture-intent/templates/intent.md`;
  appended a line to loom-code's `contract/templates/spec-minimal.md`;
  changed the inlined grammar line in `write-spec/references/spec-forms.md` (`REQ` → `RQ`).
- What came back:
  - clean: `5 passed`
  - copy side edited: `FAILED ...test_copy_matches_original[loom-design/skills/capture-intent/templates/intent.md-loom-code/contract/templates/intent.md]` — `1 failed, 4 passed`
  - original side edited: `FAILED ...[loom-design/skills/write-spec/templates/spec-minimal.md-loom-code/contract/templates/spec-minimal.md]` — `1 failed, 4 passed`
  - grammar edited: `FAILED ...test_inlined_requirement_grammar_matches_manifest` — `1 failed, 4 passed`
  - restored: `5 passed`, `git status` clean.
- Note: loom-workflow carries no template copy. decision-map's intent skeleton is
  an inline string in `start_delivery.py:31-64` (pre-existing), not a copy, and no
  test compares its field set with loom-code's `contract/templates/intent.md`.

## 3. 在 loom-design 或 loom-workflow 執行時會用到的檔案中加入一個讀取 loom-code 檔案的寫法（包含腳本與 `<loom-code>` 這類路徑寫法）時，自動的邊界檢查會擋下。

- How I tried it: planted one read at a time, ran
  `python3 scripts/check_plugin_boundaries.py <plugin>`, removed it.
- What came back (rc per plant):
  - `.md` relative link `../../../../loom-code/contract/templates/intent.md` → rc=1 `sibling internal path`
  - `.md` `python3 <loom-code>/scripts/loom_checker.py intent <path>` → rc=1 `sibling placeholder path: <loom-code>` + `sibling checker reference: loom_checker`
  - loom-workflow `.md` `loom-code/skills/write-plan/SKILL.md` → rc=1
  - loom-design `.py` `open("../loom-code/contract/manifest.yaml")` → rc=1
  - loom-workflow `.py` `root / "loom-code" / "contract" / "manifest.yaml"` → rc=1 `sibling path join: loom-code/contract`
  - loom-workflow `.sh` `bash "$ROOT/../loom-code/hooks/session-start"` → rc=1
  - real `loom-workflow/hooks/hooks.json`, `loom-workflow/hooks.json`, `loom-workflow/hooks/hooks-codex.json`, each with `${CLAUDE_PLUGIN_ROOT}/../loom-code/scripts/loom_checker.py` → rc=1 each
  - new `loom-workflow/hooks/hooks-probe.json` → rc=1
  - extensionless python-shebang hook calling `../loom-code/scripts/loom_checker.py` → rc=1
  - clean tree before and after → rc=0 for both plugins.
- Observation: a JSON file not named `hooks*.json` (my first plant was
  `zz-probe-hooks.json`) is not scanned (rc=0). Both manifests point only at
  `hooks.json` / `hooks-codex.json`, so no host loads such a file; not a defect.
- Evidence: `tests/test_check_plugin_boundaries.py`, `tests/test_adversarial_boundary_runtime_forms.py` passed (A6 run).

## 4. 原本 loom-design 寫完 intent 當下做的每一項 intent 格式檢查（結構、product 問題不得含識別字、needs-design 理由與 commit 一致、needs-design 重新計算），在 loom-code 的 write-plan 開始規劃前都會執行；故意寫錯任一項的 intent 會在 write-plan 被擋下。

- How I tried it:
  - Read `loom-code/skills/write-plan/SKILL.md:203-209`: for an intent whose
    `status:` is already `confirmed`, branch first, then run
    `loom_checker.py intent docs/loom/intent/<change-id>.md` until it exits 0,
    before Step 4 (spec decision) and planning.
  - Scratch script built one fresh git repo per case (trunk `main`, change branch
    `engineering/2026-09-29-demo`, confirmed intent committed with
    `docs(loom): intent ... confirmed` and a `needs-design:` body line) and ran
    `python3 <at>/loom-code/scripts/loom_checker.py intent docs/loom/intent/2026-09-29-demo.md`.
- What came back:
  - control (well-formed) → rc=0
  - empty `## Open questions` → rc=1 `BLOCK intent.schema: required section 'Open questions' is missing or empty.`
  - no `## Acceptance` → rc=1 `BLOCK intent.schema: required section 'Acceptance' is missing or empty.`
  - product Problem naming `scripts/export_notes.py` → rc=1 `BLOCK intent.product-no-identifiers` (file path + snake_case identifier)
  - `needs-design: no` without reason → rc=1 `BLOCK intent.needs-design-reason: 'needs-design: no' does not match 'yes | no — <reason>'.`
  - commit body carries a different needs-design line → rc=1 `BLOCK intent.needs-design-reason: the commit message (commit 29f89f6 ...) does not carry the line ...`
  - `needs-design: no` with a branch commit touching `src/cli/export.py` → rc=1 `BLOCK intent.needs-design-recompute` (+ `intent.kind-recompute`)
- Note: capture-intent no longer runs the check itself
  (`loom-design/skills/capture-intent/SKILL.md` Step 4 ends "`loom-code:write-plan` runs the intent check on this file before planning.").

## 5. product 變更遇到 repo 沒有已批准的原則文件時，原則訪談仍在第一次確認 intent 的同一段對話中進行，不會延到後面的站。

- How I tried it: read `loom-design/skills/capture-intent/SKILL.md` Step 3 and
  Step 4 item 4, and confirmed the interview template it names exists in the
  isolated extract (`capture-intent/templates/PRINCIPLES-interview.md`).
- What came back: Step 3 — "For `kind: product` only, read `PRINCIPLES.md` ...
  When it is missing or not ratified, run the interview ... **now, in this same
  conversation** — not as a separate stop"; Step 4 item 4 — "The principles
  confirmation ... restated in the same message, confirmed by the same yes";
  on yes, `ratified-by:` is written. The ratified definition (`ratified-by:`
  line + ≥3 Non-negotiables) matches the checker's. product-principles now reads
  `../capture-intent/templates/PRINCIPLES-interview.md` inside the plugin.
- Not run: a live product-change conversation with a real user. This is a
  prose instruction; verdict rests on reading the station text plus the template
  being present, and `loom-design/tests/spec/test_capture_intent_contract.py`
  passing in the suite.

## 6. 三個 plugin 的版號各自升級，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

- How I tried it: grepped versions in `plugin.json`, `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json`, CHANGELOG top entry, `README*.md` for each plugin,
  compared with branch base 879dd3a9; ran
  `pytest loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized loom-code/tests/test_adversarial_version_metadata_sync.py loom-workflow/tests/scripts/test_release_metadata.py tests/test_check_plugin_boundaries.py tests/test_adversarial_boundary_runtime_forms.py tests/test_loom_plugin_install_layout.py`.
- What came back:
  - loom-code 3.22.4 → 3.23.0, loom-design 2.6.3 → 2.7.0, loom-workflow 5.5.4 → 5.5.5;
    all three manifests per plugin agree; CHANGELOG tops `## [3.23.0] — 2026-09-29`,
    `## [2.7.0] — 2026-09-29`, `## [5.5.5] — 2026-09-29`; README / README.ja / README.zh-TW
    and root README table carry the new numbers.
  - `72 passed in 25.97s`.
- Evidence: the automated test suite, which runs before the change is accepted and
  blocks it on failure, also covers these pins; its full run here exited 0 (Setup).

---

# Re-run after fix round (9eecc6c9..95a970b7), tested at 95a970b

Clean copy: `git worktree add --detach <scratch>/at2 HEAD` (removed afterwards
with `git worktree remove`); isolated extract:
`git archive HEAD loom-design loom-workflow | tar -x -C <scratch>/iso2` (no
`loom-code` sibling). Fix commits: d2e96ced (boundary check, extensionless
non-python hooks), b6823f0c (READMEs), 12b6b029 + 95a970b7 (distill-sessions
name-only target, propose.py name matching), 919eb9ce (write-spec principles stop).

## Setup (re-run)

- Clean worktree created at HEAD; the plugins are plain directories, so the
  README local-install form needs no build. Setup unaffected by the fixes.
- Targeted tests for the re-tested rows, in the clean worktree:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-workflow/tests/distill-sessions tests/test_check_plugin_boundaries.py tests/test_adversarial_boundary_runtime_forms.py tests/test_loom_plugin_install_layout.py loom-design/tests/spec loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized loom-workflow/tests/scripts/test_release_metadata.py`
  → `214 passed in 4.96s`.
- Full package suite not run by the tester (left to finalize-review):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

## README finding (earlier open question) — resolved

- `README.md:118-119` now: "Requires `loom-code` for planning onward; intent and
  spec work alone."; `README.md:186-188` drops "the contract package";
  `README.md:204` now: "the other two hand off to its stations by skill name".
- `loom-code/README.md:111-113`, `README.ja.md:110-114`, `README.zh-TW.md:99-101`:
  "neither sibling reads this package at runtime" (and translations).
- `grep -rln "contract package it reads\|use its contract package\|contract --require"`
  over non-`docs/` Markdown: only loom-code's own write-plan files and CHANGELOG
  history remain — none claims a sibling reads the package.

## 1. (re-tested in full)

- How I tried it: scratch script `a1/run_a1.py` in the isolated extract.
  - Built the three-session transcript tree with the fixture builders of
    `loom-workflow/tests/distill-sessions/test_main_e2e.py` (copied, pointed at
    the extract's scripts).
  - `python3 main.py --project-root <tree>/projects --facets-root <tree>/facets`
    (cwd = extract's `distill-sessions/scripts`).
  - Converted each payload into a `merged.json` entry per SKILL.md Step 3:
    `session_id`, `target_skill` (from payload), `target_skill_path: ""`, one
    Memory Item (same title, anchor `Examples`) per session.
  - `python3 propose.py --input merged.json --target-skill <scratch>/target/brainstorming/SKILL.md --output ... --run-date 2026-09-29`,
    then the same with `--target-skill <scratch>/target/other-skill/SKILL.md`.
  - Re-read distill-sessions SKILL.md Steps 2-3, `references/runtime-protocol.md`,
    `agents/prompt-failure-analysis.md:52-57`; grepped the extract's
    distill-sessions tree for `loom-code` outside `loom-code:` names.
- What came back:
  - `main.py rc= 0`; `top_skills: ['loom-code:brainstorming']`; 3 payloads, each
    input `{'target_skill': 'loom-code:brainstorming', 'target_skill_md_content': '', 'target_skill_path': ''}`.
  - propose.py matching name: `rc=0`; item under `## Proposed additions`,
    `_(supported by 3 session(s): e2e1..., e2e2..., e2e3...)_` — no item dropped.
  - propose.py other skill: `rc=0`; 0 occurrences (correctly filtered).
  - SKILL.md now: "Pass the target skill by name only ... never by a file path ...
    If the host cannot provide the skill by name, the subagent analyzes the
    trajectory without it, and the summary says so; do not drop the trajectory."
    The stop list no longer requires a target SKILL.md.
  - Remaining `loom-code` mentions in the tree: trigger phrases
    (`SKILL.md:24-26`, `test-prompts.json`, `trigger-eval.json`) and provenance
    comments (`friction_signals.py:3`, `propose.py:108`) — none is a read.
  - Boundary check on HEAD: `OK: loom-design is filesystem-boundary clean.`,
    `OK: loom-workflow is filesystem-boundary clean.`
- Note: name matching uses only the part after `:` against the target
  directory name (`propose.py:164-171`), so two plugins' same-named skills in one
  run would share a proposal; no current plugin has such a pair.

## 3. (re-tested for the fixed surface)

- How I tried it: scratch script `a3.py` in the clean worktree; each plant
  written, checked untracked and after `git add -N`, then removed:
  `python3 scripts/check_plugin_boundaries.py <plugin>`.
- What came back:
  - clean before: rc=0 both plugins.
  - `loom-workflow/hooks/session-probe` (`#!/usr/bin/env bash`, `exec python3 "${CLAUDE_PLUGIN_ROOT}/../loom-code/scripts/loom_checker.py"`) → rc=1 `:2: sibling internal path: /../loom-code/scripts/loom_checker.py` (both modes).
  - `loom-workflow/hooks/sh-probe` (`#!/bin/sh`, `cat "$ROOT/../loom-code/contract/manifest.yaml"`) → rc=1 `:2: sibling internal path: ROOT/../loom-code/contract/manifest.yaml`.
  - `loom-design/hooks/zsh-probe` (`#!/usr/bin/env zsh`, `source "${0:A:h}/../../loom-code/hooks/session-start"`) → rc=1 `:2: sibling internal path: /../../loom-code/hooks/session-start`.
  - `loom-workflow/hooks/no-shebang-probe` (no shebang, `cat ../loom-code/contract/manifest.yaml`) → rc=0 `OK` (both modes) — not scanned: `_is_shell_script` requires a `#!` first line (`scripts/check_plugin_boundaries.py:86-98`).
  - clean after: rc=0 both plugins; `git status` clean.
- Other plant forms from the first run are carried over: the fix only adds the
  `_is_shell_script` branch; Markdown, JSON, `.py` and python-shebang paths are
  unchanged in the diff.

## 5. (re-tested in full)

- How I tried it: read `loom-design/skills/write-spec/SKILL.md` Step 1 and
  `loom-design/skills/capture-intent/SKILL.md:155-170`.
- What came back:
  - write-spec Step 1: "For a `kind: product` intent, if `PRINCIPLES.md` lacks a
    `ratified-by: <name> <date>` line or a `## Non-negotiables` section with at
    least three items, **stop** and hand back to `loom-design:capture-intent`;
    never write `ratified-by:` yourself. Otherwise a missing standing document
    never blocks this station".
  - capture-intent: same ratified definition; interview "**now, in this same
    conversation** — not as a separate stop".
  - `loom-design/tests/spec` passed in the targeted run above.
- Not run: a live product-change conversation with a real user.

## Carried over

- 2: fix diff touches no template, template copy, or `tests/test_contract_template_copies.py`.
- 4: fix diff touches neither `loom-code/skills/write-plan/` nor `loom_checker.py`.
- 6: README hunks change prose only, no version strings; version pin tests
  passed in the targeted run above.
