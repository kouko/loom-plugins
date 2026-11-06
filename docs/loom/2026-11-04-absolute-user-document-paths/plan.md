# Concise document-delivery guidance — revised plan
intent: 2026-11-04-absolute-user-document-paths@3a7ee21c
charter: 1.1

Scope revision confirmed for implementation on 2026-11-05. Continue the same change with narrower delivery obligations; existing implementation and review evidence describe the earlier scope, not completion of this revision.

## Current State Evidence
- Forward: `loom-code/hooks/session-start@13ecd257` :: "When delivering a local document" begins the 100-word rule; seven other runtime locations contain the same normalized text.
- Reverse: `loom-design/skills/capture-intent/SKILL.md@13ecd257` :: "Read references/conversation-paths.md" is the reference's only runtime consumer; inlining removes that extra read.
- Error: `loom-code/tests/test_conversation_document_paths.py@13ecd257` :: `test_direct_design_document_delivery_carries_path_guidance` special-cases capture's reference instead of checking its inline body.
- Data: `loom-design/skills/capture-intent/references/conversation-paths.md@13ecd257` holds only the delivery paragraph; removing it requires no adopting-project migration.
- Boundary: `loom-workflow/skills/loom-visualization/references/plain-language.md@13ecd257` preserves stored paths and unknown-support fallback; the shortened text must retain both without promising terminal clickability.

## Delivery rule

Deliver local documents with actual absolute paths from the active worktree or external location, including in copyable instructions. For known local Markdown support, use the document's project-relative path as link text (external files: basename) and absolute targets; otherwise show full absolute paths. Enclose targets with spaces in angle brackets. Preserve bundled references, stored relative paths, quoted examples and incidental filenames.

## Task DAG
### Wave 0
**W0-01 Narrow the existing delivery guidance and its regression checks** after: none acceptance: 1, 2, 3, 4
- Files: loom-code/hooks/session-start; loom-design/skills/{capture-intent/references/conversation-paths.md,architecture-design/SKILL.md,design-system/SKILL.md,product-principles/SKILL.md,write-spec/SKILL.md}; loom-workflow/skills/loom-visualization/{SKILL.md,references/plain-language.md}; loom-code/tests/test_conversation_document_paths.py
- Test: A1 positive: delivered-location; boundary: incidental-filename. A2 positive: supported-compact-link; boundary: unknown-support-plain-path. A3 positive: worktree-external-location; negative: wrong-root. A4 positive: portable-reference-preserved; negative: stored-link-rewrite.
- Risk: agent-decided — replace existing paragraphs in place with one concise rule; update the named tests to narrow conversation scope, preserve location/portability coverage, and remove global file-URI and exact-wording pins. No resolver, host detector, new shared layer or procedure gate.

**W0-02 Validate the reduced outcome and synchronize release evidence** after: W0-01 acceptance: 1, 2, 3, 4
- Files: loom-code/{.claude-plugin/plugin.json,CHANGELOG.md}; loom-design/{.claude-plugin/plugin.json,CHANGELOG.md}; loom-workflow/{.claude-plugin/plugin.json,CHANGELOG.md}; derived manifests and existing release pins; docs/loom/2026-11-04-absolute-user-document-paths/
- Test: A1 positive: neutral-document-delivery; boundary: incidental-filename. A2 positive: known-supported-link; boundary: unknown-support-fallback. A3 positive: distinct-worktree-and-external-file; negative: wrong-target. A4 positive: stored-reference-unchanged; negative: unintended-rewrite. Run targeted regressions, the required package suite and independent acceptance review.
- Risk: agent-decided — retain current unmerged release versions, update their descriptions, and refresh evidence after functional edits. Reuse existing fixtures for bounded host acceptance; exclude terminal clicks and broad experiments.

### Wave 1 — approved wording and indirection reduction
**W1-01 Shorten the rule and inline its single-use capture entry** after: W0-02 acceptance: 1, 2, 3, 4
- Files: loom-code/hooks/session-start; loom-design/skills/; loom-workflow/skills/loom-visualization/{SKILL.md,references/plain-language.md}; loom-code/tests/test_conversation_document_paths.py; loom-code/CHANGELOG.md; loom-design/CHANGELOG.md; loom-workflow/CHANGELOG.md
- Test: A1 positive: inline-entry-delivery; boundary: incidental-filename. A2 positive: explicit-path-link-text; boundary: unknown-support-plain-path. A3 positive: worktree-external-location; negative: fixed-root. A4 positive: portable-reference-preserved; negative: stored-path-rewrite.
- Risk: agent-decided — preserve all obligations while reducing each copy from 100 to 60 words. Inline capture guidance and delete its reference; tighten capture wording to retain its existing 3500-word body cap. Keep unmerged versions and existing coverage.

## Simplicity check
- Inline the single-use reference and shorten the existing policy without a new loader — taken

## Questions asked
① — what — 以上就是你要的範圍嗎？ 若不希望自動建立 PR，也可一併說明。

## Risks
1. user-decided — 2026-11-05: implement one concise document-delivery rule. Retain authorized PR publication after renewed verification; merge requires explicit acceptance and installed-plugin updates remain outside this change.
2. agent-decided — realpath is an optional implementation tool. Judge correct delivered locations, not tool-call presence or byte-for-byte reuse.
3. agent-decided — use known host support; unknown support falls back to full absolute text. Do not infer Markdown support from terminal branding or run environment detection.
4. agent-decided — normal filename mentions and quoted examples are outside delivery scope; actual copyable delivery instructions must still identify the intended document.
5. agent-decided — retain existing standalone plugin entry points to avoid a new cross-plugin dependency. Inline duplication is bounded; do not create a new policy service or new guide files.
6. agent-decided — prior dogfood provides counterexamples and reusable fixtures, not universal reliability or causal improvement estimates. Terminal wrap/click behavior remains unverified and out of scope.
7. agent-decided — revised intent is committed and pinned. Run plan/intake checks before Build and replace previous acceptance and review evidence for the revised functional tree; do not carry earlier passing verdicts into this review.
8. user-decided — 2026-11-06: adopt the 60-word rule and inline capture guidance, preserving all four Acceptance lines. This is the same review episode's second functional digest; prior host outputs remain historical evidence, not current execution proof.
9. agent-decided — do not start the pending twelve authenticated external-model sessions or bypass their approval rejection. Use local mechanical checks and native independent verification; disclose that the shortened text has no newly verified external-host behavior.
10. agent-decided — the inline candidate exposed capture's existing 3500-word body cap: 3554 words failed its unchanged test. Remove at least 54 words of redundant capture prose without deleting obligations, changing gates, or raising the cap.
