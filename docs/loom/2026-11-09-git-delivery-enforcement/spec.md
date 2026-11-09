# Git delivery enforcement — spec
intent: 2026-11-09-git-delivery-enforcement@4c555b14
pre-build-review: required — publication authorization, local Git hook execution, server protection and four host boundaries affect security and cross-system behavior.

## Requirements
REQ-1 — Observed delivery
  WHEN delivery is checked, Loom shall distinguish uncommitted work, unpublished commits, absent or mismatched PR, incomplete checks, published PR and merged PR using current Git/server evidence, and shall not report the requested target complete when evidence is incomplete or unavailable → Acceptance #1
REQ-2 — Delivery authorization
  WHEN a check runs, Loom shall keep read-only observation separate from publication and merge authorization, support an explicit local-only target without remote writes, and never infer permission to publish or merge from a successful observation → Acceptance #2
REQ-3 — Git-native trunk protection
  WHERE repository protection is installed, ordinary commits and merge commits on the default/main/master branch shall be refused independently of shell spelling, feature-branch operations shall remain possible, existing hooks and work shall be preserved, and safe synchronization of an already published remote trunk shall remain possible → Acceptance #3
REQ-4 — Observed remote protection
  WHEN remote protection is inspected, Loom shall distinguish effective PR/check requirements from absent or unconfirmed requirements, provide a setup remedy without applying it, and preserve server enforcement of direct-push and required-check restrictions in a configured environment → Acceptance #4
REQ-5 — Non-success remains non-success
  WHEN publication or merging observes failed, cancelled, pending, unknown or inaccessible checks, Loom shall return distinguishable outcomes and shall not merge or fall back to direct trunk updates because of that outcome → Acceptance #5
REQ-6 — Actionable failures
  WHEN a scoped delivery, protection or publication/merge check cannot succeed, its result shall carry the observed reason and a safe corresponding next action, including the missing condition when automatic repair is not justified, without recommending bypass or data discard → Acceptance #6
REQ-7 — Policy and host integration
  WHEN a change is small or engineering-only, Loom shall retain repository branch/PR policy, expose the same executable delivery observation on every supported host, and use documented host continuation hooks where available while reporting unsupported termination enforcement explicitly → Acceptance #7

## Design decision
- user-decided — preserve the existing publish/land flow and reuse current scripts; the user accepted 1B + 2A/B + 3B and requested the remedy alongside each scoped error. The user's later reuse request removes unnecessary proposed files, not any Acceptance obligation.
- agent-decided — put `cmd_delivery` and observation helpers in existing `command_handlers/publish.py`, import their narrow helpers from land, and route `delivery` through `scripts/loom_checker.py`. No separate delivery command-handler or orchestration service is added. Retain existing trust-root executable resolution, origin identity and environment protections.
- agent-decided — the read-only command accepts `--goal local|published|merged` (default published), optional committed `--intent <path>`, `--json`, and internal `--hook`. Emit a small result with `state`, `reason`, `next`, `evidence` and `complete`. Exit 0 only for the requested observed goal, 1 for observed incompletion, 2 for malformed input/unavailable evidence; hook framing translates these facts but never performs writes. A local-only goal must be explicit; absent publication authorization is not proof of local-only intent.
- agent-decided — use HEAD, selected origin/default branch, live remote refs and exact PR head/base/repository identity; do not trust PR-body verification declarations or remote-tracking refs as live proof. Require exact HEAD equality for open publication. For merged PRs, use the server merge state and merge SHA rather than ancestry of pre-squash commits. Require matching repository/base and the selected branch identity; a merged PR for an older branch head does not deliver newer local commits. Validate live branch/HEAD stability across reads.
- agent-decided — reject uncommitted paths attributable to this change: committed branch-delta paths plus concrete Files entries in its committed plan; include untracked matches, deletes and staged edits. Preserve unrelated paths without staging or deleting them. Without an attributable scope, do not claim that unseen working-tree code was delivered; report the attribution limitation. An authorized skip may publish absent verification under the existing policy; delivery completeness does not certify acceptance quality or override explicit skip rules.
- agent-decided — reuse CI classification for required-only publish and all-registered land observations, keeping these policies distinct. A valid JSON failure response remains a check failure even when gh exits 1; it is not automatically an authentication failure. Unknown/malformed/error responses remain unconfirmed. Preserve bounded waits and empty-registration semantics; a PR with no configured required checks can be published but must report that fact rather than claim checks passed.
- agent-decided — all new result categories include an explicit next action; existing scoped refusal paths append a safe next-action line without changing legacy BLOCK prefixes or exit codes. Prefer typed call-site information over regex guesses about arbitrary stderr; an unclassified external failure asks for diagnostics and says not to switch merge routes. No auto-executed remediation registry or new retry budget.
- user-decided — revise PRINCIPLES.md's no-Git-hooks fixed choice for explicit repository-level protection. This affects the user's ordinary Git operations too. No user's existing repo protection, hook or GitHub setting is changed by this development task; installation is an explicit adopter action.
- agent-decided — extend existing `push.py` with `--install-git-hooks`, `--git-hook <pre-commit|pre-merge-commit|pre-push>` and `--remove-git-hooks`. Resolve the repository's effective hooks directory (including core.hooksPath and linked worktrees), use exclusive creation and managed-content checks, and refuse existing foreign hooks rather than overwrite or silently chain them. Idempotent install verifies all managed contents. Removal deletes only matching managed files. Tiny installed wrappers call the installed plugin's existing launcher; unavailable runtime blocks with its repair advice. No network repair runs in a Git hook. Protect the remote trunk destination in pre-push, not only the currently checked-out branch. Git-native hooks are not an unbypassable security boundary; fast-forward local merges may not create a commit, while server PR rules protect remote trunk updates.
- agent-decided — keep the existing shallow shell guard as early feedback on repositories without native protection. Do not grow a shell grammar parser. Native guard failures give the branch and a preserve-work branch/worktree remedy, not advice to set protectMain=false or use no-verify.
- agent-decided — Claude Code and Codex have documented Stop hooks. A shared hook entry reobserves delivery only for an identified confirmed change with automatic-publication authorization; allow open/unconfirmed changes, explicit local-only targets, required product behavior confirmation, already published PR awaiting acceptance, and irrelevant/child hooks. Block a premature stop once with the observed missing step and safe remedy. On `stop_hook_active`, emit the observed incomplete/unconfirmed state to the user without another forced continuation; external blockers do not create infinite loops. This is bounded recovery, not an assertion that arbitrary final prose can be mechanically certified.
- agent-decided — OpenCode v2's documented SessionHooks interface exposes prompt/context/model/transport/retry hooks but no Stop hook. Keep its existing adapter and use the same executable delivery command plus a startup capability disclosure; do not invent an undocumented event or claim enforced termination. Antigravity has no verified termination decision in the installed adapter: use the same command and disclose that boundary. Native Git protection is host-independent. This preserves all hosts' ability to execute checks without pretending equal termination capability.
- agent-decided — strengthen github-rules observation only within its existing advisory/setup boundary, including bypass visibility for the required-check ruleset. Existing explicit setup consent remains separate from code delivery. A configured test server/fixture can prove the refusal contract without changing real project rules; independent acceptance must distinguish simulated server decisions from live GitHub enforcement.

## Alternatives considered
- A separate delivery engine, command wrapper, Git-protection script and recovery registry: rejected because publish/land/push already own these facts/actions; user explicitly requested reuse.
- Only reword station instructions: rejected because historical agents already ignored equivalent rules.
- Expand shell parsing to every wrapper/subshell: rejected because native Git and server rules cover ordinary operations without rebuilding a shell parser.
- Unconditionally block every end of every turn: rejected because it breaks intent/behavior/acceptance questions and can loop on unavailable credentials.
- Enforce valid review evidence at every merge: not adopted; this changes the separate existing explicit-skip policy and is not necessary to observe whether actual content was published.
- Install protection globally or overwrite existing hooks: rejected; authorization is scoped to explicit repository installation and preserves existing work.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker.py:COMMANDS`; publish and land are existing entry points, no read-only delivery command.
- Reverse: `loom-code/skills/ship/SKILL.md:Publish once` and `Land after acceptance`; hosts call `push --hook` through their installed definitions.
- Error: `command_handlers/publish.py:_external_or_block` and `land.py:_observe_all_checks`; failures are text/exit-code based, with inconsistent diagnostic versus failed-check treatment.
- Data: `publish.py:_cmd_publish_trusted` already compares exact remote HEAD and PR identity; `verification.py:verification_status` concerns review evidence, not delivery completion.
- Boundary: `push.py:DIRECT_GIT_CHANGE` checks literal shell starts; `hooks/hooks-codex.json`, `hooks/hooks.json`, `opencode/loader.js:registerHooks`, `hooks/agy_adapter.py` own host framing; `github_rules.py` prints setup but never applies it.

## UI flows
| Case | Action | Observable result |
|---|---|---|
| Empty/no change | Run delivery without identifiable committed intent | Non-success reason and guidance to identify the change; no remote write |
| Local-only | Run delivery with local goal | Attributable pending changes prevent completion; otherwise report local completion without a network operation |
| Unpushed | Check published goal after a local commit | Incomplete with local/remote evidence and advice to resume publish |
| Missing/mismatched PR | Check published goal | Incomplete with exact mismatch and a safe publish/reconcile remedy, not a claim that PR existence is enough |
| In progress | Required CI is pending | Pending with advice to continue bounded observation; no merge |
| Error/unconfirmed | Server/credentials unavailable or response malformed | Unconfirmed, diagnostic evidence and missing condition; no fabricated check failure/success |
| Success | Exact publication target or merged PR is observed | Complete for that goal, PR URL and explicit CI/merge evidence; no automatic merge authorization |
| Native hook | Attempt a main commit/merge commit or trunk-destination push | Nonzero exit, protected branch and safe next action; feature operations and ordinary remote-trunk sync remain available |
| Installer conflict | Install/remove with foreign or edited hooks | Refuse and name conflicting paths; leave files/config unchanged |
| Stop supported | Identified authorized change ends before publication | One continuation with observed reason/remedy; repeated continuation or external blocker is surfaced as incomplete, not looped |
| Stop unsupported | Use OpenCode/Antigravity | Explicit capability limitation and the shared delivery command; no assertion that termination was blocked |

## Supporting evidence
- Complexity analysis: `evidence/complexity-analysis.md` (revised to reuse existing scripts after user feedback).
- Host references: [Codex Stop hooks](https://learn.chatgpt.com/docs/hooks#stop), [Claude Stop hooks](https://code.claude.com/docs/en/hooks#stop), [OpenCode SessionHooks](https://opencode.ai/docs/build/plugins/server#session-reference). Retrieved 2026-11-09; protocol support is documentation evidence, not a live host execution claim.
