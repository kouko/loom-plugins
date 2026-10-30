# Shared editable diagram — acceptance test evidence

Tried on 2026-10-30 in a fresh `git archive 3433fd9e` extraction at `/private/tmp/loom-diagram-accept-rSQ7m4`. This was a source archive, not a fresh OS installation. The repository working tree's untracked `diagrams/` was not used or modified. VS Code Draw.io Integration 1.17.0 and official draw.io Desktop 32.6.1 were reported available, but no UI result from them was obtained in this run.

## 1. VS Code live update
- How I tried it: Created `diagrams/acceptance.drawio` with the documented `diagram.py new acceptance` command in the clean archive. Attempted to inspect VS Code through `cua_repl`; the app binding stalled and was aborted.
- What came back: CLI created the diagram and projection. No usable VS Code UI observation.
- Evidence: creation output in section 5; UI criterion not verified.

## 2. User edit read-back
- How I tried it: No manual editor edit completed; the UI attempt stalled.
- What came back: No saved user edit to read back.
- Evidence: not verified. The scripted XML change in section 3 is not a user edit.

## 3. Projection mismatch
- How I tried it: In the clean archive, inserted a `node-a` vertex with value `Acceptance Node` into the generated XML using a short Python fixture command, then ran `python3 <archive>/loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py check diagrams/acceptance.drawio` from the change directory.
- What came back: exit 1, `diagrams/acceptance.projection.md: line 3: '- none' != '- node-a: Acceptance Node'`.
- Evidence: `diagram.py project diagrams/acceptance.drawio` printed `diagrams/acceptance.projection.md`; `diagram.py check` then exited 0 and printed `acceptance.drawio: projection matches` and `sample.json: projection matches`. Focused suite: `pytest -q loom-workflow/tests/loom-interactive-diagram` → `20 passed in 0.80s`. The automated package suite, which runs before acceptance and blocks on failure, is scheduled for `finalize-review`; it was not run here.

## 4. Malformed diagram rejection
- How I tried it: Created `diagrams/broken.drawio` with incomplete `<mxfile><diagram>` content and a matching backend header, then ran `diagram.py check diagrams/broken.drawio`.
- What came back: exit 1, `diagrams/broken.drawio: invalid XML: no element found: line 1, column 17`.
- Evidence: captured CLI output above; focused suite `20 passed`. Full package suite left to `finalize-review`.

## 5. Clean setup and collaboration loop
- How I tried it: Extracted `git archive 3433fd9e` to a new `/private/tmp` directory; read root README, the tool's `SKILL.md`, and `references/editor-setup.md`. Ran the documented `new acceptance` command from the change directory.
- What came back: `diagrams/acceptance.drawio` and `diagrams/acceptance.projection.md` were printed. `python3 -m pytest` failed because that Python lacks pytest; the available `pytest` executable ran the focused suite successfully. No editor loop completed because the UI call stalled.
- Evidence: fresh archive path and outputs above. Prerequisites were already installed on the machine; installation from scratch was not tried.

## 6. Desktop synchronization
- How I tried it: Read the documented desktop steps; did not complete UI control after the VS Code UI call stalled.
- What came back: No observation for autosave on, autosave off, synchronization prompt, or stale-write modal.
- Evidence: not verified. The editor setup document's prior observations are author-provided context, not evidence from this run.

## 7. Backend registration and selection
- How I tried it: From the clean archive, ran `diagram.py list-backends`, `diagram.py new acceptance`, `diagram.py new demo-json sample`, then `diagram.py check`.
- What came back: list output `demo-json`, `drawio`; creation printed both `.drawio`/`.projection.md` and `.json`/`.projection.md` paths; check exited 0 and reported projection matches for both.
- Evidence: captured commands and output above; focused suite `20 passed` includes registry and unknown-backend cases. Full package suite left to `finalize-review`.

## 8. Shared rules referenced by two stations
- How I tried it: Read `loom-design/skills/write-spec/SKILL.md` and `loom-design/skills/architecture-design/SKILL.md` in the clean archive, and compared their diagram pointers with the shared tool.
- What came back: write-spec line 142 and architecture-design line 20 point to `loom-workflow:loom-interactive-diagram`; neither embeds the format or projection rules. Shared rules are in `loom-workflow/skills/loom-interactive-diagram/SKILL.md` and its references.
- Evidence: file inspection and focused suite `20 passed`.

## 9. VS Code UI flow
- How I tried it: Same attempt as section 1.
- What came back: No editor state was obtained after the UI call stalled.
- Evidence: not verified.

## 10. Desktop UI flow
- How I tried it: No desktop UI action completed.
- What came back: No desktop states were observed.
- Evidence: not verified.

## 11. Station command flow
- How I tried it: Ran list, new, project, check, and malformed-file checks from the clean change directory; compared these to the command flow in the spec.
- What came back: All listed CLI actions produced the expected success or failure outputs. No live station conversation or user handoff was exercised.
- Evidence: sections 3, 4, and 7; partly verified.

## 12. End-to-end path walk
- How I tried it: Setup and command portions were performed; user editor edit and agent read-back were not.
- What came back: No complete round trip.
- Evidence: sections 1, 2, 5, and 11; not verified.

## Re-run on 2026-10-30, at 38ae86a7

The fix range was `3d91e626..38ae86a7`. I inspected the complete diff: it changes the Markdown link parser, draw.io `<object>` label projection, related tests, and wording in the shared tool/editor instructions. It does not change the backend registry, VS Code extension, or draw.io Desktop. I extracted `git archive 38ae86a7` to a new `/private/tmp/loom-diagram-retest-JBIDST` directory. No previous test fixture was reused. UI control had timed out twice, so this re-run made no UI calls. The root agent reported that the full package suite and both graduated adversarial programs passed on this HEAD; those are Build handoff claims, not my independently observed results.

- 1: carried over — external editor synchronization implementation was unchanged; no UI result was obtained in either run. Result stays not verified.
- 2: carried over — manual editor save and file read-back were unchanged; the new wrapper projection behavior is exercised under line 3, but a user hand-edit remains unobserved. Result stays not verified.
- 3: re-tested — `pytest -vv ... -k 'reference_and_balanced_inline_links_are_checked or wrapped_cell_labels_are_projected_for_nodes_and_edges'` ran seven selected cases, all passed. They cover explicit reference, balanced-parenthesis, titled inline, angle-wrapped titled inline, shortcut reference, collapsed reference, and wrapped draw.io node/edge labels. In the fresh change folder I ran `diagram.py new retest`, inserted an `<object label="Visible node" id="n1"><mxCell vertex="1" parent="1"/></object>` and analogous `Visible edge` wrapper, then ran `diagram.py check diagrams/retest.drawio`: exit 1, `diagrams/retest.projection.md: line 3: '- none' != '- n1: Visible node'`. `diagram.py project diagrams/retest.drawio` regenerated the projection, and `diagram.py check` exited 0. The resulting projection contained `- n1: Visible node` and `- e1: n1 -> n1 | Visible edge`.
- 4: re-tested — the six link-form cases each check both mismatched projection and malformed target in the focused tests. Separately, I wrote incomplete `<mxfile><diagram>` to `diagrams/broken.drawio` and ran `diagram.py check diagrams/broken.drawio`: exit 1, `diagrams/broken.drawio: invalid XML: no element found: line 1, column 17`.
- 5: re-tested — from the new archive, the documented commands `diagram.py list-backends`, `diagram.py new retest`, and `diagram.py new demo-json sample` succeeded. `diagram.py check` reported projection matches for both. The editor portion of the collaboration loop remains not verified; no fresh OS or editor installation was attempted.
- 6: carried over — the fix does not alter desktop synchronization; the UI run remains unavailable. Result stays not verified.
- 7: carried over — registry discovery and backend selection code were unchanged. The new archive still listed `demo-json` and `drawio`, and generated one of each; this corroborates but does not replace the first full test.
- 8: re-tested — `rg -n 'loom-interactive-diagram'` showed only the shared-tool pointers in `loom-design/skills/write-spec/SKILL.md:142` and `loom-design/skills/architecture-design/SKILL.md:20`. The modified shared tool remains the rule home; the station text does not restate the format or projection rules.
- 9: carried over — VS Code UI states were not changed by the fix and were not observed in this run. Result stays not verified.
- 10: carried over — desktop UI states were not changed by the fix and were not observed in this run. Result stays not verified.
- 11: re-tested — list, new, project, check, mismatch, and malformed-file error paths ran in the fresh change folder. No live station conversation occurred. Result stays partly.
- 12: carried over — the fix changes projection/link handling, not the user-editor-to-agent handoff; manual user edit/read-back remains unobserved. Result stays not verified.

Focused suite run independently in the fresh archive: `pytest -q loom-workflow/tests/loom-interactive-diagram` → `25 passed in 1.25s`. The full package suite was left to `finalize-review`.

## Re-run on 2026-10-30, at a63bf8f2

I extracted `git archive a63bf8f2` into a new `/private/tmp/loom-diagram-ui-Q6OV2z` directory. The disposable diagram was `/private/tmp/loom-diagram-ui-Q6OV2z/docs/loom/2026-10-29-shared-diagram-tool/diagrams/ui-accept.drawio`; no root-worktree diagram was opened or changed. The already installed VS Code Draw.io Integration appeared in the VS Code extension accessibility tree as version 1.17.0. This was a fresh source copy with installed prerequisites, not a fresh operating-system installation.

- 1: re-tested — from the change directory, `python3 <archive>/loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new ui-accept` printed the `.drawio` and `.projection.md` paths. In VS Code, Quick Open found the absolute path and opened the file in a Draw.io Integration webview (`extensionId=hediet.vscode-drawio`). The open canvas was initially empty. I then wrote an XML vertex with `id="agent-node"` and `value="Agent Added"` to that same file from the shell. Without reopening or refreshing the tab, the next UI accessibility state added `text Agent Added`, and the screenshot showed the labeled rectangle on the canvas. The text buffer was clean before the external write.
- 2: re-tested — I double-clicked the visible rectangle in the VS Code webview. The accessibility tree showed a settable text entry area with selected text `Agent Added`. I pasted `User Changed`, clicked the canvas, and pressed Command-S. The next UI tree showed `text User Changed`. Independently reading the same disk file with `rg -n 'User Changed|Agent Added' diagrams/ui-accept.drawio` returned line 7 with `value="User Changed"`; `Agent Added` no longer appeared. Thus the agent read back the exact manual edit.
- 5: re-tested — the documented clean-source procedure completed through `diagram.py new`, the external update in the open VS Code editor, manual edit and save, `diagram.py project diagrams/ui-accept.drawio`, and `diagram.py check diagrams/ui-accept.drawio`. The last command exited 0 and printed `diagrams/ui-accept.drawio: projection matches`. The extension was already installed; installation from scratch was not observed.
- 6: re-tested but not verified — I called `cua.getApp('com.jgraph.drawio.desktop')` with `timeout_ms: 20000`. The call took 185.7 seconds and then returned an accessibility tree for the previously open `live-check.drawio`, including an Autosave checkbox and `Desktop Auto` text. This was not the fresh `ui-accept.drawio` fixture, so it proves neither autosave-on synchronization nor autosave-off prompt/click behavior on this run. I stopped further UI calls after that stall.
- 9: re-tested — the empty canvas, externally updated node, and editable node were observed in VS Code. A malformed diagram error was tested by CLI in the previous runs, but its editor UI state was not observed; this UI flow remains partly verified.
- 10: carried over — desktop app could not be driven to the new fixture after the stalled app binding. Its UI flow remains not verified.
- 12: re-tested — external agent update, user edit, save, disk read-back, projection, and check all succeeded. No actual station conversation was run, so the full path walk remains partly verified.

## Re-run on 2026-10-31, at ea77d7a3 (UI fixture archived from 9a641891)

The clean fixture was created with `git archive 9a641891 | tar -x -C /private/tmp/loom-diagram-wait-oz40KJ`, before any editor operation. The final verification HEAD is `ea77d7a3`. I compared `a63bf8f2..ea77d7a3`: the runtime addition is the new `wait_for_save.py` and its skill/editor instructions; the later fix rejects non-finite durations and graduates the four adversarial cases into `loom-workflow/tests/loom-interactive-diagram/test_wait_nonfinite_arguments.py`. The diagram generator, backend registry, projection and link checking, and two station references did not change. No source files in the fixture were repaired. The original worktree and its untracked diagrams were not used.

### Acceptance 1 — VS Code external update
- From the archive's `docs/loom/2026-10-29-shared-diagram-tool`, ran `python3 /private/tmp/loom-diagram-wait-oz40KJ/loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py new wait-accept`; output was `diagrams/wait-accept.drawio` and `diagrams/wait-accept.projection.md`.
- Opened that absolute file with VS Code Quick Open. Its Draw.io Integration webview (`extensionId=hediet.vscode-drawio`) showed empty Page-1. An external shell write inserted `<mxCell id="n1" value="Agent Seed" ...>`. Without reopening the tab, the webview accessibility state added `text Agent Seed`. This is a clean-buffer case.

### Acceptance 2 — manual edit read-back, both editors
- In VS Code, double-clicked the visible `Agent Seed` node, replaced selected text with `VSCode Saved Edit`, clicked outside the node and pressed Command-S. The webview displayed `VSCode Saved Edit`; `rg -n 'VSCode Saved Edit|Agent Seed' diagrams/wait-accept.drawio` returned line 7 with `value="VSCode Saved Edit"` and no old label.
- Opened the same archived file in draw.io Desktop via File > Open. Double-clicked that node, replaced its label with `Desktop Saved Edit`, clicked outside, and pressed Command-S. The app said `All changes saved`; disk line 7 then contained `value="Desktop Saved Edit"`, with no prior label. No follow-up user message was sent in either case.

### Acceptance 3 and 4 — carried over
- The prior full re-test at `38ae86a7` independently exercised six spec-link forms, wrapped node/edge projection differences, regeneration and valid check, plus malformed XML rejection naming the file. The final diff adds only the wait path and metadata; neither diagram checking path changed. The latest fixture's sequential `diagram.py project diagrams/wait-accept.drawio` then `diagram.py check diagrams/wait-accept.drawio` printed `diagrams/wait-accept.projection.md` and `diagrams/wait-accept.drawio: projection matches`.
- One initial exploratory `project`/`check` pair was accidentally run in parallel; that `check` raced against projection rewrite and reported a missing header. The immediately repeated sequential check passed. This was a test orchestration race, not an observed product failure.

### Acceptance 5 — clean-source setup
- Followed `references/editor-setup.md` from the fresh archive. The preinstalled VS Code Draw.io Integration and draw.io Desktop opened the newly generated file, showed external updates, saved manual edits, and supplied disk read-back. `project` then `check` passed. This was a fresh source extraction with installed prerequisites, not a fresh OS or editor installation.

### Acceptance 6 — desktop sync modes
- With Desktop Autosave checkbox at `0`, changed disk label from `Desktop Saved Edit` to `Desktop External Sync`. The app displayed `The file has been modified. Click here to synchronize.`; clicking that link changed the canvas text to `Desktop External Sync`.
- Checked Autosave to value `1`, changed disk label to `Desktop Auto Sync`, and observed the canvas text change to `Desktop Auto Sync` without clicking synchronization. Restored Autosave to `0` afterward.

### Acceptance 7 and 8 — carried over
- Prior clean-source check listed `demo-json` and `drawio`, generated one artifact of each, and validated both. The two station skill documents pointed to `loom-workflow:loom-interactive-diagram` without duplicating format rules. The final diff does not touch the registry, selection, or those station documents.

### Acceptance 9 — active-turn saved edit on both surfaces
- VS Code: launched `python3 .../wait_for_save.py diagrams/wait-accept.drawio --timeout 120` in a live shell session after the agent's last write. It printed `READY`. Only then changed the node in the VS Code Draw.io Integration webview and saved it. The same process printed `CHANGED` and exited 0. Disk read-back identified `VSCode Saved Edit`; sequential `diagram.py project` and `diagram.py check` ended with `projection matches`.
- Desktop: launched the same wait command again and observed `READY`. Only then edited the node in draw.io Desktop and saved it. The process printed `CHANGED` and exited 0. Disk read-back identified `Desktop Saved Edit`; sequential project and check again ended with `projection matches`.
- These are actual editor saves during this acceptance tester's active turn. They show the file signal and immediate read-back, but do not establish actor identity from the signal alone.

### Acceptance 10 — unchanged and unrelated changes
- Launched `wait_for_save.py diagrams/wait-accept.drawio --timeout 3 --interval 0.1`, observed `READY`, then ran `touch diagrams/wait-accept.drawio diagrams/unrelated.txt`. This changed metadata for the target but no diagram bytes, and created an unrelated file. The wait printed `TIMEOUT` and exited 1, not `CHANGED`.
- Focused final-tree tests: `pytest -q loom-workflow/tests/loom-interactive-diagram/test_wait_for_save.py loom-workflow/tests/loom-interactive-diagram/test_wait_nonfinite_arguments.py` → `10 passed`. The focused tests cover unchanged content, unrelated file, changed content, missing file, unreadable file, and invalid timeout/interval. The full package suite is reserved for `finalize-review`.

### Spec UI flows
- VS Code surface: empty canvas, external node appearance, manual edit, save, and read-back observed in this fixture. The malformed XML CLI failure was observed in the earlier re-run; the editor's own error display was not inspected.
- Desktop surface: manual edit, Autosave-off synchronization prompt/click, and Autosave-on silent update observed in this fixture. Empty open and stale-write conflict modal were not inspected.
- Command surface: prior full re-test exercised list, new, project, check, mismatch, malformed input and unknown backend. The new wait path did not change these commands. No actual station conversation ran.
- Path walk: file generation, agent write, editor update, user edit, save, disk read-back, projection, and check were observed. A live station discussion continuing after the read-back was not tested.
- Active-turn wait surface: `READY`, `CHANGED` for each editor, `TIMEOUT` for unchanged/unrelated changes, and `ERROR /private/tmp/nonexistent-diagram.drawio: No such file or directory` for a missing path were observed. The host conversation text on timeout or error was not tested.
