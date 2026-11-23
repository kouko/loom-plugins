# Plan — 2026-11-20-readme-sync

intent: docs/loom/intent/2026-11-20-readme-sync.md
intent_confirmed_sha: fc8e38819 (post-sync-trunk; the intent-commit sha)

## Current State Evidence

- **Forward** — `loom-code/README.md` sections at `loom-code/README.md:21,67,80,96,114,124,233,252,346`; the `## The checker` section spans `loom-code/README.md:124-231` and carries the five JSON-command material, the read-only `data` table, the one-object envelope, the checked-consumer example and the `suggested_next`/delivery paragraphs.
- **Reverse** — `loom-code/README.ja.md:123-153` and `loom-code/README.zh-TW.md:110-135` carry only the opening `--json` paragraph and the `loom_checker.py` paragraph; the JSON-command list, `data` table, envelope, consumer example and `suggested_next`/delivery material are absent. Every other section heading matches across the three files (`loom-code/README.ja.md:21,67,80,97,113,123,154,171`; `loom-code/README.zh-TW.md:19,59,72,87,101,110,136,151`).
- **Error** — `loom-code/tests/test_adversarial_version_metadata_sync.py:146` fails any loom-code version string in `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md` or root `README.md` that differs from the manifest; `loom-workflow/tests/scripts/test_release_metadata.py:19` pins `5.26.1` across four manifests, CHANGELOG, three READMEs and two root-README lines.
- **Data** — `loom-code/.claude-plugin/plugin.json` version `3.87.1`; `loom-workflow/.claude-plugin/plugin.json` version `5.26.1`; `loom-workflow/README.md:75`, `loom-workflow/README.ja.md:75`, `loom-workflow/README.zh-TW.md` all say 16 skills and each names `loom-herdr` three times (verified post-rebase).
- **Boundary** — `loom-workflow/README.md:70`, `:README.ja.md:70`, `:README.zh-TW.md:64` already define the old map (Acceptance 2, committed at `ec92bed69`); the loom-code ja/zh checker material is the only remaining content gap.

## Wave 1 — loom-code translation gap (Acceptance 1)

- W1-01 — Restore the checker-section material in `loom-code/README.ja.md`
  - Files: `loom-code/README.ja.md` — the `## checker` section (currently `:123-153`), inserting the translated versions of the English paragraphs at `loom-code/README.md:133-208` between the existing opening paragraph and the `loom_checker.py` paragraph.
  - Test: A1 positive: `test_no_readme_states_a_loom_code_version_other_than_the_manifest`; negative: none-new (docs-only; see Risk).
  - Risk: Translation must carry every fact (five JSON commands, the `data` table rows, envelope fields, exit-86/timeout note, `suggested_next` rules); under-translating is the defect this change exists to fix.
  - Reason (agent-decided): keep the existing Japanese paragraph style and bullet length; translate, do not restructure.

- W1-02 — Restore the checker-section material in `loom-code/README.zh-TW.md`
  - Files: `loom-code/README.zh-TW.md` — the `## checker` section (currently `:110-135`), inserting the same translated material.
  - Test: A1 positive: `test_no_readme_states_a_loom_code_version_other_than_the_manifest`; negative: none-new.
  - Risk: Same under-translation risk as W1-01; Traditional Chinese wording must match the file's existing register.
  - Reason (agent-decided): mirror the Japanese structure so the three files stay parallel.

## Wave 2 — release metadata (Constraints)

- W2-01 — Bump loom-code to 3.87.2
  - Files: `loom-code/.claude-plugin/plugin.json`, its three derived manifests via `python3 scripts/sync_codex_manifests.py --all`, `loom-code/CHANGELOG.md` (new `## [3.87.2] — 2026-11-23 — …` top entry), `loom-code/README.md:15`, `loom-code/README.ja.md:15`, `loom-code/README.zh-TW.md:13`, root `README.md` (`loom-code` table row and its section `Version …` line), `loom-code/tests/test_write_plan_station_text.py:9` (`CURRENT_VERSION`).
  - Test: A3 positive: `test_current_release_metadata_is_synchronized`; negative: `test_no_readme_states_a_loom_code_version_other_than_the_manifest`.
  - Risk: Miss one README/root string and `test_no_readme_states_a_loom_code_version_other_than_the_manifest` blocks; run `sync_codex_manifests.py --all` rather than hand-editing derived copies.
  - Depends: `after: W1-01, W1-02`.

- W2-02 — Bump loom-workflow to 5.26.2 for the committed old-map wording
  - Files: `loom-workflow/.claude-plugin/plugin.json`, its three derived manifests via the sync script, `loom-workflow/CHANGELOG.md` (new top entry), `loom-workflow/README.md:11`, `loom-workflow/README.ja.md:11`, `loom-workflow/README.zh-TW.md:11`, root `README.md` (`loom-workflow` table row and its section `Version …` line), `loom-workflow/tests/scripts/test_release_metadata.py:19` (`CURRENT`).
  - Test: A3 positive: `test_root_readme_row_is_current`; negative: `test_plugin_readme_version_is_current`.
  - Risk: This plugin already shipped 5.26.1 on main, so the bump must land above it; update `CURRENT` in the pin test in the same commit.
  - Depends: `after: W2-01`.

## Questions asked

- ① — confirmation — user confirmed the intent (narrowed Acceptance 1-3) on 2026-11-21; intent status `confirmed 2026-11-21`.
- ① — scope — user approved continuing the loom-code README gap plus the version bump on 2026-11-23.

## Risks

- Docs-only change: the package suite is the acceptance check; no new dedicated test beyond the existing pin and version-sync tests.
- The intent's `Acceptance 3` (complete package suite) runs after both bumps, since a version-string drift breaks the pinned tests.
- `skipped-by-instruction: spec, implementer, tdd 2026-11-23` — the user's request is a documentation wording change; the build applies the edits directly.
