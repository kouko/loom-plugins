# Claude Code first-confirmation dogfood — findings

## Metadata and scope

| Field | Observation |
|---|---|
| Date / source | 2026-11-03 / committed source 11a6d731 |
| Host | Claude Code 2.1.316 |
| Requested / observed model | claude-sonnet-5-5 in every preflight and execution modelUsage |
| Effort / authentication | Explicit medium; existing claude.ai login reported firstParty |
| Target | capture-intent and the code-only first-confirmation entry |
| Attempts | Six initial workflow sessions, six repaired-harness sessions, one minimal preflight |
| Review | Two independent blind auditors; neither read the implementation, author rationale or the other audit |
| Assessment | Partial evidence with unresolved content findings; no whole-skill dogfood pass |

The executable selected an explicit model rather than the local chat-agent-group route. No inherited Anthropic endpoint/model override was present in the launch environment or user settings inspected; the local auth command reported firstParty, and the probe returned the selected model. This is configuration and CLI-observation evidence, not independent network attestation. The model ID was checked against [Anthropic's model overview](https://platform.claude.com/docs/en/models/overview).

This is a bounded host exercise of first-confirmation output, not the complete dogfood-skill-testing protocol: explicit skill invocation was used, no statistical should-trigger/should-not-trigger corpus was run, and no separate blind cold-reader probe was performed. Auditors used inherited native profiles whose exact model version was not observable. They are independent contexts, not proof of cross-provider agreement or human comprehension. No before/after control establishes that this patch introduced or reduced any defect.

## Execution evidence

All six repaired-harness sessions invoked the intended skill and reported the requested model. Capture-intent wrote an open draft in all three cases. The code-only date and correction cases remained interviews without a draft; absence alone does not show a defect while required facts remain unanswered. Code-only cases 5 and 6 still encountered a compound-shell-command permission denial, so the complete code-only workflow is not established. Permission limitations are not silently relabeled as content failures.

The first harness put tool sources inside the fixture project and over-constrained compound read commands. Those attempts were retained as diagnostic evidence. The repaired harness placed tools outside each fixture project and supplied only requester-provided project context. It still did not remove every shell restriction. There was no third retry and no source, installed-plugin, push, PR or merge action by the tested sessions.

| Case | Observed artifact / boundary | Blind content assessment |
|---|---|---|
| capture-4-r2 | Open draft; missing-date interview; no tool denial | Partial: D2 and D3 |
| capture-5-r2 | Open draft and confirmation request; no tool denial | Partial: D3 |
| capture-6-r2 | Open draft and correction interview; no tool denial | Partial: D1 and D3 |
| code-4-r2 | Contract check succeeded; missing-date interview; no draft | Partial: D3; confirmation not complete |
| code-5-r2 | Open draft; attempted checks blocked | Partial: D3; workflow also constrained |
| code-6-r2 | Correction interview; no draft; one reference-read command blocked | Partial: D1 and D3; workflow also constrained |

No observed trajectory confirmed, committed or published on the user's behalf. Completed interviews and post-confirmation handoffs were not exercised. Reported costs are CLI estimates rather than invoices: preflight USD 0.0058409, initial sessions USD 0.6569286, repaired-harness sessions USD 0.6038995, total USD 1.266669. Per-session budget flags were estimated stop thresholds, not hard billing caps.

## Severity summary

| Severity | Findings |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 0 |

The medium rating reflects observable problems with a correction/clarification workaround; it does not certify the underlying workflow. The findings below are advisory and identify candidate behavior, not a proven regression caused by this patch.

## D1 — Added a stronger acceptance guarantee

- Classification: Medium × Output-quality; informed execution plus blind audit.
- Probe: cases 6 in both entries ask to repair a prior unexplained “profile” label. The request says each job should use its own worker-selection rule instead of another job's rule.
- Expected: explain that rule and cross-job isolation without adding a requirement that repeated runs must select the same worker.
- Actual: both replies add repeatability to the acceptance conditions. Capture writes `同一個工作在相同條件下重複執行,執行者選擇的結果一致。`; code-only proposes `同一個 job 重複執行,選人的結果一致,不再因為別的 job 而變動。`
- Impact: a legitimate own-job rule could select by load or randomness. Isolation does not establish deterministic selection or universal output consistency.
- Location to examine: both owners' first-restatement paragraph and the interview boundary for observable Acceptance outcomes.
- Why prior checks missed it: the response connects all required concepts and passes a structural content checklist; those checks do not establish that every new obligation follows from supplied facts.
- Suggested edit class: preserve the supplied outcome's strength. Explain the consequence of the reported defect without converting it into a broader guarantee; leave additional desired outcomes unresolved rather than adding them to acceptance.
- Evidence: `claude-code-dogfood-evidence.md`, capture-6-r2 and code-6-r2 actual replies and captured drafts; both blind audits independently identified this issue.

## D2 — Offered an unsupported factual fallback

- Classification: Medium × Output-quality; informed execution plus blind audit.
- Probe: capture-4-r2 asks for a release-date correction, but the correct date is not supplied.
- Expected: keep the actual date unknown pending an answer or release evidence.
- Actual: after correctly asking for the actual date, the reply says `我的建議是用實際發佈日。你若不確定,就用今天。`
- Impact: the user could authorize a date that is not the release date. No incorrect date was actually written, and the draft remains open.
- Location to examine: capture-intent's missing-information interview and first-restatement context requirements.
- Why prior checks missed it: asking a factual question and preserving open status satisfy the structural boundary, while the recommendation still introduces unsupported content.
- Suggested edit class: uncertainty must remain explicit; a missing factual value does not justify recommending a convenient replacement value.
- Evidence: `claude-code-dogfood-evidence.md`, capture-4-r2; both blind audits independently identified this advice.

## D3 — Internal terminology and excess bookkeeping remain

- Classification: Medium × Jargon-leak / Output-quality; informed execution plus blind audit.
- Probe: all six repaired-harness replies, especially the familiar date correction.
- Expected: explain the requirement and needed authorization in proportionate, user-facing language.
- Actual: replies still display labels such as `open`, `needs-design: no`, `closing-review`, `Ready PR`, and branch/commit bookkeeping. The simple date request receives multiple sections before its single missing factual value is resolved. Code-4 also opens with `我已經確認了意圖` while later requesting confirmation.
- Impact: core background is more explicit, but the reader still has to interpret process vocabulary and inconsistent confirmation wording. This is not a claim that tables or headings are inherently wrong.
- Location to examine: first-restatement and publication-consequence prose in both owners.
- Why prior checks missed it: the required information is present, but presence does not establish readability, proportionality or consistent state language.
- Suggested edit class: lead with the user's problem or missing fact; disclose concrete upload/review-request consequences; keep internal labels secondary and pending status consistent. Do not impose a replacement fixed sentence template.
- Evidence: the six actual replies in `claude-code-dogfood-evidence.md`; both blind audits agreed on this limitation.

## Raw outputs and reproducibility

`claude-code-dogfood-evidence.md` preserves the six repaired-harness replies verbatim and metadata for every attempt, including raw-JSONL hashes. Full local transcripts, exact fixtures, settings, launch script and both unmodified audit JSON files remain under `/tmp/loom-context-claude-dogfood/`. Run parameters explicitly selected the model and effort, disabled hooks/auto-memory, excluded user memory, and loaded temporary plugin copies. File tools used restricted roots; allowlisted Bash subprocesses were not an OS-level filesystem boundary. These controls do not validate normal installed-host behavior with hooks enabled.

This report adds evidence only. Existing acceptance and attestation files describe their earlier, narrower source-loaded tests; they must not be presented as proof that these new Claude Code findings passed. Resolve findings and obtain fresh affected evidence before declaring the candidate fully ready on this host. This dogfood pass discovers and reports; it does not modify the skills.
