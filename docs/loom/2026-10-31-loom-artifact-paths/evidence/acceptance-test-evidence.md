# Per-change diagram artifacts — acceptance test evidence

Tried on 2026-10-31, in a clean Git worktree at `17929854`. The worktree was created with `git worktree add --detach /private/tmp/loom-artifact-paths-acceptance-clean-20261031 HEAD`. Commands ran there unless a change-directory cwd is stated. The diagram script path is `loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py`; abbreviated `diagram.py` command references below omit only that common path prefix. No product files were edited. Test-created diagrams remained only in the disposable worktree.

## Setup

- Repository README `## Install` describes installing the plugins in Claude Code. The diagram skill documents a direct `python3` invocation, which is the usable local entry point without altering the host's plugin installation.
- Command: `python3 loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py list-backends`. Output: `demo-json`, `drawio`; exit 0.
- Baseline: `git status --short` was empty; `test ! -e diagrams` passed.
- Focused suite command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py loom-workflow/tests/loom-interactive-diagram/test_internal_diagrams_symlink.py loom-workflow/tests/loom-interactive-diagram/test_parenthesized_link_invalid_diagram.py loom-workflow/tests/loom-interactive-diagram/test_reference_link_invalid_diagram.py -q`. Output: `32 passed in 1.52s`; exit 0. The default sandbox could not write `~/.cache/uv`; an alternate empty cache could not resolve PyPI DNS. This final command used the existing offline cache with approved access.
- Release metadata command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/scripts/test_release_metadata.py -q`. Output: `14 passed in 0.01s`; exit 0.
- Full package suite was deliberately left to `finalize-review`, which runs before the change is accepted and blocks it on failure.

## 1. 已指定這次變更時，從專案根目錄建立 draw.io 圖，圖檔與文字投影都位於該變更的 `docs/loom` 目錄內，根目錄不新增 `diagrams/`。

- From repository root: `python3 loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new drawio acceptance-root --change-id 2026-10-31-loom-artifact-paths` exited 0 and printed paths ending in `docs/loom/2026-10-31-loom-artifact-paths/diagrams/acceptance-root.drawio` and `acceptance-root.projection.md`.
- `test -f` on both printed files and `test ! -e diagrams` all passed. Projection began `backend: drawio`, `# Nodes`, `- none`, `# Edges`, `- none`.
- The focused diagram tests and release metadata tests above passed.

## 2. 從該次變更目錄建立同一類圖，圖檔與文字投影仍位於相同的預期位置。

- From `docs/loom/2026-10-31-loom-artifact-paths/`: `python3 ../../../loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new drawio acceptance-change` exited 0 and printed the same change's `diagrams/acceptance-change.drawio` and `acceptance-change.projection.md`.
- `test -f` on both files and `test ! -e ../../../diagrams` passed. `project diagrams/acceptance-change.drawio` printed `diagrams/acceptance-change.projection.md`; `check diagrams/acceptance-change.drawio` printed `projection matches`; both exited 0.

## 3. 無法確定這次變更的目錄、或要求更新 `docs/loom` 外的圖檔時，工具清楚拒絕寫入，且不會在 `docs/loom` 外產生或修改檔案。

- From root, `python3 loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new no-change` printed `cannot identify change; use --change-id <id> or run from its docs/loom/<id> directory`, exited 1, and created no root `diagrams/`.
- `python3 diagram.py new unknown --change-id no-such-change` printed `missing intent: .../docs/loom/intent/no-such-change.md`, exited 1, and created no `docs/loom/no-such-change/`.
- From the selected change directory, `new mismatch --change-id 2026-10-29-shared-diagram-tool-description-verify` printed `mismatches enclosing change 2026-10-31-loom-artifact-paths`, exited 1, and created no `mismatch.drawio`.
- Test fixture: copied the new valid draw.io file to root `diagrams/pre-existing.drawio`; initial SHA-256 was `3a77e82858f499c0719b26672dfb5957098a2a9bd47dc2fe6aca3db36a75acea`. `project diagrams/pre-existing.drawio --change-id 2026-10-31-loom-artifact-paths` printed `outside managed directory .../docs/loom/2026-10-31-loom-artifact-paths/diagrams`, exited 1, left that hash unchanged, and made no root projection.
- Created `docs/loom/2026-10-21-diagram-narrow-width-fixes/diagrams` as a symlink to the root fixture directory. `new blocked-link --change-id 2026-10-21-diagram-narrow-width-fixes` printed `managed diagrams directory escapes canonical diagrams location`, exited 1, and made no `diagrams/blocked-link.drawio` in root.
- Created `docs/loom/2026-10-31-loom-artifact-paths/diagrams/linked-old.drawio` as a symlink to the root fixture. `project` on that link printed `outside managed directory`, exited 1, left the fixture hash unchanged, and made no root projection. A second final-file symlink named `blocked-file.drawio` was likewise rejected by `new` before a projection was created.
- Focused diagram tests above included the graduated symlink regression and passed.

## 4. 這項變更不移動或修改使用者原有的圖檔；原有的 Loom 變更紀錄仍可從原位置讀取。

- The clean commit had no root `diagrams/`, so the root `pre-existing.drawio` above is a representative old-file fixture, not a real user's file. Added its matching projection and ran `python3 diagram.py check diagrams/pre-existing.drawio`: output `projection matches`, exit 0. Both files retained their pre-check hashes: diagram `3a77e82858f499c0719b26672dfb5957098a2a9bd47dc2fe6aca3db36a75acea`, projection `4289c4cbd08f3ac36671ed0bbb86a665340f6e6eb54222bbb0a5863b70783f57`.
- Existing record hashes before and after the CLI trials matched: intent `70160a9bae7ac8e6bacefc3cbcd47b92f692f77a848880a6e4f57614e6a24c9a`; spec `abd104dba7e139faa1f4ae5b1f1e7ec43b9b0f84d42e36b98f9e7e055b97f3ac`; plan `ae02132ca828184d72579d6f6d14cbd593a2eba2befed2ad3f7bddad0b1a4d51`. All remained readable at their original paths.

## UI-1. Empty: creation without an identifiable change

- Covered by section 3's root `new no-change`: corrective error, exit 1, no file; retry with the valid id succeeded in section 1.

## UI-2. In progress: local creation and projection

- Sections 1 and 2 show both local commands completed directly with exit 0 and printed output paths; no waiting phase occurred.

## UI-3. Success: root and change-directory creation

- Sections 1 and 2 show both invocations produced files in the same managed directory and printed those paths.

## UI-4. Error: unknown change id

- Covered by section 3's `no-such-change` command: missing intent named, exit 1, no change directory.

## UI-5. Error: conflicting explicit change id

- Covered by section 3's `mismatch` command: both ids named, exit 1, no diagram.

## UI-6. Error: escaping directory or file symlink

- Covered by section 3's directory and final-file symlink trials: each rejected, exit 1, outside fixture hash unchanged.

## UI-7. Error: projection of an external path or escaping link

- Covered by section 3's root fixture and managed symlink `project` commands: each rejected, exit 1, no outside projection.

## UI-8. Success: projection of a managed path

- Covered by section 2's `project diagrams/acceptance-change.drawio`: printed adjacent projection path, exit 0; subsequent `check` matched.

## UI-9. Success: read-only check of an external path

- Covered by section 4's `check diagrams/pre-existing.drawio`: matched, exit 0, before/after hashes identical.

## Re-run on 2026-10-31, at `c5d12cea`

- Fix diff reviewed: `git diff 71ef2452e1a8743ab4c201a195b33b4100a93ef0..c5d12cea6223410f90318ef00d50032d553a19e8 -- loom-workflow/skills/loom-interactive-diagram/SKILL.md`. It changed only guidance: root creation with an explicit id is followed by `cd docs/loom/<id>/`; watcher, `project`, and `check` then use relative paths from that directory. Because the described command route touches each acceptance line or UI flow directly or through its working directory, all rows were re-tested in full rather than carried over.
- Clean copy: `git worktree add --detach /private/tmp/loom-artifact-paths-acceptance-rerun-20261031 HEAD`; `git status --short` empty; `test ! -e diagrams` passed. `python3 loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py list-backends` printed `demo-json` and `drawio`, exit 0. The same README setup route and direct Python entry point were usable.
- Focused suite: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py loom-workflow/tests/loom-interactive-diagram/test_internal_diagrams_symlink.py loom-workflow/tests/loom-interactive-diagram/test_parenthesized_link_invalid_diagram.py loom-workflow/tests/loom-interactive-diagram/test_reference_link_invalid_diagram.py -q` printed `32 passed in 1.38s`, exit 0, using the existing offline uv cache. Full package suite remains for `finalize-review`.
- 1: From root, `python3 loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new drawio rerun-root --change-id 2026-10-31-loom-artifact-paths` exited 0 and printed both files under `docs/loom/2026-10-31-loom-artifact-paths/diagrams/`. From that change directory, `test -f` passed for the diagram and projection; `test ! -e ../../../diagrams` passed. `python3 ../../../loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py project diagrams/rerun-root.drawio` printed the adjacent projection; `check diagrams/rerun-root.drawio` printed `projection matches`, both exit 0. This is the documented root-to-change sequence.
- 2: From `docs/loom/2026-10-31-loom-artifact-paths/`, `python3 ../../../loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new drawio rerun-change` exited 0 and printed both files under the same change's `diagrams/`. Both files existed; root `diagrams/` was still absent at that point.
- 3: From root, `new rerun-no-id` printed `cannot identify change; use --change-id <id> or run from its docs/loom/<id> directory`, exit 1, no root `diagrams/`. `new unknown --change-id no-such-change` printed `missing intent: .../no-such-change.md`, exit 1, no new change directory. From the selected change directory, `new mismatch --change-id 2026-10-29-shared-diagram-tool-description-verify` printed `mismatches enclosing change`, exit 1, no file. A representative root old-file fixture was made only after the no-root checks: `diagrams/pre-existing.drawio` and its matching projection. From the selected change directory, `project ../../../diagrams/pre-existing.drawio` printed `outside managed directory`, exit 1, and fixture hashes remained unchanged. A `diagrams/` symlink in another valid change pointing to root caused `new blocked-link` to print `managed diagrams directory escapes canonical diagrams location`, exit 1, with no root write. A final-file symlink pointing to root caused `new blocked-file` to print `outside managed directory`, exit 1, with no projection. `project diagrams/linked-old.drawio` through a symlink to the root fixture likewise printed `outside managed directory`, exit 1; fixture hashes remained unchanged.
- 4: From the selected change directory, `check ../../../diagrams/pre-existing.drawio` printed `projection matches`, exit 0. The root fixture hashes before and after were diagram `3a77e82858f499c0719b26672dfb5957098a2a9bd47dc2fe6aca3db36a75acea`, projection `4289c4cbd08f3ac36671ed0bbb86a665340f6e6eb54222bbb0a5863b70783f57`. Original intent, spec, and plan stayed readable at their original paths with unchanged hashes `70160a9bae7ac8e6bacefc3cbcd47b92f692f77a848880a6e4f57614e6a24c9a`, `abd104dba7e139faa1f4ae5b1f1e7ec43b9b0f84d42e36b98f9e7e055b97f3ac`, and `ae02132ca828184d72579d6f6d14cbd593a2eba2befed2ad3f7bddad0b1a4d51`. The clean commit contained no real user root diagram; this fixture only models one.
- UI-1: The missing-id error and successful retry with `new rerun-retry --change-id 2026-10-31-loom-artifact-paths` were both observed; the retry printed paths under the managed change.
- UI-2: Local `new` and `project` completed without a waiting phase. Separately, from the change directory, `python3 ../../../loom-workflow/skills/loom-interactive-diagram/scripts/wait_for_save.py diagrams/rerun-root.drawio --timeout 20` yielded `READY` in a live session. After `READY`, a local patch added node `Rerun watcher edit` to the diagram fixture; polling that same session yielded `CHANGED`, exit 0. This simulates a saved file edit and proves the relative watcher path and same-session signal. It does not test a person editing in VS Code or draw.io Desktop.
- UI-3: Root and change-directory `new` commands both printed the same managed directory; the direct file-existence checks passed.
- UI-4: The unknown id named the missing intent, exited 1, and created no change directory.
- UI-5: The explicit id conflict named the mismatch, exited 1, and created no diagram.
- UI-6: Both escaping directory and final-file links were rejected, exited 1, and left the outside fixture unchanged.
- UI-7: External `project` from the change directory and `project` via an escaping symlink were rejected, exited 1, and left the existing outside projection unchanged.
- UI-8: After the simulated saved edit, `project diagrams/rerun-root.drawio` printed `diagrams/rerun-root.projection.md`, exit 0; `check diagrams/rerun-root.drawio` printed `projection matches`, exit 0. `rg -n 'Rerun watcher edit'` found the node in the XML at line 8 and projection at line 3.
- UI-9: External `check` from the change directory printed `projection matches`, exited 0, and the before/after fixture hashes were identical.
