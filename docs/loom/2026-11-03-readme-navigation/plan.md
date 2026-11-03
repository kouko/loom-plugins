# Linked skill documentation — plan
intent: 2026-11-03-readme-navigation@113d9899
charter: 1.1

## Current State Evidence

- Forward: README.md plugin and skill catalogs are the public entry points.
- Reverse: plugin README catalogs lead to skill guides; guides return to their plugin and project.
- Error: prior catalogs linked directories or runtime contracts, and 21 skills lacked human-facing guides.
- Data: 27 SKILL.md directories across three plugins define the live inventory; six already had translated README sets.
- Boundary: runtime skills, hooks and executables remain unchanged; navigation checks and synchronized patch metadata are included.

## Task DAG

**W1-01 Document and connect every skill** after: none acceptance: 1, 2, 3
- Files: README.md, loom-code/README*.md, loom-design/README*.md, loom-workflow/README*.md, loom-code/skills/*/README.md, loom-design/skills/*/README.md, loom-workflow/skills/*/README*.md, tests/test_readme_navigation.py
- Test: A1 positive: inventory coverage; boundary: missing guide. A2 positive: direct README targets; negative: directory-only catalog. A3 positive: valid backlinks; negative: missing destination.
- Risk: Source summaries may drift from runtime contracts; agent-decided: fresh docs review checks every new guide against its SKILL.md and tests validate navigation.

**W1-02 Separate flows from tool catalogs** after: W1-01 acceptance: 4
- Files: README.md, loom-code/README*.md, loom-design/README*.md, loom-workflow/README*.md
- Test: A4 positive: Mermaid parses and route conditions remain explicit; boundary: narrow English, Japanese and Traditional Chinese rendering.
- Risk: Simplification can hide conditions; agent-decided: independent acceptance checks branching semantics and uses the recorded Safari rendering evidence with its stated host limit.

**W2-01 Verify and package the documentation** after: W1-01, W1-02 acceptance: 1, 2, 3, 4
- Files: loom-code/, loom-design/, loom-workflow/, tests/test_readme_navigation.py, tests/test_readme_navigation_adversarial.py, tests/test_loom_plugin_install_layout.py, docs/loom/2026-11-03-readme-navigation/
- Test: A1 positive: complete package suite; boundary: changed inventory. A2 positive: direct targets; negative: broken target. A3 positive: valid backlinks; negative: missing parent. A4 positive: parser; boundary: localized labels.
- Risk: Release drift; agent-decided: patch versions, changelog entries, generated manifests, README versions and existing version assertions are synchronized before final review. Runtime skills, hooks and executables remain unchanged.

## Simplicity check

- Human-facing README guides beside existing runtime contracts — taken
- A separate documentation site and duplicated skill instructions — declined: relative Markdown links satisfy the requested navigation without another build or deployment.

## Questions asked

- none — this records the already-scoped documentation request, not a retrospective claim that an entry interview ran.

## Risks

1. Newly added guides are English; existing translations use a matching guide when available and explicitly disclose the English fallback.
2. No runtime behavior is changed. Full package tests and independent content review guard against misleading documentation and stale metadata.
3. Prior Safari rendering checked local Mermaid 11.17.0, not GitHub's renderer. Independent acceptance must retain that limit rather than claim a GitHub visual test.
4. Cross-plugin relative links fail standalone installation boundaries. Agent-decided: public GitHub README links cross those boundaries; same-plugin links remain relative and map to actual checked-out destinations in navigation tests.
5. Ignored macOS metadata appeared in local install copies. Agent-decided: skill inventories enumerate directories with SKILL.md, matching loader discovery; no user metadata is deleted.
