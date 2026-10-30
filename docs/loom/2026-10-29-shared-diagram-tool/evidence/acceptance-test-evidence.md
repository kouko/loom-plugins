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
