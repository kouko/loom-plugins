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
    loom_checker.py intake <station> <change-id> [--json]
    loom_checker.py push --hook
    loom_checker.py push --install-git-hooks
    loom_checker.py push --remove-git-hooks
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
    loom_checker.py plan <path-to-plan.md> [--json]

With the launcher, the checker is selected automatically; omit loom_checker.py:
    "<loom-code>/scripts/loom-python" --repair plan "<path-to-plan.md>"
    "<loom-code>/scripts/loom-python" --ready intake <station> <change-id>
Replace <loom-code> with the installed plugin directory and <path-to-plan.md>
with your plan file path.
Plan takes a file path; intake takes a station and a change-id.
Plan and intake accept an optional final --json selector; text remains default.
Detailed help: finalize-review --help, publish --help, delivery --help
              plan --help, intake --help, reviewer-count --help
              intent --help, intents --help, push --help, land --help
              sync-trunk --help, github-rules --help, pr-floor --help
              standing --help, contract --help, charter --help
Every listed sub-command supports <command> --help or <command> -h.
Only exact command-plus-help forms are help.
No validation runs for --help or -h alone.

Exit codes depend on the command: 0 may include advisory or unsynced results;
1 means a failed check or incomplete operation; 2 means usage/internal error
or a hook refusal. See each command's help for its completion limits.
The publication hook allows on unexpected exceptions; other commands exit 2.

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
from loom_checker.preparation_output import new_result, error_result, write_result
from loom_checker.rules import list_rules


USAGE = __doc__.split("Sub-commands (the CLI contract other stations depend on):", 1)[1]


PREPARATION_JSON_HELP = """Optional JSON: append --json as the final argument only. Exact --help/-h
remains text; help combined with --json is checked as an ordinary invocation.
Duplicate selectors are usage errors. Earlier --json tokens without a final
selector retain their existing operand meaning; ./--json names a literal file.

JSON stdout is one object plus newline; checker stderr is empty. Fields:
schema_version: 1; command: plan|intake; status: passed|blocked|error;
diagnostics: ordered [{rule_id, message}]; notices: ordered strings;
error: null or {kind: usage|internal, message}. Empty arrays are [], not null.
Exit 0 means passed, 1 blocked, 2 error. Blocked includes rule diagnostics;
error has empty diagnostics. Notices may precede a blocker or internal error
and never imply success. Status covers only this invocation's checks, not
workflow completion or authority. Do not depend on key order or message prose.
Launcher/startup failures, termination and broken pipes are outside this
in-process result guarantee. Read the actual process result; do not retry
automatically. Without --json, existing text streams and exits are unchanged.
"""


COMMAND_HELP = {
    "intent": """intent — check one intent's implemented rules
Usage: intent <path> [--commit-msg <file>]
Supply readable relative-to-working-directory or absolute paths. Repository
context is resolved from the intent; the bundled manifest defines its schema.
--commit-msg supplies design-reasoning evidence; it does not create a commit.
Checks cover schema, map existence, product identifiers, design reasoning and
applicable touched-interface/kind rules. Advisory stdout may precede a blocker;
success may have empty stdout. Exit 0 means these checks passed, Exit 1 reports
BLOCK diagnostics on stderr, Exit 2 means arguments, files or internal failure.
Reads only; it neither creates nor confirms intent or authorizes delivery.
Correct the reported source artifact or path through its owning workflow and retry.
""",
    "intents": """intents — inspect locally derived intent delivery states
Usage: intents [<change-id>] [--remote <name>] [--metadata]
Run in the repository. The remote defaults to origin and must be a safe literal.
Identifiers contain letters, digits, dots, underscores and hyphens; a selected
ID needs its canonical intent file. --metadata requires one ID.
Without an ID, lists active/indeterminate confirmed intents and may print nothing.
With an ID, reports its state. Tab-separated stdout contains ID/state/detail;
delivered metadata can add commit, pr and committed_at (committer, not merge date).
Exit 0 is a local-ref observation, not live freshness proof. Indeterminate gives
exit 1 and refresh advice; Exit 2 means invocation or internal error on stderr.
Reads local Git only, never fetches. Refresh the selected remote-default ref
explicitly when needed, then retry; this does not perform delivery.
""",
    "push": """push — provide host-hook feedback or install native branch protection
Usage: push --hook
       push --install-git-hooks
       push --remove-git-hooks
Only --hook reads PreToolUse JSON from stdin; invalid ordinary calls do not.
The hook refuses direct git commit/merge/push on main/master with exit 2
unless repository-local loom.protectMain=false explicitly allows those commands.
This opt-out affects the host hook, not the separate native hooks below.
Malformed/missing payload also exits 2. Publication reminders may emit a host
JSON systemMessage on stdout and a diagnostic on stderr; reminder failures and
unexpected top-level hook exceptions allow exit 0. It performs no publication.

Native modes are explicit repository configuration operations. They read and
refuse a core.hooksPath override or unreadable setting without changing it.
Install validates local and live origin default metadata; it may create the
Git hooks directory and writes three owned hooks: pre-commit, pre-merge-commit,
pre-push. Remove deletes only those owned files. Foreign/edited hooks and
symlinked locations are refused; preserve them and arrange hook-owner integration.
Native success prints installed/removed on stdout, exit 0. Caught failures
print loom: diagnostics on stderr, exit 2, without BLOCK. Inspect origin and
repair default metadata as directed before retry. Native hooks protect main,
master and the origin default branch, but are ordinary Git safeguards, not a
security boundary or proof of remote branch protection. Help grants no consent.
""",
    "land": """land — merge an accepted PR or clean up merged changes
Usage: land --accepted-by <name>
       land --cleanup <branch>
       land --sweep [--confirm <token>]
Choose exactly one form; --confirm applies only to sweep. Run in the repository
with trusted git/gh, eligible change branch/PR and live evidence/checks. A real
maintainer acceptance must already exist; the name or help supplies no consent.
The accepted form may squash merge remotely, verify, sync trunk, then delete
the change worktree and local/remote branch. Cleanup targets a named merged
change. Sweep computes candidates and a confirmation token; even without a
token it fetches/prunes refs. A matching revalidated token enables deletion.
Do not run cleanup when worktree preservation was requested.
Exit 0 can follow successful merge/cleanup even when best-effort trunk sync
was skipped or failed and stdout says "trunk not updated". Read the trunk
result; preserve work before independently resolving local trunk conditions.
Named cleanup never syncs trunk. Sweep listing also returns exit 0. Exit 1 reports
refusal or failed stage with BLOCK stderr, Exit 2 reports usage/internal errors.
Progress/results appear on stdout. Merge can succeed before verification or
cleanup fails: inspect remote merge and preserved work before corrective action;
use cleanup for an already merged change instead of blindly repeating a merge.
Dirty work and divergent local trunk are preserved/refused, not force-discarded.
""",
    "sync-trunk": """sync-trunk — bring a clean change branch onto fetched trunk
Usage: sync-trunk
Run on a clean attached change branch, not trunk, with trusted Git and resolvable
trunk metadata. Preserve and commit work before resolving a dirty-tree refusal.
Fetches origin, then may rebase safe unpublished commits or merge trunk. Refuses
preflight conflicts/collisions; abort/rollback is attempted after mutation failure,
not guaranteed. Results appear on stdout; WARN/BLOCK diagnostics on stderr.
Exit 0 includes fetch WARN with no sync, already-current and completed sync.
Exit 1 means BLOCK review.sync; Exit 2 means arguments/internal error. Read the
warning before assuming synchronization. Resolve origin/network or conflicts
through normal Build and retry. Changed content needs full tests/probes again;
rebased commit identities require updating pinned references before review.
""",
    "github-rules": """github-rules — inspect GitHub trunk protection as advisory information
Usage: github-rules [--print-setup]
Run in the repository with origin metadata and authenticated gh read access.
Uses network reads to report present, absent or unconfirmed rules on stdout.
Exit 0 includes unavailable/unconfirmed protection; it does not prove protection
or verification. Exit 2 means invalid arguments or unexpected internal failure
on stderr. Restore origin, authentication/network and read access, then rerun.
--print-setup prints a setup command when prerequisites permit, without executing
it. It never changes GitHub rules. Running printed setup is a separate mutation
requiring its own authorization; help grants none.
""",
    "pr-floor": """pr-floor — validate a PR body and disclose verification in CI
Usage: pr-floor --body-file <file> --base <sha> --head <sha> [--branch <name>]
Supply unique paired flags, a readable body file (relative to the working
directory or absolute), required base/head Git evidence and optional branch.
Run in the repository. Emits CI error/notice annotations on stdout. Body
structure failures also report BLOCK ci.pr-floor on stderr, exit 1. Exit 0
means the body passed; recomputed verification may still be stale or absent.
Exit 2 means invocation, unreadable file or internal failure. Correct named
headings or Git context; never fabricate stronger verification status.
Can append a verification line to GITHUB_STEP_SUMMARY when set, so it is not
strictly read-only. It runs no PR-controlled commands, tests or reviews and
does not authorize publication or merge.
""",
    "standing": """standing — check applicable standing-document policy for one intent
Usage: standing <path-to-intent>
Supply one readable relative-to-working-directory or absolute intent path;
repository context is resolved from that file. Reads applicable PRINCIPLES.md,
DESIGN.md and root ARCHITECTURE.md plus standing policy records.
Warnings on stderr can coexist with passing checks and empty stdout. Exit 0
means implemented policy checks passed, not semantic certification of documents.
Exit 1 reports BLOCK diagnostics for second-vendor/product-principles policy;
Exit 2 means missing file, invalid arguments or internal failure. Correct the
authentic policy/document record through its owning workflow, then rerun.
Read-only; does not ratify documents or perform review.
""",
    "contract": """contract — check compatibility with the bundled contract manifest
Usage: contract --require <major.minor>
Supply a numeric major.minor requirement. Reads the manifest in effect; a
matching major and sufficiently high minor pass. Exit 0 prints current and
required versions on stdout; Exit 1 reports BLOCK contract.requires on stderr;
Exit 2 means malformed/missing arguments or internal failure. Follow the
diagnostic to update the applicable consuming plugin or loom-code requirement,
then retry. Read-only: this does not check plugin release version, provision
runtime, run station prerequisites or authorize a later operation.
""",
    "charter": """charter — render and validate artifact charter rows
Usage: charter [--manifest <path>]
Defaults to the contract manifest in effect. An override is a readable YAML
path, relative to the working directory or absolute. Repeated --manifest uses
the last path. No repository mutation occurs.
Prints a Markdown table on stdout in manifest artifact order, including an
empty table for missing/empty artifacts. Exit 0 means implemented row checks
passed; Exit 1 reports BLOCK contract.charter-complete on stderr. A table can
coexist with failure and is not an approval. Exit 2 means file, arguments or
internal failure. Correct the reported manifest charter fields and retry.
""",
    "plan": """plan — check the implemented field caps on one named file
Usage: plan <path-to-plan.md> [--json]
Supply a readable file path, relative to the working directory or absolute;
this command does not resolve a change-id or select a canonical plan.

The check applies field caps only when the file has a charter: frontmatter
key. Charter 1.1 or later also requires a valid Simplicity check record.
A file without that key, including an empty file, may pass. Passing does not
approve the plan, prove its requirements are complete or verify the change.

Text results: exit 0 has no success payload on stdout; the implemented checks on
the named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;
correct the reported field and rerun. Exit 2 means a missing/unreadable file,
invalid invocation or internal failure; correct the path, access or invocation
from the diagnostic. No artifact is rewritten and no later station runs.
Planning guidance: <loom-code>/skills/write-plan/SKILL.md.
""",
    "intake": """intake — check the selected station's current prerequisites
Usage: intake <write-spec|write-plan> <change-id> [--json]
Run inside the selected repository. Supply a change-id, not a file path;
accepted identifiers contain only letters, digits, dots, underscores and
hyphens. Canonical artifacts are resolved through the bundled contract.

Text results: exit 0 means the applicable prerequisites passed for this snapshot;
it does not perform the station, authorize publication or verify the change.
Conditional interface-surfaces (...) information may appear on stdout for
engineering intents or applicable needs-design=yes write-plan intake.
That information is advisory and may precede a later BLOCK; it is not a
success result. Other intake paths have no stdout payload.

Exit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic
required artifacts through their owning workflow, then rerun. Exit 2 means
invalid station/change-id/arguments or an internal failure; correct the
invocation or repository/environment from the diagnostic. These checks are
read-only and synchronous; no previous pass waives the next check.
Station and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.
""",
    "reviewer-count": """reviewer-count — compute the required independent reviewer floor
Usage: reviewer-count <change-id>
Run inside the selected repository with a clean tree and committed functional
content. Supply one nonblank change-id operand. Preserve work and finish and
commit the change before requesting the floor; do not discard files to pass.

Results: exit 0 prints the integer floor and newline on stdout. Obtain that
many independent reviewers; the number is not a verdict or proof of review,
acceptance, finalization or completed verification. The policy conservatively
requires two when it cannot classify the complete committed delta.
Exit 2 means missing/extra operands, a dirty tree or an internal failure;
use the diagnostic to correct the invocation or repository condition, then
rerun. This read-only command neither dispatches reviewers nor writes evidence.
Review guidance: <loom-code>/skills/closing-review/SKILL.md.
""",
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
Finalization executes the package suite and declared adversarial commands and
atomically writes the generated attestation. It grants no publication authority.
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
Run with trusted git/gh on a clean committed selected branch. Publication may
write a local body snapshot before the remote operations; rollback is not promised.

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
Hook forms: delivery --hook; delivery --hook --host claude|codex.
Hook mode consumes host stdin and emits host-specific feedback with its own
exit semantics; it is separate from ordinary --json. Do not mix hook forms
with observation options. Duplicate options are invalid. Malformed ordinary
invocations may report text on stderr even when --json was supplied.
""",
}

HELP_NOTICE = """
No validation or publication occurred: help only, exit 0.
Use "<loom-code>/scripts/loom-python" --ready <command> <arguments>.
Replace <loom-code> with the installed loom-code plugin directory; launcher
runtime readiness is still required. Bundled paths above are plugin-relative.
--ready with missing runtime exits 86 without provisioning. --repair may use
network and write runtime caches/locks before checker help; it is not offline.
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
    preparation = new_result(argv[0]) if len(argv) >= 2 and argv[0] in {"plan", "intake"} and argv[-1] == "--json" else None
    if preparation is not None:
        argv = argv[:-1]
    hint = ""
    if argv and argv[0] in {"finalize-review", "publish", "delivery", "plan", "intake", "reviewer-count"} and not (argv[0] == "delivery" and "--hook" in argv[1:]):
        hint = (f'Help: "<loom-code>/scripts/loom-python" --ready {argv[0]} --help '
                '(replace <loom-code> with the installed loom-code plugin directory).\n')
    try:
        if preparation is not None and "--json" in argv[1:]:
            raise UsageError("duplicate --json selector.")
        if not argv:
            raise UsageError("no sub-command given." + USAGE)
        if argv in (["--help"], ["-h"]):
            out.write(USAGE)
            return 0
        if preparation is None and len(argv) == 2 and argv[0] in COMMAND_HELP and argv[1] in {"--help", "-h"}:
            out.write(COMMAND_HELP[argv[0]])
            if argv[0] in {"plan", "intake"}:
                out.write(PREPARATION_JSON_HELP)
            out.write(HELP_NOTICE)
            return 0
        if argv[0] == "--list-rules":
            return list_rules(out)
        command = COMMANDS.get(argv[0])
        if command is None:
            raise UsageError(f"unknown sub-command {argv[0]!r}." + USAGE)
        if preparation is not None:
            result = command(argv[1:], out, err, result=preparation)
            write_result(preparation, out)
            return result
        result = command(argv[1:], out, err)
        if result != 0 and hint:
            err.write(hint)
        return result
    except UsageError as exc:
        if preparation is not None:
            error_result(preparation, "usage", str(exc))
            write_result(preparation, out)
            return 2
        err.write(f"{exc}\n")
        if hint:
            err.write(hint)
        return 2
    except Exception as exc:
        if preparation is not None:
            error_result(preparation, "internal", f"loom_checker internal error: {type(exc).__name__}: {exc}")
            write_result(preparation, out)
            return 2
        if argv[:2] == ["push", "--hook"]:  # the publication hook never refuses on a crash (REQ-4)
            err.write(f"loom: publication hook failed ({type(exc).__name__}: {exc}); allowing.\n")
            return 0
        err.write(f"loom_checker internal error: {type(exc).__name__}: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
