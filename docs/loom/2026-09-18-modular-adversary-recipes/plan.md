# Modular adversary recipes — plan
intent: 2026-09-18-modular-adversary-recipes@20afa15d
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/references/adversarial.md:1` holds all three recipes plus the shared protocol; headings at :9 Reuse, :51 Code, :78 Spec, :86 Skill, :98 Recording.
- Reverse: `loom-code/scripts/test_review_convergence_contract.py:9` and `test_build_mechanical_checks.py:288` each read the whole document into one constant, so every recipe's pins share two test files.
- Error: deleting a kind today means cutting passages out of the middle of that document and then hunting its pins across those two test files by hand.
- Data: `loom-code/agents/adversary.md:30` tells the adversary to read that one file first; `loom-code/skills/build/SKILL.md:71` links the same path.
- Boundary: every file stays inside `loom-code/skills/closing-review/references/`; no plugin-level file is created and nothing is shared with another skill.

## Task DAG

**W0-01 Split each kind into its own file beside the protocol**  after: none  acceptance: 1, 2, 8
- Files: loom-code/skills/closing-review/references/adversarial.md, loom-code/skills/closing-review/references/adversarial-code.md, loom-code/skills/closing-review/references/adversarial-spec.md, loom-code/skills/closing-review/references/adversarial-skill-gate.md, loom-code/scripts/test_adversary_layout.py, loom-code/scripts/test_review_convergence_contract.py, loom-code/scripts/test_build_mechanical_checks.py, docs/loom/2026-09-18-modular-adversary-recipes/evidence/rule-correspondence.md
- Test: A1 positive: recipe-files-beside-protocol; negative: recipe-body-left-in-protocol. A2 positive: kind-rule-in-own-file; negative: kind-rule-outside-own-file. A8 positive: every-rule-mapped; boundary: no-rule-added.
- Risk: Existing pins read the old document; leaving them would go red. agent-decided: the same commit repoints each moved pin at its new file, verbatim, no rewording.

**W0-02 Routing table the contract can be followed from**  after: W0-01  acceptance: 4, 7
- Files: loom-code/skills/closing-review/references/adversarial.md, loom-code/agents/adversary.md
- Test: A4 positive: add-kind-one-file-one-row; negative: existing-recipe-file-untouched. A7 positive: protocol-plus-kind-is-complete; negative: unrouted-kind-detected.
- Risk: The contract path form stays as it is today. agent-decided: only the file names it points at change, since repairing that form is out of scope for this change.

**W1-01 One test file per recipe**  after: W0-01  acceptance: 3, 6
- Files: loom-code/scripts/test_adversary_recipe_code.py, loom-code/scripts/test_adversary_recipe_spec.py, loom-code/scripts/test_adversary_recipe_skill_gate.py, loom-code/scripts/test_adversary_protocol.py, loom-code/scripts/test_review_convergence_contract.py, loom-code/scripts/test_build_mechanical_checks.py
- Test: A3 positive: one-recipe-edit-one-test-red; negative: sibling-recipe-tests-green. A6 positive: failure-names-its-recipe; boundary: protocol-edit-hits-protocol-test.
- Risk: A moved pin must not weaken. agent-decided: each assertion keeps its original pinned text and affirmative-verb form; the two shared files keep only cross-cutting pins.

**W1-02 Removal leaves nothing dangling**  after: W0-02, W1-01  acceptance: 5
- Files: loom-code/scripts/test_adversary_routing.py
- Test: A5 positive: deleting-a-kind-leaves-no-reference; negative: stale-reference-detected.
- Risk: A grep-shaped check can pass by skipping. agent-decided: the test performs a synthetic deletion in a temporary copy and asserts on the result, never on prose.

**W2-01 Write the four properties into the conventions and the roadmap**  after: W0-02  acceptance: 9
- Files: AGENTS.md, loom-code/ROADMAP.md, loom-code/scripts/test_module_criteria_text.py
- Test: A9 positive: four-properties-stated-once; negative: property-without-a-check.
- Risk: Conventions can grow into a second rulebook. agent-decided: four lines naming change, add, remove and locate, plus one roadmap line; no new process and no cross-skill guidance.

**W2-02 Clean-environment suite**  after: W1-02, W2-01  acceptance: 10
- Files: docs/loom/2026-09-18-modular-adversary-recipes/evidence/suite-run.md
- Test: A10 positive: full-suite-green; boundary: clean-clone-green.
- Risk: Host Python drift can mask a failure. agent-decided: run the repository's declared isolated runner, and rehearse the probes in a clone as the scanners change already requires.

## Questions asked
① — what — 要用哪個範圍開 intent：只搬家、按 artifact type 拆檔、還是拆成多個 subagent？
① — what — 模組邊界按 artifact type 切，還是按攻擊手法切？
① — what — 路徑修正只修因搬檔不得不改的那條，還是四份 agent 契約一起修？
① — what — 走法用「示範＋判準」、先寫判準、還是只做示範？
① — consequence — 工作區那三個未提交的檔案要存成暫存分支、複製到暫存目錄、還是直接丟棄？

## Risks
1. user-decided — modularization stays inside the skill: nothing moves to the plugin level and nothing is shared between skills, so the recipes keep their current folder and only split within it.
2. user-decided — the execution-side draft was parked on `wip/adversary-execution` rather than discarded, so its 136 lines stay recoverable while this change starts from a clean tree.
3. agent-decided — the protocol keeps the existing file name, so both readers and their path pins stay valid and the split adds no dangling reference.
4. Pinned prose lives in two shared test files today; moving pins in the same change that moves the prose can hide a dropped assertion. The correspondence list in W0-01 is the cross-check.
5. agent-decided — the branch keeps its worktree name: no checker rule reads branch names, and renaming risks the worktree tooling that created it.
