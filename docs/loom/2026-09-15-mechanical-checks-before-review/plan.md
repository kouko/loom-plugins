# Run every mechanical check before closing reviewers read the change — plan
intent: 2026-09-15-mechanical-checks-before-review@ef450389
charter: 1.0

## Current State Evidence
- Forward: loom-code/skills/closing-review/SKILL.md:147-161 dispatches the adversary and creates adversarial programs inside closing review, after Build hands off.
- Reverse: loom-code/agents/reviewer.md:69-71 downgrades evidence a reviewer did not run itself, so 32 of 40 recent reviewers re-ran the package suite.
- Error: loom-code/scripts/loom_checker/command_handlers/finalize.py:104-127 fails on a broken suite or adversarial program only after reviewer verdicts already exist.
- Data: loom-code/contract/manifest.yaml:66-68 names closing-review the owner of action adversarial; step_selection at :246-255 names steps without owners.
- Boundary: loom-code/skills/build/SKILL.md:76-78 bans the complete package suite in Build; build/SKILL.md:18-20 skip list omits adversarial and package-tests.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

Wave 1 — reviewer contract

**W1-01 Reviewers leave suite and adversarial runs to Build and finalization**  after: none  acceptance: 4, 8
- Files: loom-code/agents/reviewer.md, loom-code/skills/closing-review/references/lenses.md, loom-code/scripts/test_reviewer_mechanical_evidence.py, docs/loom/2026-09-15-mechanical-checks-before-review/evidence/cold-read-reviewer.md
- Test: A4 positive: reviewer-text-runs-changed-test-files-and-flags-skips; negative: no-reviewer-or-lens-text-requires-suite-run-or-downgrade. A8 positive: cold-reader-reviews-without-suite-run; boundary: cold-reader-still-downgrades-unopened-citation.
- Risk: fold reviewer.md:140-141 into one rule; keep citation-reading duty; adversary.md "You own" paragraph is byte-pinned and untouched; agent-decided.

Wave 2 — station order

**W2-01 Build ends with adversary, package suite and adversarial programs**  after: W1-01  acceptance: 1, 2, 5
- Files: loom-code/skills/build/SKILL.md, loom-code/agents/implementer.md, loom-code/agents/adversary.md, loom-code/contract/manifest.yaml, loom-code/scripts/test_simplified_station_text.py, loom-code/scripts/test_legacy_contract_removed.py, loom-code/scripts/test_build_mechanical_checks.py
- Test: A1 positive: build-dispatches-fresh-adversary-then-suite-after-tasks; negative: adversary-prompt-carries-no-implementer-explanation. A2 positive: build-allows-complete-suite-at-end; negative: no-speculative-preflight-ban-remains. A5 positive: fix-return-reruns-existing-programs; boundary: skipped-selection-step-omits-that-check.
- Risk: adversary gets intent, plan and changed paths only; fix loops re-run existing programs without re-dispatch; Build skip list gains adversarial and package-tests; agent-decided.

**W2-02 Closing review reviews only mechanically checked content**  after: W2-01  acceptance: 3, 6, 7
- Files: loom-code/skills/closing-review/SKILL.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/scripts/test_review_convergence_contract.py, loom-code/scripts/test_simplified_station_text.py, loom-code/scripts/test_dispatch_profile_contract.py
- Test: A3 positive: reviewers-dispatched-after-build-checks; negative: no-adversary-dispatch-in-closing-review. A6 positive: finalize-failure-fix-needs-next-round; negative: earlier-verdicts-not-reused. A7 positive: checker-tests-pass-unchanged; negative: no-diff-to-finalize-attestation-push-code.
- Risk: edits gate review.bounded-episode wording; section 5 still passes Build's committed programs, so suite runs twice per change by intent constraint; agent-decided.

Wave 3 — mirrored descriptions

**W3-01 Station summary tables name Build's mechanical checks**  after: W2-02  acceptance: 1, 3
- Files: loom-code/skills/write-plan/SKILL.md, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/write-spec/SKILL.md, loom-design/skills/product-principles/SKILL.md, loom-design/skills/design-system/SKILL.md
- Test: A1 positive: all-five-build-rows-name-suite-and-adversary; negative: byte-identical-summary-tests-pass. A3 positive: closing-review-rows-drop-adversary-creation; negative: no-row-says-closing-review-dispatches-adversary.
- Risk: five copies edited identically; byte-identical tests in loom-design guard drift; agent-decided.

**W3-02 READMEs and Codex description follow the new order**  after: W3-01  acceptance: 3
- Files: README.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, loom-code/.codex-plugin/plugin.json
- Test: A3 positive: readmes-say-build-runs-adversary-and-suite; negative: no-readme-says-closing-review-dispatches-adversary.
- Risk: Japanese and Traditional Chinese copies translated from the English edit; longDescription is hand-written, sync script leaves it; agent-decided.

Wave 4 — release

**W4-01 loom-code release notes and version**  after: W3-02  acceptance: 9, 10
- Files: loom-code/CHANGELOG.md, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, README.md
- Test: A9 positive: closing-review-reviewer-transcripts-show-no-suite-command; negative: transcript-scan-detects-seeded-suite-command. A10 positive: package-suite-and-mechanism-check-green; negative: mechanism-check-flags-net-increase.
- Risk: minor bump to 3.5.0 via sync_codex_manifests.py; A9 is proven during this change's closing review from local subagent transcripts; agent-decided.

**W4-02 loom-design patch release**  after: W4-01  acceptance: 10
- Files: loom-design/CHANGELOG.md, loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-design/plugin.json
- Test: A10 positive: loom-design-manifests-in-sync-at-patch-version; negative: manifest-drift-check-fails-on-mismatch.
- Risk: patch bump for station-table text only; agent-decided.

## Questions asked
① — what — Restated the problem (closing review slow because reviewers re-run the full suite) and the 10 Acceptance lines in plain words; asked "is this what you want?" — answered 「對，確認」.
① — consequence — Answering yes authorizes a later non-forced push and Ready PR after Review and publication checks pass; merge stays a separate decision; the user may opt out before publication — answered 「同意自動發布」.

## Risks
1. Main merged expert-mode (aa0cffff) the same day over the same files; the branch was rebased before planning, and any further main change needs another rebase before closing review.
2. The suite runs twice per change, at Build end and in finalize-review; removing the second run needs checker changes the intent excludes.
3. Branch renamed from speedup-reviewer-subagent to feat/2026-09-15-mechanical-checks-before-review so the PR title type matches; herdr workspace metadata may still show the old name.
4. The missing attack-catalogue reference stays broken for adversary skill and gate attacks; it is out of scope and should become its own intent.
5. Ordinary dispatches load the installed reviewer contract, so closing reviewers run from a --plugin-dir headless session on the branch plugin (probe evidence plugin-dir-reviewer-probe.md); the edited contract then reviews its own change; agent-decided.
