# Second-vendor mode routing

An independent cross-model review counts only when the selected model's provider
family differs from the current model's family. A CLI name does not establish
its family: `agy` can list models from several families. Locally check installed
`claude`, `codex` and `agy` as candidate executors on Codex, Claude Code or
Antigravity CLI; exclude the current model family once known. An installed
`agy` with no selected model is availability-unverified, not a verified
outside reviewer. The downstream `loom-code:external-review` skill selects
and checks an explicit model and effort after authorization. Detect a candidate with
`command -v <cli>` **and** a probe that it runs — `<cli> --version` must
exit 0. In zsh `command -v` may print an alias or a function body rather
than a path; do not try to parse it. **Any non-empty output plus a
`<cli> --version` that exits 0 counts as present**, and nothing else
does. Never `which`: it reports shell aliases and stale hashes, and
suggesting a tool that turns out not to run costs the user a question for
nothing. A different executable alone does not establish independence.

When `docs/loom/KICKOFF-DEFAULTS.md` has no `second-vendor:` line, create
the file from capture-intent's `templates/KICKOFF-DEFAULTS.md` if
needed and record `second-vendor: suggest`. `suggest` adds no question at
capture-intent. Pass the observed mode forward; write-plan owns the
post-plan availability or recommendation notice and its response timing.

This standalone plugin does not call `second_vendor_policy.py` and does not
reimplement its risk mapping. That executable belongs to loom-code.

**`ask`** puts one cross-model review question into decision point ① only when
the user has not already made a qualifying choice. Skip the per-change question when a direct user request names an outside coding agent and an unambiguous active review target.
Quote that request, target and final `selected_executor` as
`authorization_source` in the downstream execution record; a direct request
authorizes one bounded review without a
second confirmation. Show cost, vendor-egress, `review_root`, outside-root
read and local-execution disclosures before discovery or dispatch. If the
provider or target is ambiguous, or material scope expands, ask for the
missing choice. A suggestion alone does not authorize execution; under `ask`
the question below still applies. Probe local candidates first. With a
runnable candidate, prefer the current host's native question tool. Claude Code
uses `AskUserQuestion` when available in the current agent; the authoritative
tool reference names that tool and owns its live schema
([Claude Code tools reference](https://code.claude.com/docs/en/tools-reference)).
Codex uses `request_user_input` only when the host exposes it in the active
mode; its live tool schema owns the valid question shape and availability, and
the official implementation enforces both mode and root-thread availability
([Codex handler](https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/request_user_input.rs)).
Treat the two choice meanings as `decline this change` and `use <tool>`, and
render both choices in the user's current conversation language. If the
interface requires a recommended choice, mark `decline this change` as
recommended so quota use and repository-data egress remain opt-in. If the
candidate runs but no native question tool is available, ask one blocking
plain-language Markdown question with the same choices and no fabricated
recommendation. If there is no runnable candidate, state that no local review
executor is available and continue without asking. An `agy` candidate without
selected model evidence is unverified, not a confirmed model family.

The answer governs this change only and never rewrites the KICKOFF line. Add
an actual question to the running list kept in SKILL.md, so it lands in the
plan's `## Questions asked`; a direct request adds no question. Pass the
accepted CLI or decline to Closing Review. A named CLI is not a confirmed
provider family until a concrete model is selected and checked.

A **fixed CLI** is the standing reviewer choice and adds no intent question.
Probe it with the same local availability rule before downstream use; never
replace it silently with another vendor. Antigravity can be an executor when
`agy` lists a concrete non-host-family model and the shared runner accepts its
explicit model and effort; local installation alone proves neither property.
When selection or execution fails, Closing Review reports the limitation and
never silently drops the second vendor.
