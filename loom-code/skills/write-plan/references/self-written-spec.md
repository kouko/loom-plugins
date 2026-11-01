# Writing the minimal spec yourself

Loaded by step 4 of `../SKILL.md` when this station writes the spec
itself. Relative paths here are relative to this file's directory; step
numbers are that SKILL.md's.

When a task's rationale outgrows its Risk line, write
`docs/loom/<change-id>/spec.md` from `contract/templates/spec-minimal.md` —
Requirements one per Acceptance line, Design decision one line per
agent-decided fork, Alternatives considered, Current state evidence, UI
flows (N/A unless a carried detail is visible) — carrying the template's five
sections and leaving the `confirmed-behavior:` line to product changes.
Decision point ② stays product-only. Declare `pre-build-review: required|not-required — <reason>`
using the risk classes below; only a required spec gets a pre-build review.

A non-empty carried-details list — from `capture-intent`'s hand-off or your
own intake — forces that spec even when every Risk line fits; record each
item per the `Record each carried detail` bullet below. An empty list forces no spec.

**`yes`, spec missing, `loom-design` not installed** — you write a minimal
spec yourself, from `contract/templates/spec-minimal.md`:

- Set `intent: <change-id>@<confirmation-sha>` and agent-decide
  `pre-build-review: required|not-required — <reason>`; require review for
  security/privacy, irreversible data, public contracts, cross-system
  architecture, or materially ambiguous requirements.
- Map each Acceptance line one-to-one to `REQ-<n> — <name> → Acceptance #<n>`.
- Fill UI flows (action and response, or `N/A`), Design decision,
  Alternatives considered, and path-anchored Forward/Reverse/Error/Data/Boundary
  evidence. Do not show those internal sections to the user.
- UI flows form: a short flow is `<action> → <reaction>` lines; several
  parallel cases on one surface, a table `case | what the user does | what
  they see`; states or paths that branch or go back and forth, a Mermaid
  `stateDiagram-v2` or `flowchart`.
- Record each carried detail as a UI flows line when visible, else as a clause
  on a Requirement line — the two parts decision point ② shows; only an
  engineering change may put one on a Design decision line instead. That
  clause goes on the Requirement line of the Acceptance line the detail
  serves, never a new REQ. An agent proposal the user did not agree to is not
  recorded.

Print one line for the user: installing `loom-design` gets them a fuller
spec than this one. For `pre-build-review: required`, dispatch one
fresh-context `loom-code:reviewer` with lens `spec+adversarial`, the spec
commit's parent (`<spec-commit>^`) as `reviewed_sha`, and the intent and
spec as ground truth; it must pass before planning, with no acceptance testing, adversary, or
`finalize-review`. On NEEDS_REVISION, close each finding, commit, and send
only those fixes back to that reviewer. For `not-required`, proceed without a
formal spec review; `intake.spec-ready` blocks a spec with no declaration.

Running ② on a product spec you wrote: when a flow has parallel cases or
branches, lead with a table or a text (ASCII) diagram, then the per-case
sentences; never put Mermaid in this message — a terminal shows it as raw
code.

<!-- gate: write-plan.product-spec-needs-confirmed-behavior -->
**A product spec needs `confirmed-behavior:` before it becomes a plan.**
When `kind: product`, decision point ② belongs to whoever wrote the spec.
Present the Requirements, UI flows and product
one-way doors in plain words — "you type ___ and you see ___; when ___
happens it will ___" — and nothing from `## Design decision` down, ever.
Doors asked at ① are not asked again at ②. On
"yes", write `confirmed-behavior: <date> @<spec sha7>` into the spec
frontmatter, where `<spec sha7>` is the first seven characters of
`git hash-object docs/loom/<change-id>/spec.md` after the spec's last
edit, pinning the text the user approved. On a correction, rewrite,
present again, and recompute the hash. Engineering changes skip this.

When done, return to step 4's intake check.
