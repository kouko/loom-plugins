#!/usr/bin/env python3
"""The loom checker -- the single deterministic layer of the loom flow.

Every rule here RECOMPUTES its fact from the repository (the intent file,
the manifest, the git diff, or the generated attestation). No rule
trusts an agent's claim about itself; concept-model §7 is explicit that
this layer stops missed steps, not a goal-directed agent.

Sub-commands (the CLI contract other stations depend on):

    loom_checker.py --list-rules
    loom_checker.py --help
    loom_checker.py intent <path> [--commit-msg <file>]
    loom_checker.py intents [<change-id>] [--remote <name>] [--metadata]
    loom_checker.py intake <station> <change-id>
    loom_checker.py push --hook
    loom_checker.py publish --intent <absolute-path> --title <text> --body-file <absolute-path>
    loom_checker.py publish --confirm-authorized --title <text> --body-file <absolute-path>
    loom_checker.py delivery [--goal local|published|merged] [--intent <path>] [--json]
    loom_checker.py land --accepted-by <name>
    loom_checker.py land --cleanup <branch>
    loom_checker.py land --sweep [--confirm <token>]
    loom_checker.py sync-trunk
    loom_checker.py github-rules [--print-setup]
    loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha> [--branch <name>]
    loom_checker.py reviewer-count <change-id>
    loom_checker.py finalize-review <change-id> --input <review-input.json>
    loom_checker.py standing <path-to-intent>
    loom_checker.py contract --require <major.minor>
    loom_checker.py charter [--manifest <path>]
    loom_checker.py plan <path-to-plan.md>

With the launcher, the checker is selected automatically; omit loom_checker.py:
    "<loom-code>/scripts/loom-python" --repair plan "<path-to-plan.md>"
    "<loom-code>/scripts/loom-python" --ready intake <station> <change-id>
Replace <loom-code> with the installed plugin directory and <path-to-plan.md>
with your plan file path.
Plan takes a file path; intake takes a station and a change-id.
Detailed help: finalize-review --help, publish --help, delivery --help
(each also accepts -h). Only these exact command-plus-help forms are help.
No validation runs for --help or -h alone.

Exit codes: 0 pass (or help displayed), 1 a rule failed (`BLOCK <rule.id>: <reason>` on
stderr), 2 usage or internal error. Any unexpected exception fails
closed as exit 2 -- a checker that cannot decide never says "fine".

Schemas are not restated here: the required frontmatter fields, sections,
station names, interface-surface defaults and artifact paths are read
from `loom-code/contract/manifest.yaml`, which is the versioned contract
package this checker ships with.
"""
from __future__ import annotations

import sys

from loom_checker.command_handlers.charter import cmd_charter
from loom_checker.command_handlers.contract import cmd_contract
from loom_checker.command_handlers.finalize import cmd_finalize_review
from loom_checker.command_handlers.github_rules import cmd_github_rules
from loom_checker.command_handlers.intake import cmd_intake
from loom_checker.command_handlers.intent import cmd_intent
from loom_checker.command_handlers.intents import cmd_intents
from loom_checker.command_handlers.land import cmd_land
from loom_checker.command_handlers.plan import cmd_plan
from loom_checker.command_handlers.publish import cmd_publish
from loom_checker.command_handlers.publish import cmd_delivery
from loom_checker.command_handlers.pr_floor import cmd_pr_floor
from loom_checker.command_handlers.push import cmd_push
from loom_checker.command_handlers.reviewer_count import cmd_reviewer_count
from loom_checker.command_handlers.standing import cmd_standing
from loom_checker.command_handlers.sync import cmd_sync_trunk
from loom_checker.helpers import UsageError
from loom_checker.rules import list_rules


USAGE = __doc__.split("Sub-commands (the CLI contract other stations depend on):", 1)[1]


COMMAND_HELP = {
    "finalize-review": """finalize-review — verify committed content and generate an attestation
Usage: finalize-review <change-id> --input <review-input.json>
<change-id> identifies the change; it is not a file path. --input names a
readable JSON file (relative to the working directory or absolute). Keep this
temporary input outside the repository so the checkout stays clean.

Run inside the selected repository after committing functional content, intent,
plan, required acceptance report and adversarial programs. Resolve the trunk
used for the branch diff. Review the current HEAD's content; the diff base is
the comparison starting point, not the reviewed target. Compute the required
reviewer count with reviewer-count <change-id>; use distinct real reviewers
independent of the writer. Preserve each original verdict and its findings;
never invent identities, passing judgments, probe evidence or authorization.

Illustrative JSON shape only — replace placeholders with authentic output;
this is not ready-to-submit review evidence:
{
  "verdicts": [{
    "reviewer": "<actual reviewer id>", "vendor": "<actual vendor>",
    "model": "<actual model>", "lens": "<actual review lens>",
    "verdict": "<original verdict>", "findings": []
  }],
  "findings": [],
  "adversarial": [{"command": "<artifact-bound execution command>",
                   "artifact": "<committed repository-relative program path>"}]
}
Repeat verdict rows for the required reviewers. Empty findings arrays are
appropriate only when the source has none; top-level findings carry every
unresolved adversarial finding from Build. Finalization accepts only PASS or
PASS_WITH_NOTES verdicts; a failing judgment requires the normal fix/review
route, not relabelling. Preserve scores and notes from the actual review too.
For a selected outside reviewer, retain its complete external_review runner
result, dimension_scores, notes and reviewed_sha; review_target_sha is the
concrete HEAD supplied to that review, not the diff base. The raw review output
must match the attributed verdict. Do not manufacture a receipt.

Use the actual committed probe and supported runner command from Build's
handoff. Where required, copy the reviewer's probe confirmation as
"confirmation": {"reviewer": "<id>", "reviewed_sha": "<reviewed commit>",
                 "quote": "<whole output lines naming this probe>"}.
If the adversary actually recorded no program, replace the adversarial list
with [{"no_program": "<observed reason>"}]; never mix it with program rows.
The reason must be nonblank, single-line, trimmed and contain no HTML comment.
This observed outcome is not a bypass. Follow existing explicit skip
instructions: when reviewers, adversarial or package-tests were skipped by
instruction, skip finalization and disclose absent verification. The checker
still recomputes any automatic narrow-change simplification.
Complete outside-review receipt and probe rules: <loom-code>/skills/closing-review/SKILL.md.

Results: exit 0 announces the generated attestation; exit 1 reports a BLOCK
rule and reason; exit 2 reports invocation/internal errors. Correct malformed
JSON or missing inputs using the diagnostic; obtain missing authentic evidence
through the normal review workflow. A passed stage is not overall success.
Stderr progress is advisory and can also contain errors: while running, keep
observing the same process; inspect its final exit and generated evidence.
""",
    "publish": """publish — publish an authorized branch and observe required CI
Usage: publish --intent <absolute-intent-path> --title <text> --body-file <absolute-body-path>
Legacy: publish --confirm-authorized --title <text> --body-file <absolute-body-path>

Publication may perform a remote write (push and create/update a Ready PR).
--intent must name this change's canonical, committed, confirmed intent with
an existing valid automatic-publication authorization that remains unrevoked.
The legacy --confirm-authorized argument records an actual explicit user
publication decision; it is not a way to supply missing consent. If neither
authorization exists, stop and obtain that decision. Help grants no authority.
Observation grants neither publication nor merge authorization.

--title needs non-empty text; keep the existing branch/title policy.
--body-file must be an absolute path to a readable UTF-8 Markdown file.
Prepare the body from the confirmed intent, current diff, review and actual
verification evidence. Include each of these nine headings exactly once,
with substantive content (Follow-ups may say None):
## Context
## Intended outcome
## Scope
## Decisions
## Implementation
## Behaviour change
## Verification
## Risks and rollback
## Follow-ups

Under Verification include Verification status: <computed status>.
The checker reports valid, absent or stale (<reason>); if refused, copy the
reported corrected Verification status: line into the body without inventing
a stronger status. Disclose actual instructed skips and missing evidence.
When recorded, include Adversarial outcome: no program — <recorded reason>.
Detailed body, skipped-step and risk requirements: <loom-code>/skills/ship/SKILL.md.
Existing body snapshots, origin/HEAD reconciliation and branch/title checks
still apply. Correct the named input or condition, preserving work.

Results: exit 0 completes publication and its required-check observation;
exit 1 means blocked or unconfirmed; exit 2 means invocation or authorization
errors, or internal failures. Read the diagnostic to determine the next action;
the exit code alone is not a reason to retry.
Verification output or a PR URL alone is not completion. Stderr progress is
advisory and can also contain errors; while CI is pending keep observing the
same process. Inspect the final exit and evidence. Exit 0 with
"No required checks registered" means no checks registered, not tests passed.
An observation failure may follow a successful remote write. Before considering
another publish, run delivery --goal published --json to observe existing
state and follow its diagnostic; do not blindly repeat a write or switch routes.
""",
    "delivery": """delivery — observe the selected delivery goal without writes
Usage: delivery [--goal local|published|merged] [--intent <path>] [--json]
Run inside the selected repository on its identified feature branch.
--goal defaults to published. local checks that attributable paths are committed;
it does not check finalization, attestation or verification. published checks the
matching Ready PR and required CI; merged checks merged delivery evidence.
--intent optionally identifies the change's canonical committed intent (a
relative or absolute path); it does not create or grant authorization.
Local observation does not claim publication. Observation never authorizes
publication or merge, and does not perform either action.

--json emits the existing object on stdout:
state: observed delivery condition; reason: why it was classified that way;
next: suggested next action, subject to existing authorization;
evidence: observations supporting the result; complete: whether the goal is met.
A JSON object by itself, especially complete: false, is not proof of delivery.
Use state, reason, next and evidence together with the process exit status.
Exit 0 means the selected goal was achieved; exit 1 means incomplete or
unconfirmed; exit 2 means invocation/internal error. Pending means wait and
observe again; blocked means resolve the stated condition; unconfirmed means
evidence is unavailable, not success. Correct invocation errors using the
diagnostic. Re-observation grants no permission to retry a remote write.
Stderr progress is advisory and can also contain errors; inspect final results.
More workflow guidance: <loom-code>/skills/ship/SKILL.md.
""",
}

HELP_NOTICE = """
No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
"""


COMMANDS = {
    "intent": cmd_intent,
    "intents": cmd_intents,
    "intake": cmd_intake,
    "push": cmd_push,
    "publish": cmd_publish,
    "delivery": cmd_delivery,
    "land": cmd_land,
    "sync-trunk": cmd_sync_trunk,
    "github-rules": cmd_github_rules,
    "pr-floor": cmd_pr_floor,
    "standing": cmd_standing,
    "contract": cmd_contract,
    "charter": cmd_charter,
    "plan": cmd_plan,
    "reviewer-count": cmd_reviewer_count,
    "finalize-review": cmd_finalize_review,
}


def main(argv: list[str], out=sys.stdout, err=sys.stderr) -> int:
    hint = ""
    if argv and argv[0] in COMMAND_HELP and not (argv[0] == "delivery" and "--hook" in argv[1:]):
        hint = (f'Help: "<loom-code>/scripts/loom-python" --ready {argv[0]} --help '
                '(replace <loom-code> with the installed loom-code plugin directory).\n')
    try:
        if not argv:
            raise UsageError("no sub-command given." + USAGE)
        if argv in (["--help"], ["-h"]):
            out.write(USAGE)
            return 0
        if len(argv) == 2 and argv[0] in COMMAND_HELP and argv[1] in {"--help", "-h"}:
            out.write(COMMAND_HELP[argv[0]] + HELP_NOTICE)
            return 0
        if argv[0] == "--list-rules":
            return list_rules(out)
        command = COMMANDS.get(argv[0])
        if command is None:
            raise UsageError(f"unknown sub-command {argv[0]!r}." + USAGE)
        result = command(argv[1:], out, err)
        if result != 0 and hint:
            err.write(hint)
        return result
    except UsageError as exc:
        err.write(f"{exc}\n")
        if hint:
            err.write(hint)
        return 2
    except Exception as exc:
        if argv[:2] == ["push", "--hook"]:  # the publication hook never refuses on a crash (REQ-4)
            err.write(f"loom: publication hook failed ({type(exc).__name__}: {exc}); allowing.\n")
            return 0
        err.write(f"loom_checker internal error: {type(exc).__name__}: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
