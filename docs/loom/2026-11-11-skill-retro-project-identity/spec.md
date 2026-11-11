# Skill-retro project identity — spec
intent: 2026-11-11-skill-retro-project-identity@ad8f5e4a
pre-build-review: required — additive JSON output and event attribution change a consumed contract.

## Requirements
REQ-1 — Known project identity
  The retrospective shall count known repositories distinctly while grouping their subdirectories and linked worktrees under one project → Acceptance #1
REQ-2 — Unknown attribution
  IF project attribution cannot be established THEN the retrospective shall exclude it from known-project counts and disclose incomplete attribution without manufacturing cross-project confidence → Acceptance #2
REQ-3 — Bounded ranking correctness
  The retrospective shall use known project identities for the cross-project score component and retain source provenance, without claiming duplicate-session correctness → Acceptance #3

## Design decision
- agent-decided — REQ-1: retain observed `cwd` on Event; attribute each skill invocation to that event's directory rather than arbitrarily choosing a session's first directory. Claude records supply cwd; Codex session_meta establishes cwd and subsequent turn_context replaces it. Missing/invalid context resets attribution to unknown, avoiding stale inheritance. Keep existing session IDs and invocation detection unchanged.
- agent-decided — REQ-1: resolve absolute existing cwd through `git -C <cwd> rev-parse --path-format=absolute --git-common-dir`, canonicalize the returned directory, and cache resolution per cwd per ingest run. Linked worktrees share this directory; independent clones remain separate. Clear repository-routing GIT environment variables for this inspection, disable optional locks and bound command time. Never run transcript commands, fetch, initialize repositories, or trust Git paths from transcript text.
- agent-decided — REQ-2: missing, relative, malformed, nonexistent, inaccessible, non-Git directories and unavailable/failed/timed-out Git yield unknown. Current filesystem identity is a current observation, not proof of historical path identity; explicitly document that ceiling. No speculative reconstruction of removed worktrees or merging by remote URL.
- agent-decided — REQ-2: retain nullable resolved `project_path` on Event and add sorted `unknown_project_sessions` to aggregate output. A session can have known and unknown invocations; it appears in the unknown list if any matching invocation is unknown. Known project count is a lower bound; incomplete attribution may reduce rank. Existing high/low confidence remains a statement about known distinct projects, never overall evidence quality.
- agent-decided — REQ-3: aggregate the union of resolved project identities on matching invocation events. One session can contribute multiple observed projects, but independent-session thresholds remain separate and unchanged. Retain the optional explicit session_to_project API for existing callers, with missing/empty entries unknown instead of a session-ID fallback. Give fingerprint_count the same missing-mapping semantics because it explicitly accepts project mappings.
- agent-decided — REQ-3: retain weights, frequency, minimum-session and proposal-promotion behavior. Unknown contributes zero known projects; normalization retains the existing zero-denominator guard. CLI top-N regression inputs use distinct sessions to isolate project attribution and include a binding top-N cut. Serialize cwd/project_path alongside existing event source path/line so every counted project is traceable.
- agent-decided — data policy: no transcript or historical report is modified. Source-format grounding used only metadata types from one local Codex session on 2026-11-11: session_meta had string id and absolute string cwd; turn_context had absolute string cwd. No private content is retained in fixtures; fixtures are synthetic.
- agent-decided — keep project identity distinct from session deduplication. The completed Claude proposal review supports this boundary; its technical open questions are resolved here, not added to intent Open questions. Its threshold-config finding remains a separate defect.

## Alternatives considered
- Raw cwd or session ID as identity — inflates projects for worktrees or missing metadata.
- Session-first cwd — loses later project attribution when one session visits multiple repositories.
- Remote URL or folder-name grouping — merges independent local clones without established identity evidence.
- Full session/copy rewrite or adapter expansion — independently shippable behavior outside this change.
- Unknown as a shared project — creates unsupported cross-project evidence when combined with a known project.

## Current state evidence
- Forward: `loom-workflow/skills/skill-retro/scripts/main.py:main` ingests and ranks events.
- Reverse: `loom-workflow/skills/skill-retro/scripts/main.py:aggregate_by_skill` omits project mappings.
- Error: `loom-workflow/skills/skill-retro/scripts/aggregate.py:aggregate_by_skill` substitutes session IDs for missing project identity.
- Data: `loom-workflow/skills/skill-retro/scripts/event.py:Event` has source locators but no cwd/project identity.
- Boundary: `loom-workflow/skills/skill-retro/scripts/cluster.py:cluster_memory_items` keeps distinct-session promotion unchanged.

## UI flows
| Case | Action | Result |
| --- | --- | --- |
| Known data | Run the existing retrospective preview | Exit 0; existing JSON includes canonical project identities and no unknown sessions when all matching invocations resolve. |
| Incomplete data | Run preview with missing or unresolvable project locations | Exit 0; known-project count excludes unknowns and the affected sessions are listed; lower ranking is possible. |
| Empty | Run preview without qualifying invocations | Exit 0; existing empty top_skills/subagent_payload lists remain. |
| In progress | Wait for preview | No new interactive state; repository lookup is cached and time-bounded. |
| Repository lookup failure | Run preview when Git is missing, times out or cannot inspect a location | Continue with unknown attribution, exit 0; restore access or supply transcripts with valid locations to improve coverage, never invent identity. |

## Supporting research
[Project-count investigation](../research/2026-11-11-skill-retro-project-count.md) retains the observed ranking inversion and scope limits.
