# Loom flow recovery loop — plan
intent: 2026-09-19-loom-flow-recovery-loop@e4a57bc8
spec: docs/loom/2026-09-19-loom-flow-recovery-loop/spec.md@ce91283
charter: 1.0

## Task DAG

**W0-01 Build re-enters its end-of-Build checks when an item is absent**  after: —  acceptance: 1
- Files: loom-code/skills/build/SKILL.md
- Test: A1 positive: RL-01; negative: RL-02.
- Risk: Widening the antecedent could make Build re-dispatch the adversary on every entry. Bound it to absence, per spec REQ-1 and the Design decision on adding an antecedent. agent-decided.

**W0-02 Closing review tells absence from failure and names the producer**  after: W0-01  acceptance: 3, 4, 5
- Files: loom-code/skills/closing-review/SKILL.md
- Test: A3 positive: RL-03; negative: RL-04. A4 positive: RL-05; boundary: RL-06. A5 positive: RL-07; negative: RL-08.
- Risk: Prose could restate the artifact-to-station mapping instead of citing it. Spec REQ-3 forbids a second copy; RL-04 fails the build if one appears. agent-decided.

**W0-03 Probes pin the recovery rules and the no-repeat bound**  after: W0-02  acceptance: 2
- Files: loom-code/skills/build/probes/test_recovery_rules.py, loom-code/skills/closing-review/probes/test_recovery_rules.py
- Test: A2 positive: RL-09; boundary: RL-10.
- Risk: A prose-presence probe passes on wording that no agent follows. The blind run, not these probes, decides Acceptance 1, 2 and 5 behaviourally. agent-decided.

## Questions asked
1 — what — 這次要修的「卡死」範圍到哪裡？
1 — what — 如果 agent 回頭補跑、但補跑本身也失敗了，你希望它怎麼做？
1 — what — 證據 指的是啥？ 我覺得是不是把邏輯改成 如果缺了哪個東西就直接回去補 這樣邏輯更簡單？
1 — what — 我想再簡化 理想上應該是整個 loom 邏輯要能夠自動走到底 而且只要使用者說跳過或直接做哪件事 loom 機制就應該配合直接依照使用者的意願執行
1 — consequence — 說 yes 等於授權自動發布（closing-review 與發布前檢查通過後直接 push 並開 Ready PR），合併仍另外問你；你隨時可在發布前改口

## Risks
1. The change is prose an agent must follow, not code a test can force. Probes pin the wording; only the blind run shows an agent actually recovering. Acceptance 1, 2 and 5 rest on it.
2. Build and closing-review prose are mirrored on the same rule, so W0-01 and W0-02 stay sequential; disjoint files do not make them independent.
3. Absence as an antecedent sits next to four existing return edges conditioned on failure. Wording that blurs the two could make a passing check look like a missing item.
4. Bounding a station to two entries is a rule an agent counts, not a runtime guard. A run that ignores it fails the blind run rather than being stopped mechanically.
