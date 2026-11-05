# Concise document-delivery guidance — revised plan
intent: 2026-11-04-absolute-user-document-paths@3a7ee21c
charter: 1.1

Scope revision confirmed for implementation on 2026-11-05. Continue the same change with narrower delivery obligations; existing implementation and review evidence describe the earlier scope, not completion of this revision.

## Current State Evidence
- Forward: `loom-code/hooks/session-start` :: "Use absolute paths for every local document location shared in conversation." is broader than document delivery.
- Reverse: `loom-design/skills/capture-intent/references/conversation-paths.md` :: "Never use" imposes a global file-URI prohibition without a universal renderer contract.
- Error: `loom-code/tests/test_conversation_document_paths.py` :: `test_emitted_code_guidance_and_direct_visualization_cover_document_paths` pins the old wording and file-URI prohibition; static checks establish instruction coverage, not host behavior.
- Data: `loom-design/skills/capture-intent/SKILL.md` :: `references/conversation-paths.md` remains a bundled relative resource; portable references are not delivery targets.
- Boundary: `loom-workflow/skills/loom-visualization/references/plain-language.md` :: "where local file links are supported" already separates supported links from plain paths; terminal wrapping remains outside this contract.

## Delivery rule

When delivering a local document, provide its actual absolute location. Where local Markdown links are known to be supported, use the document's project-relative path as the link text (or its filename for an external document) and an absolute target; otherwise show the full absolute path. Preserve portable references inside files.

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

## Simplicity check
- none found

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
