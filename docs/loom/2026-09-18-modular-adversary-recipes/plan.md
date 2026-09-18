# Modular adversary recipes — plan
intent: 2026-09-18-modular-adversary-recipes@20afa15d
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/references/adversarial.md:1` holds all three recipes plus the shared protocol; headings at :9 Reuse, :51 Code, :78 Spec, :86 Skill, :98 Recording.
- Reverse: `loom-code/scripts/test_review_convergence_contract.py:9` and `test_build_mechanical_checks.py:288` each read the whole document into one constant, so every recipe's pins share two test files.
- Error: `loom-code/agents/adversary.md:30` names `loom-code/skills/closing-review/references/adversarial.md`, a repo-root-relative path that resolves only while this repository is the working directory.
- Data: `loom-code/references/` already holds plugin-level shared prose: `engineering-baseline.md`, `dispatch-profile.md`, `antigravity-tools.md`.
- Boundary: `loom-code/skills/build/SKILL.md:71` links the file across stations; reviewer, blind-runner and implementer contract paths stay untouched.

## Task DAG

**W0-01 Split the procedure into protocol plus one file per kind**  after: none  acceptance: 1, 2, 8
- Files: loom-code/references/adversary-protocol.md, loom-code/references/adversary-code.md, loom-code/references/adversary-spec.md, loom-code/references/adversary-skill-gate.md, loom-code/skills/closing-review/references/adversarial.md, docs/loom/2026-09-18-modular-adversary-recipes/evidence/rule-correspondence.md
- Test: A1 positive: recipes-at-plugin-references; negative: station-copy-absent. A2 positive: kind-rule-in-own-file; negative: kind-rule-outside-own-file. A8 positive: every-rule-mapped; boundary: no-rule-added.
- Risk: Content moves verbatim; any rewording breaks pinned tests. agent-decided: split on the document's existing H2 boundaries, protocol keeps intro, Reuse and Recording.

**W0-02 Routing table and host-neutral path in the adversary contract**  after: W0-01  acceptance: 4, 7
- Files: loom-code/agents/adversary.md, loom-code/skills/build/SKILL.md
- Test: A4 positive: add-kind-one-file-one-row; negative: existing-recipe-file-untouched. A7 positive: protocol-plus-kind-is-complete; negative: no-station-folder-needed.
- Risk: The path must resolve on three hosts. agent-decided: use the repository's `<loom-code>` form, since only Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}`.

**W1-01 One test file per recipe**  after: W0-01  acceptance: 3, 6
- Files: loom-code/scripts/test_adversary_protocol.py, loom-code/scripts/test_adversary_recipe_code.py, loom-code/scripts/test_adversary_recipe_spec.py, loom-code/scripts/test_adversary_recipe_skill_gate.py, loom-code/scripts/test_review_convergence_contract.py, loom-code/scripts/test_build_mechanical_checks.py
- Test: A3 positive: one-recipe-edit-one-test-red; negative: sibling-recipe-tests-green. A6 positive: failure-names-its-recipe; boundary: protocol-edit-hits-protocol-test.
- Risk: A moved pin must not weaken. agent-decided: each assertion keeps its original pinned text and its affirmative-verb form; the two shared files keep only cross-cutting pins.

**W1-02 Removal leaves nothing dangling**  after: W0-02, W1-01  acceptance: 5
- Files: loom-code/scripts/test_adversary_routing.py
- Test: A5 positive: deleting-a-kind-leaves-no-reference; negative: stale-reference-detected.
- Risk: A grep-shaped check can pass by skipping. agent-decided: the test performs a synthetic deletion in a temporary copy and asserts on the result, never on prose.

**W2-01 Write the four properties into the conventions and the roadmap**  after: W0-02  acceptance: 9
- Files: AGENTS.md, loom-code/ROADMAP.md, loom-code/scripts/test_module_criteria_text.py
- Test: A9 positive: four-properties-stated-once; negative: external-standard-claim-absent.
- Risk: The nesting rule is this repository's own. agent-decided: state it as a repository rule and drop the claim that an external skill convention requires it.

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
1. user-decided — the execution-side draft was parked on `wip/adversary-execution` rather than discarded, so its 136 lines stay recoverable while this change starts from a clean tree.
2. user-decided — only the path this change moves is repaired; the same defect in the reviewer, blind-runner and implementer contracts is left for a separate change.
3. agent-decided — the branch keeps its worktree name rather than a typed name: no checker rule reads branch names, and renaming risks the worktree tooling that created it.
4. Pinned prose lives in two shared test files today; moving pins in the same change that moves the prose can hide a dropped assertion. The correspondence list in W0-01 is the cross-check.
