# Standalone diagrams and external edits — acceptance evidence

Tested 2026-11-01 from detached clean worktree at `7094b40b171de4f54cbbe81f67f369d918bbad22`. The separate change worktree was not used to execute commands. Disposable fixture root was `/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/standalone-acceptance-dq0mmb7l`; `$FIXTURE` below denotes that root. The probe harness was `/private/tmp/standalone_acceptance_probe_20261101.py`. It made a minimal repository fixture with `docs/loom/intent/example.md`, and compared SHA-256 digests of the original file before and after copies. The harness first used a symlink spelling of the temporary directory returned by `tempfile`, so the product correctly refused it; rerunning with the resolved path passed. No product code was changed.

The repository README's local development instructions require the locked `uv` environment for tests. The local `python3` had no pytest, so focused tests were run with `uv run --isolated --with-requirements requirements-package-tests.lock pytest -q loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py loom-workflow/tests/loom-interactive-diagram/test_skill_guidance.py loom-workflow/tests/loom-interactive-diagram/test_wait_for_save.py`: `43 passed in 2.87s`. This was not the full package suite; `finalize-review` will run that later. The plugin script loaded in the clean copy: `list-backends` returned `demo-json` and `drawio`. README's public marketplace installation uses GitHub main and would not install this unmerged commit; local script loading and focused tests are the setup check for this snapshot.

## 1. Standalone creation

- Command: `diagram.py new solo --output-dir $FIXTURE/project` from a directory outside the fixture repository.
- Result: exit 0; printed `$FIXTURE/project/solo.drawio` and `$FIXTURE/project/solo.projection.md`; both were present.

## 2. Ask before every external edit

- Inspected the shipped guidance at `loom-workflow/skills/loom-interactive-diagram/SKILL.md:53-64`: show resolved source and proposed destination, ask before each external edit, wait for an answer, including after a prior direct-edit choice, and do not act on silence. The focused `test_skill_guidance.py` passed.
- There was no live fresh agent conversation in this run. Therefore this checks the instruction contract, not whether an actual agent will ask before each edit. No copy or edit was started in place of an unanswered user choice.

## 3. Direct original edit or project copy

- Copied `$FIXTURE/outside/original.drawio` using `copy ... --output-dir $FIXTURE/project` and `copy ... --change-id example` from fixture repository root. Both exited 0; SHA-256 of original was identical before and after each copy.
- Controlled edit of the original: inserted an `mxCell` labelled `Acceptance edit` into the fixture XML; `project $FIXTURE/outside/original.drawio --in-place` exited 0 and printed `$FIXTURE/outside/original.projection.md`; `check` exited 0 and printed `projection matches`. No copy was made by `project`.
- This is a controlled file edit, not a live VS Code operation or observation of a user's direct-edit choice in agent chat.

## 4. Managed copy location

- Command: `diagram.py copy $FIXTURE/outside/original.drawio --change-id example` from fixture repository root.
- Result: exit 0; paths printed under `$FIXTURE/repo/docs/loom/example/diagrams/` for both `.drawio` and `.projection.md`; original digest stayed equal.
- A user approval was not fabricated; the command was exercised as if the user had already selected copy.

## 5. Managed creation and external write boundary

- Commands: `new managed --change-id example` from repository root and `new implicit` from `$FIXTURE/repo/docs/loom/example`. Both exited 0 with diagram and projection under `$FIXTURE/repo/docs/loom/example/diagrams/`.
- `project $FIXTURE/outside/original.drawio --change-id example` exited 1 with `outside managed directory .../diagrams`; original digest was unchanged. In-place work required the separate `--in-place` flag.

## 6. Guidance distinguishes contexts

- `loom-workflow/skills/loom-interactive-diagram/SKILL.md:10-20` distinguishes standalone destination selection from Loom change files; lines 35-64 document copy, direct edit, and question-before-edit; lines 69-103 describe the selected path for save monitoring and follow-up checks.
- Focused guidance and command tests: `43 passed`. This verifies the documented contract and command behavior, not conversational compliance by a live agent.

## UI flow 1. Standalone create

- Same command and output as row 1. Both artifacts were in the selected directory.

## UI flow 2. Standalone create without destination

- Command: `diagram.py new absent` outside Loom.
- Result: exit 1; `destination required outside Loom; use --output-dir DIR`; no file was created. Whether an agent asks the user for a directory was not exercised.

## UI flow 3. Managed creation

- Same two commands and outputs as row 5; both managed paths were under the selected change's `diagrams/` folder.

## UI flow 4. External edit prompt

- The skill instruction is at `SKILL.md:53-64`; there was no live agent turn, so the resolved-path display, question, and directory follow-up were not observed.

## UI flow 5. Standalone copy

- Command: `copy $FIXTURE/outside/original.drawio --output-dir $FIXTURE/project`.
- Result: exit 0; printed `$FIXTURE/project/original.drawio` and `$FIXTURE/project/original.projection.md`; original SHA-256 unchanged.

## UI flow 6. Loom copy

- Command: `copy $FIXTURE/outside/original.drawio --change-id example`.
- Result: exit 0; printed two paths under `$FIXTURE/repo/docs/loom/example/diagrams/`; original SHA-256 unchanged.

## UI flow 7. Direct edit selected

- Command after controlled edit: `project $FIXTURE/outside/original.drawio --in-place`.
- Result: exit 0; adjacent projection printed and `check` reported `projection matches`. No separate copy was created. Agent questioning was not observed.

## UI flow 8. No answer

- No live agent turn was exercised; no file operation was used to stand in for silence. The no-action rule is written at `SKILL.md:55-59`, but it cannot prove actual waiting.

## UI flow 9. Source missing or invalid

- Command: `copy $FIXTURE/outside/gone.drawio --output-dir $FIXTURE/project`.
- Result: exit 1; `$FIXTURE/outside/gone.drawio: missing or invalid diagram`. Invalid existing XML and agent follow-up were not separately exercised.

## UI flow 10. Source symlink

- Created `$FIXTURE/outside/alias.drawio` symlink to the valid original. `project .../alias.drawio --in-place` exited 1 with `symlinked diagram; select resolved path`; no projection write occurred. Agent follow-up was not observed.

## UI flow 11. Projection symlink

- Replaced adjacent projection with a dangling symlink. `project $FIXTURE/outside/original.drawio --in-place` exited 1 with `symlinked projection; select a safe destination`. Symlink target remained absent.

## UI flow 12. No adjacent projection

- Removed the projection and ran `project $FIXTURE/outside/original.drawio --in-place`.
- Result: exit 0; adjacent `.projection.md` created; `check` exited 0 with `projection matches`.

## UI flow 13. Unsupported extension

- Created `$FIXTURE/outside/unknown.foo`; `project .../unknown.foo --in-place` exited 1 with `unsupported diagram extension`; no `unknown.projection.md` was written.

## UI flow 14. Destination occupied

- Repeated standalone `copy` to the existing destination. Exit 1 with `$FIXTURE/project/original.drawio: already exists`; original digest stayed equal. The harness did not directly hash the pre-existing destination, but the `open("xb")` command path and focused tests cover nonoverwrite. Agent follow-up was not observed.

## UI flow 15. Copy without project directory

- Command: `copy $FIXTURE/outside/original.drawio` outside Loom.
- Result: exit 1; `destination required outside Loom; use --output-dir DIR`. Agent asking for a directory was not observed.

## UI flow 16. Save wait

- Started `wait_for_save.py $FIXTURE/outside/original.drawio --timeout 30` in a live tool session. It returned `READY` and stayed running. After a controlled valid XML edit with the host edit tool, polling the same session returned `CHANGED` and exit 0. Then `project ... --in-place` and `check` both exited 0, with `projection matches`.
- This proves file-change detection and follow-up in a controlled local operation. It does not prove a real VS Code save or that the agent would keep the conversation open while the user edits.

## UI flow 17. Check mismatch

- Added `mismatch` to the adjacent projection, then ran `check $FIXTURE/outside/original.drawio`.
- Result: exit 1; `$FIXTURE/outside/original.projection.md: line 6: 'mismatch' != '<missing>'`. Regenerated with `project ... --in-place`; next check exited 0 and printed `projection matches`.
