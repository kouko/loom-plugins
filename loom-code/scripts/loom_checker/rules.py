from __future__ import annotations

import sys

from loom_checker.probes import MAX_PROBE_PROGRAMS


RULES: list[tuple[str, str]] = [
    (
        "adversarial.proportionate",
        f"A change produces at most {MAX_PROBE_PROGRAMS} adversarial probe "
        "programs, and every one of them carries a non-empty `concern:` line in "
        "its first lines naming the kind of defect it defends against. Both "
        "halves are recomputed at finalize-review over the union of three sets, "
        "because no one of them is the whole of what the step produced: the "
        "programs the selected commit holds anywhere in the change's store, "
        "whatever their extension; the programs finalize-review is about to "
        "execute; and the programs this branch adds straight into the package "
        "suite the repository declares, which the `concern:` line marks as the "
        "adversary's output rather than ordinary new tests. A graduated program "
        "therefore still spends against the ceiling, which reading the store "
        "alone could not see, since the graduation gate empties that directory "
        "first. A program committed elsewhere in the change's store, outside its "
        "`evidence/probes/` directory, is refused rather than left uncounted.",
    ),
    (
        "contract.requires",
        "A consumer plugin's requires-contract floor is met by this contract manifest version: "
        "the same major, and a minor at or above the required one.",
    ),
    (
        "contract.charter-complete",
        "Every artifact in the contract manifest carries a complete `charter:` block -- "
        "non-empty answers/readers/must/must_not/edits_after, a must_not goes_to naming "
        "another artifact in the table, and a signoff naming a real station.",
    ),
    (
        "intake.confirmed",
        "write-spec / write-plan accept only an intent whose status line reads `confirmed <date>` "
        "with a date the calendar has; `closed <date> — PR #<N>` or `closed <date> — branch <name>` "
        "is blocked -- that change is closed and a new change starts from a new intent. closed is "
        "terminal either way, and a confirmed intent is also blocked after canonical delivery evidence "
        "appears on the selected remote-default snapshot. Local branches and worktree evidence never "
        "prove delivery; an unresolved remote default is indeterminate and blocks intake.",
    ),
    (
        "intake.confirmed-behavior",
        "write-plan accepts a product change only when its spec carries a "
        "`confirmed-behavior: <date> @<spec-blob-sha7>` line naming the spec as it stands.",
    ),
    (
        "intake.test-case-pair",
        "Every task in a newly authored plan names the intent Acceptance lines it owns, "
        "and each named line has positive plus negative or boundary test cases.",
    ),
    (
        "intake.spec-ready",
        "write-plan accepts a needs-design: yes change only when its spec exists and carries "
        "an explicit `pre-build-review: required|not-required — <reason>` declaration. Review "
        "independence is enforced by the write-spec station, not persisted in a ledger.",
    ),
    (
        "intent.kind-recompute",
        "kind: engineering is rejected when the diff touches a declared interface-surface glob.",
    ),
    (
        "intent.needs-design-reason",
        "The needs-design line carries a reason and appears verbatim in the message of the "
        "commit that last changed the intent's status or needs-design line.",
    ),
    (
        "intent.needs-design-recompute",
        "needs-design: no is rejected when the diff touches a declared interface-surface glob.",
    ),
    (
        "intent.product-no-identifiers",
        "A product intent's Problem section names no file path, code identifier or script filename.",
    ),
    (
        "intent.schema",
        "The intent file carries every required frontmatter field and H2 section declared in the contract manifest.",
    ),
    (
        "plan.field-caps",
        "A plan whose frontmatter carries a `charter:` key (any value, presence only) caps each "
        "task's Test and Risk lines at 40 words, its Files line at 8 comma-separated entries "
        "(a comma inside backticks does not split), each numbered `## Risks` item at 40 words, "
        "and each `## Current State Evidence` bullet at 30 words -- CJK runs with no internal "
        "whitespace count as one word by len(text.split()); a task missing its Files, Test or "
        "Risk line blocks too. A plan with no `charter:` line is skipped entirely.",
    ),
    (
        "spec.req-grammar",
        "Every Requirements entry reads `REQ-<n> — <name>` with n contiguous from 1, "
        "unique, and points at an Acceptance number the intent actually carries.",
    ),
    (
        "spec.ui-flows-recompute",
        "While the diff touches a declared interface-surface glob, the spec's UI flows section "
        "carries at least one prose line (outside fences, indented code and HTML comments) with an arrow and "
        "at least four visible characters on each side. This is a structural floor only -- "
        "whether the flow says anything true or useful is the reviewer lens's job, not a "
        "keyword list's. Runs at write-plan intake only.",
    ),
    (
        "standing.product-principles-reject",
        "A product change is rejected until PRINCIPLES.md is ratified: a `ratified-by: <name> "
        "<YYYY-MM-DD>` signature with a real date, over three or more distinct non-negotiables.",
    ),
    (
        "standing.second-vendor-valid",
        "KICKOFF-DEFAULTS rejects the removed `second-vendor: none` value with explicit "
        "migration guidance to use the non-blocking `suggest` mode.",
    ),
    (
        "standing.silence",
        "KICKOFF-DEFAULTS `standing-docs: waived` silences the WARN only, never the product rejection.",
    ),
    (
        "standing.warn",
        "A missing PRINCIPLES.md, DESIGN.md or ARCHITECTURE.md prints the fixed three-line WARN and never blocks.",
    ),
]


RULES.append((
    "publish.preconditions",
    "publish pushes HEAD and opens or updates its one pull request only when the change "
    "is identified, publication is authorized, git and gh resolve to trusted executables, "
    "origin is a literal GitHub URL, and HEAD, the remote branch and the PR identity stay "
    "unchanged across every network step; the verification status is disclosed, never "
    "a refusal.",
))


RULES.append((
    "push.contextual-body",
    "The exact pull-request body carries Ship's nine top-level contextual headings "
    "exactly once and in order, with no competing Memory heading or explicit claim "
    "to expose private or hidden chain-of-thought.",
))


RULES.append((
    "ci.pr-floor",
    "The pr-floor CI check fails only when the pull-request body lacks Ship's nine "
    "contextual headings in order, naming the heading; the verification status is "
    "recomputed from git and published as a notice, and every status passes.",
))


RULES.append((
    "land.merge",
    "land merges nothing unless every precondition holds: the change identified from the "
    "branch name or its one intent file, an --accepted-by name equal to the intent's "
    "originator or publication authorizer, a live PR body with the nine contextual "
    "headings, one open PR whose head is HEAD, every check passed (not only required "
    "ones), and a MERGEABLE state other than BLOCKED, DIRTY, BEHIND, UNSTABLE, or DRAFT. "
    "No attestation is required; an absent or stale one is printed after the merge.",
))


RULES.append((
    "land.verify",
    "After land merges, the squash commit read back from the trunk carries the PR title "
    "and the PR body; otherwise land stops before trunk sync and cleanup.",
))


RULES.append((
    "land.cleanup",
    "land removes a change's worktree and branches only when its PR is merged, the "
    "worktree is clean apart from regenerable caches, and each branch tip equals the "
    "merged PR head, selected by exact branch name; a changed sweep list removes nothing.",
))


RULES.append((
    "review.sync",
    "sync-trunk merges the freshly fetched origin trunk into the change branch before "
    "closing review, never rebasing or forcing: it refuses a trunk checkout, a detached "
    "HEAD or a dirty worktree untouched; adds no commit when HEAD already contains the "
    "trunk tip; on conflict names every conflicting file and leaves HEAD and the "
    "worktree untouched (detected in memory, or merged then aborted when git cannot); "
    "an unreachable remote only warns.",
))


def list_rules(out=sys.stdout) -> int:
    for rule_id, description in sorted(RULES):
        out.write(f"{rule_id}\t{description}\n")
    return 0
