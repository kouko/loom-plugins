# Engineering research — spec
intent: 2026-11-08-engineering-research-skill@da402f1b
pre-build-review: required — A portable research-record contract and optional cross-system Vault writes introduce persistence and privacy boundaries.

## Requirements

REQ-1 — Optional discoverable capability
  The loom-workflow plugin shall expose engineering-research through its installed skill discovery and optional router without making research a lifecycle station or prerequisite for unrelated work. → Acceptance #1

REQ-2 — Consequential-gap routing
  WHEN an unresolved factual premise could change an engineering decision during a Loom task or standalone engineering discussion, the agent shall consider research proportionate to that gap while preserving the owning task and its authorization; routine lookups with no consequential gap shall remain ordinary work. → Acceptance #2

REQ-3 — Premise, evidence and artifact verification
  The research agent shall check the question's premise and relevant project/version/environment conditions, distinguish observations, source claims, inference and untested claims, and inspect the actual evidence and any claimed saved artifact before reporting completion. → Acceptance #3

REQ-4 — Question-led evaluation
  WHEN research includes an engineering assessment, the agent shall select the smallest suitable method or complementary methods for distinct gaps, record why they fit, and allow direct factual answers without a named framework or mandatory source/tool counts. → Acceptance #4

REQ-5 — Durable question-scoped records
  The research agent shall retain one portable Markdown record with flat frontmatter per independently answerable question, update the same question under unchanged conditions, and preserve and link the earlier record when material conditions require a new revalidation. → Acceptance #5

REQ-6 — Honest unsaved outcome
  IF writing is prohibited or unavailable THEN the research agent shall provide an explicitly unsaved draft and identify the missing saved artifact without overriding the boundary or claiming persistence. → Acceptance #6

REQ-7 — Implementation and relation grounding
  WHEN researching GitHub/GitLab implementation behavior or recording structured relationships, the agent shall inspect relevant source and connected conditions, use diagrams only when useful, and identify evidence status without inferring verified causality from diagram structure or rendering. → Acceptance #7

REQ-8 — Consented long-term preservation
  WHEN a change is verified merged into main and its research has enduring or cross-repository value, the finishing agent shall offer a concrete Obsidian preservation candidate, require release evidence for release-dependent claims, and write only after that instance's destination and scope are explicitly authorized while preserving the project original and repository/revision provenance. → Acceptance #8

REQ-9 — Evidence-bounded delivery
  The implementation shall provide actual discovery, workflow-handoff and behavioral acceptance evidence and identify which results concern frozen prototypes, the formal skill, isolated loaders or untested installed hosts. → Acceptance #9

## Design decision

- user-decided — Use one Markdown file per research question with frontmatter: “那就依照你的建議 按研究問題分檔 以及採用 frontmatter 吧”.
- user-decided — Inspect implementation beyond README for repository research: “另外我也想要針對 github / gitlab repo 的研究時 讓 agent 知道除了閱讀 README.md 之外 也需要直接閱讀原始碼確認”.
- user-decided — Include research methods and source rules: “可以幫我把剛才討論的研究方法跟資料來源規則加入 skill 內嗎？”.
- user-decided — The confirmed intake includes post-merge preservation proposals with per-instance Vault-write consent; this change does not authorize any present Vault write.
- agent-decided — Promote the revision-5 package, retaining methods, source policy, evaluation selection, optional structured relations and a research template as directly linked single-level bundled files. Conditional references preserve lightweight factual checks rather than loading all evaluation domains every time.
- agent-decided — Expand the description to include standalone engineering discussions and decision-critical small checks. Intent/spec/planning and build are examples of useful moments, not exclusive scope. A lookup's low cost does not make a consequential unresolved premise routine.
- agent-decided — Initial conversation/artifact orientation may establish the question, current revision and existing evidence. Load method/source guidance before collecting new substantive evidence or executing a new experiment; reused evidence still receives applicability checks. This removes the prototype's ambiguous read-order instruction without forcing redundant research.
- agent-decided — Add short optional calls at intent, spec, plan and build evidence-gap locations plus the workflow router. These are invitations to the capability, not new blocking prose gates. No researcher advances a user decision point, installs tools or publishes on the user's behalf.
- agent-decided — Active-change records use `docs/loom/<change-id>/research/<sequence>-<topic>.md`; without a change use `docs/loom/research/<YYYY-MM-DD>-<topic>.md`. Allocate by existing contents and unused names, do not overwrite a distinct question. These paths define adopting-project stores, not links to this repository's development history.
- agent-decided — Require flat `title`, `type: loom-research`, `status`, `created`, `updated`, and list `tags` containing `loom/research`; `change` is optional and factual. Status is `in-progress`, `concluded` or `superseded`, not acceptance or confidence. Unresolved research may conclude honestly. Preserve created dates and explicit frozen/no-edit boundaries.
- agent-decided — After the existing merge/cleanup completes, Ship may load engineering-research's preservation guidance by skill name if available and relevant records exist. Follow the printed cleanup destination before further filesystem work. For a previously merged change, explicit research invocation can perform the same check. No background monitor, mandatory fourth Loom checkpoint or promise to notice a later release while idle is introduced.
- agent-decided — Keep preservation guidance in a directly linked reference owned by engineering-research; Ship delegates by skill name and never reads another plugin's files directly. The research skill remains useful without Ship or Obsidian installed, and Ship remains usable without loom-workflow.
- agent-decided — Verify the exact merged change and stable revision before preparing a candidate; a locally closed intent, green CI or publication alone is insufficient. Release-dependent findings remain pending until relevant release evidence exists; independently supported source findings may be offered with their actual scope.
- agent-decided — Discover configured Vaults through available official Obsidian CLI capabilities, inspecting local help/version before choosing supported query syntax. A folder name or Vault presence establishes neither destination preference nor authorization. If CLI is unavailable, use a user-supplied destination or present an unsaved candidate; multiple results do not permit arbitrary selection. Do not install or start a new service for discovery.
- agent-decided — Prepare the candidate content and provenance before asking to write it. Request destination and content scope together; do not offer only an abstract permission request. Recheck permission and target before writing. Refusal, missing Vault, delayed release, failed cleanup or unavailable evidence never reverse the merge or block original task completion.
- agent-decided — Keep originals, use ordinary Markdown links and pinned repository revision/source references in the Vault copy, and require separate authorization for overwriting any existing note. Read back an authorized saved note before reporting it saved. The future adoption workflow may ask this optional external-write question; the present implementation session writes no Vault note.
- agent-decided — Register engineering-research as a counted workflow tool, not as an allegedly standalone budget exemption. Declare the added mechanism/maintenance cost through the existing budget-exception convention and executable registry checks. No new checker rule or runtime schema gate is needed merely to recommend evidence-backed behavior.
- agent-decided — Validate the formal package with isolated real loader and behavioral runs; do not update existing user/global installations. A discovery benchmark measures routing separately from explicit-invocation workflow success and does not establish improved causal research quality.

## Alternatives considered

- Keep only the prototype: rejected because installed discovery and workflow ownership remain absent.
- Put all research and frameworks in the main skill: rejected because simple facts would load irrelevant domain guidance.
- Use one research file per implementation cycle: rejected because unrelated questions and revalidation histories become entangled; the user chose per-question records.
- Force every lookup through research or every research through all frameworks: rejected because cost grows without a demonstrated decision benefit.
- Automatically export when a Vault folder exists: rejected because filesystem discovery does not authorize an external write or select a destination.
- Require Vault export before merge: rejected because preservation value and release validity are established later and optional export must not become a merge gate.
- Add polling or automatic release watchers: rejected because an on-demand capability and the existing finishing task cover the authorized scope.

## Current state evidence

- Forward: `loom-workflow/skills/using-loom-workflow/SKILL.md` — router request table lists optional tools but no engineering-research; `loom-design/skills/capture-intent/SKILL.md` — Step 1 gathers facts without a research-tool handoff.
- Reverse: `loom-code/skills/ship/SKILL.md` — §5 and Handoff finish after land and cleanup; no post-merge research preservation owner exists. `loom-workflow/tests/scripts/test_skill_count.py` — COUNTED and OPTIONAL_ROUTERS pin shipped discovery boundaries.
- Error: `docs/skill-dogfood/2026-11-08-engineering-research-frameworks/report.md` — read-order observations and host/coverage limits; the prototype's `SKILL.md` says “Before gathering evidence” despite earlier premise/orientation steps.
- Data: `docs/loom/2026-11-07-engineering-research-trial/revision-5-framework-selection/candidate/engineering-research/templates/research.md` — flat metadata and evidence sections; `loom-code/contract/manifest.yaml` — tools registry; `docs/loom/evidence/mechanisms.yaml` — mechanism population and budget evidence.
- Boundary: `PRINCIPLES.md` — fixed three-plugin boundary, skill-name delegation, non-negotiables 4 and 5; confirmed intent Constraints and Out of scope exclude mandatory new gates, automatic Vault writes, installation changes and automatic merge.

## UI flows

N/A — This engineering change adds agent instructions and portable research records rather than a new application UI or command; persistence and external-write conditions are defined in REQ-5, REQ-6 and REQ-8.
