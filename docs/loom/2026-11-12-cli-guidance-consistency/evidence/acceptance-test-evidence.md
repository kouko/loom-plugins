# CLI guidance consistency — acceptance test evidence

Canonical final tested commit: c2bab0811a1ba1083e2452d84375d9c02c79bc3a. The initial run below is retained; the final re-run section records the corrected spec and all repeated cases.

Tried on 2026-11-12, in a clean copy of the project at 159af54d7f11f92bdecba9e9d93fb515f1bc317c.

## Setup and scope
Fresh local clone: `git clone --no-hardlinks /private/tmp/loom-cli-guidance-consistency /private/tmp/loom-guidance-independent-acceptance`. Initial tree clean. Read README CLI conventions and invoked the candidate's bundled `loom-code/scripts/loom-python --ready`, rather than installed 3.69.0. No external host installation, automatic routing, paid service, remote write or efficiency benchmark was performed. Commands were independently derived from help and genuine retained intent/spec/plan artifacts. Controlled negative edits were confined to the disposable clone and restored before recovery. No implementation was repaired.

## 1. Consistent discovery and usable instructions
Exact long and short help were tried outside git for all three commands. Genuine canonical plan check, both intake stations and reviewer floor all returned exit 0 with the documented output. Help is explicitly limited; passing the named check is not approval or completed verification.

## 2. Recoverable errors and truthful blocked outcomes
Missing operands, unavailable plan, invalid station/change identifier/extra operand, absent intent and all nonexact help shapes were refused. A controlled missing Simplicity record produced plan exit 1; the same defect in the genuine plan produced intake exit 1 while retaining the advisory stdout line. After restoring the record, all three normal calls passed. Dirty-tree reviewer refusal returned exit 2; removing only the tester's controlled changes recovered to floor 2.

Nit: the spec's Repository/internal failure row conflates caller repository misuse with internal exceptions. Outside git, reviewer-count actually exits 2 with a help hint. The caller can correct this, so the runtime is useful; correct the spec to distinguish this UsageError from internal exceptions. Reported to orchestrator. A historical product intent was additionally refused as already delivered, with no stdout; this was not misreported as successful intake.

## 3. Compatibility, streams and verification
Normal plan stdout/stderr remained empty; genuine intake retained its advisory line byte-for-byte before both pass and late BLOCK; reviewer floor was `2\n`. Controlled diagnostics and exit statuses were as recorded below. The focused regression module additionally tests direct-handler/dispatcher stream equivalence, help not dispatching handlers, and internal-error hint exclusion.

Focused test command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py -q` in the clean clone, using existing host cache after sandbox escalation. Result: `39 passed in 7.14s`, exit 0.

Preserved setup failures: initial canonical uv invocation exit 2: `Could not acquire lock ... Operation not permitted ... /Users/kouko/.cache/uv/.tmpoHD9Lk`. A temporary offline cache retry exited 1 because execnet==2.1.2 was absent. System `python3 -m pytest ...` exited 1: `No module named pytest`. The canonical command succeeded with existing-cache access; no packages were installed into the base environment.

The full automated test suite runs before the change is accepted and blocks it on failure; it remains the formal finalize-review check, not an acceptance result claimed here. Command reserved for finalization: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. I did not run the full suite or finalize-review.

## Raw captured calls
Each JSON record preserves actual argv, working directory, exit status and separate stdout/stderr. The temporary negative plan contained `charter: 1.1\n`; the canonical negative plan replaced its Simplicity section with a deliberately missing-record heading. Both were restored using apply_patch before recovery.

```json
[
  {
    "name": "plan-normal",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "docs/loom/2026-11-12-cli-guidance-consistency/plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "name": "intake-spec",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-spec",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "intake-plan",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "reviewer-normal",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "2\n",
    "stderr": ""
  },
  {
    "name": "plan-missing",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "/private/tmp/nonexistent-guidance-plan"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "no such plan file: /private/tmp/nonexistent-guidance-plan\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-empty-args",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "plan needs a path.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-empty",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "intake needs a station and a change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-unknown",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "unknown",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station 'unknown'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-bad-id",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "bad/id"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "'bad/id' is not a change-id; expected [A-Za-z0-9._-]+ (the id is spliced into a path, so nothing else is accepted).\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-extra",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument 'extra'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-absent",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "absent-guidance-change"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 1,
    "stdout": "",
    "stderr": "BLOCK intake.confirmed: no intent file at docs/loom/intent/absent-guidance-change.md.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-empty",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan--help",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "--help"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "plan — check the implemented field caps on one named file\nUsage: plan <path-to-plan.md>\nSupply a readable file path, relative to the working directory or absolute;\nthis command does not resolve a change-id or select a canonical plan.\n\nThe check applies field caps only when the file has a charter: frontmatter\nkey. Charter 1.1 or later also requires a valid Simplicity check record.\nA file without that key, including an empty file, may pass. Passing does not\napprove the plan, prove its requirements are complete or verify the change.\n\nResults: exit 0 has no success payload on stdout; the implemented checks on\nthe named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;\ncorrect the reported field and rerun. Exit 2 means a missing/unreadable file,\ninvalid invocation or internal failure; correct the path, access or invocation\nfrom the diagnostic. No artifact is rewritten and no later station runs.\nPlanning guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "plan-h",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "-h"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "plan — check the implemented field caps on one named file\nUsage: plan <path-to-plan.md>\nSupply a readable file path, relative to the working directory or absolute;\nthis command does not resolve a change-id or select a canonical plan.\n\nThe check applies field caps only when the file has a charter: frontmatter\nkey. Charter 1.1 or later also requires a valid Simplicity check record.\nA file without that key, including an empty file, may pass. Passing does not\napprove the plan, prove its requirements are complete or verify the change.\n\nResults: exit 0 has no success payload on stdout; the implemented checks on\nthe named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;\ncorrect the reported field and rerun. Exit 2 means a missing/unreadable file,\ninvalid invocation or internal failure; correct the path, access or invocation\nfrom the diagnostic. No artifact is rewritten and no later station runs.\nPlanning guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "plan-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "--help",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument 'extra'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "extra",
      "--help"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument '--help'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "-h",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument 'extra'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake--help",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "--help"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "intake — check the selected station's current prerequisites\nUsage: intake <write-spec|write-plan> <change-id>\nRun inside the selected repository. Supply a change-id, not a file path;\naccepted identifiers contain only letters, digits, dots, underscores and\nhyphens. Canonical artifacts are resolved through the bundled contract.\n\nResults: exit 0 means the applicable prerequisites passed for this snapshot;\nit does not perform the station, authorize publication or verify the change.\nConditional interface-surfaces (...) information may appear on stdout for\nengineering intents or applicable needs-design=yes write-plan intake.\nThat information is advisory and may precede a later BLOCK; it is not a\nsuccess result. Other intake paths have no stdout payload.\n\nExit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic\nrequired artifacts through their owning workflow, then rerun. Exit 2 means\ninvalid station/change-id/arguments or an internal failure; correct the\ninvocation or repository/environment from the diagnostic. These checks are\nread-only and synchronous; no previous pass waives the next check.\nStation and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "intake-h",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "-h"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "intake — check the selected station's current prerequisites\nUsage: intake <write-spec|write-plan> <change-id>\nRun inside the selected repository. Supply a change-id, not a file path;\naccepted identifiers contain only letters, digits, dots, underscores and\nhyphens. Canonical artifacts are resolved through the bundled contract.\n\nResults: exit 0 means the applicable prerequisites passed for this snapshot;\nit does not perform the station, authorize publication or verify the change.\nConditional interface-surfaces (...) information may appear on stdout for\nengineering intents or applicable needs-design=yes write-plan intake.\nThat information is advisory and may precede a later BLOCK; it is not a\nsuccess result. Other intake paths have no stdout payload.\n\nExit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic\nrequired artifacts through their owning workflow, then rerun. Exit 2 means\ninvalid station/change-id/arguments or an internal failure; correct the\ninvocation or repository/environment from the diagnostic. These checks are\nread-only and synchronous; no previous pass waives the next check.\nStation and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "intake-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "--help",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station '--help'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "extra",
      "--help"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station 'extra'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "-h",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station '-h'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-count--help",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "--help"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "reviewer-count — compute the required independent reviewer floor\nUsage: reviewer-count <change-id>\nRun inside the selected repository with a clean tree and committed functional\ncontent. Supply one nonblank change-id operand. Preserve work and finish and\ncommit the change before requesting the floor; do not discard files to pass.\n\nResults: exit 0 prints the integer floor and newline on stdout. Obtain that\nmany independent reviewers; the number is not a verdict or proof of review,\nacceptance, finalization or completed verification. The policy conservatively\nrequires two when it cannot classify the complete committed delta.\nExit 2 means missing/extra operands, a dirty tree or an internal failure;\nuse the diagnostic to correct the invocation or repository condition, then\nrerun. This read-only command neither dispatches reviewers nor writes evidence.\nReview guidance: <loom-code>/skills/closing-review/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "reviewer-count-h",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "-h"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "reviewer-count — compute the required independent reviewer floor\nUsage: reviewer-count <change-id>\nRun inside the selected repository with a clean tree and committed functional\ncontent. Supply one nonblank change-id operand. Preserve work and finish and\ncommit the change before requesting the floor; do not discard files to pass.\n\nResults: exit 0 prints the integer floor and newline on stdout. Obtain that\nmany independent reviewers; the number is not a verdict or proof of review,\nacceptance, finalization or completed verification. The policy conservatively\nrequires two when it cannot classify the complete committed delta.\nExit 2 means missing/extra operands, a dirty tree or an internal failure;\nuse the diagnostic to correct the invocation or repository condition, then\nrerun. This read-only command neither dispatches reviewers nor writes evidence.\nReview guidance: <loom-code>/skills/closing-review/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "reviewer-count-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "--help",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-count-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "extra",
      "--help"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-count-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "-h",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-blocked",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "acceptance-invalid-plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 1,
    "stdout": "",
    "stderr": "BLOCK plan.field-caps: Simplicity check section missing or empty (charter 1.1)\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-late-block",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 1,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": "BLOCK plan.field-caps: Simplicity check section missing or empty (charter 1.1)\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-dirty",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs a clean tree with completed functional content.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-outside",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp",
    "exit": 2,
    "stdout": "",
    "stderr": "/private/tmp is not inside a git work tree.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "docs/loom/2026-11-12-cli-guidance-consistency/plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "name": "intake-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "reviewer-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "2\n",
    "stderr": ""
  }
]
```

## Re-run on 2026-11-12, at c2bab0811a1ba1083e2452d84375d9c02c79bc3a

This is the canonical tested commit for the report. Fetched that exact commit into the disposable clone and checked it out detached, starting clean. Reviewed `git diff 159af54d7f11f92bdecba9e9d93fb515f1bc317c HEAD`: only spec error-class wording and its plan pin/task changed (two files); no runtime or test implementation changed. The initial nit is resolved: the spec now separately describes outside-repository UsageError plus help hint and unexpected internal exception without hint.

- 1: re-tested — all three long/short help forms outside git and genuine plan, both intake stations and reviewer floor.
- 2: re-tested — invalid invocation, missing artifacts, controlled plan/intake late BLOCK, dirty repository, outside-repository diagnostic and recovery across all three commands. Repeated all 34 earlier captured cases, then repeated the three recovery calls after removing only tester changes.
- 3: re-tested — genuine output/status/conditional advisory stdout and refusal cases; focused canonical uv test module returned `39 passed in 11.71s`, exit 0. Its internal-error injection coverage passed. Full suite/finalization remains reserved as described above.

```json
[
  {
    "name": "plan-normal",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "docs/loom/2026-11-12-cli-guidance-consistency/plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "name": "intake-spec",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-spec",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "intake-plan",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "reviewer-normal",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "2\n",
    "stderr": ""
  },
  {
    "name": "plan-missing",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "/private/tmp/nonexistent-guidance-plan"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "no such plan file: /private/tmp/nonexistent-guidance-plan\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-empty-args",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "plan needs a path.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-empty",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "intake needs a station and a change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-unknown",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "unknown",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station 'unknown'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-bad-id",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "bad/id"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "'bad/id' is not a change-id; expected [A-Za-z0-9._-]+ (the id is spliced into a path, so nothing else is accepted).\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-extra",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument 'extra'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-absent",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "absent-guidance-change"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 1,
    "stdout": "",
    "stderr": "BLOCK intake.confirmed: no intent file at docs/loom/intent/absent-guidance-change.md.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-empty",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan--help",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "--help"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "plan — check the implemented field caps on one named file\nUsage: plan <path-to-plan.md>\nSupply a readable file path, relative to the working directory or absolute;\nthis command does not resolve a change-id or select a canonical plan.\n\nThe check applies field caps only when the file has a charter: frontmatter\nkey. Charter 1.1 or later also requires a valid Simplicity check record.\nA file without that key, including an empty file, may pass. Passing does not\napprove the plan, prove its requirements are complete or verify the change.\n\nResults: exit 0 has no success payload on stdout; the implemented checks on\nthe named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;\ncorrect the reported field and rerun. Exit 2 means a missing/unreadable file,\ninvalid invocation or internal failure; correct the path, access or invocation\nfrom the diagnostic. No artifact is rewritten and no later station runs.\nPlanning guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "plan-h",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "-h"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "plan — check the implemented field caps on one named file\nUsage: plan <path-to-plan.md>\nSupply a readable file path, relative to the working directory or absolute;\nthis command does not resolve a change-id or select a canonical plan.\n\nThe check applies field caps only when the file has a charter: frontmatter\nkey. Charter 1.1 or later also requires a valid Simplicity check record.\nA file without that key, including an empty file, may pass. Passing does not\napprove the plan, prove its requirements are complete or verify the change.\n\nResults: exit 0 has no success payload on stdout; the implemented checks on\nthe named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;\ncorrect the reported field and rerun. Exit 2 means a missing/unreadable file,\ninvalid invocation or internal failure; correct the path, access or invocation\nfrom the diagnostic. No artifact is rewritten and no later station runs.\nPlanning guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "plan-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "--help",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument 'extra'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "extra",
      "--help"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument '--help'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "-h",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unexpected argument 'extra'.\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake--help",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "--help"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "intake — check the selected station's current prerequisites\nUsage: intake <write-spec|write-plan> <change-id>\nRun inside the selected repository. Supply a change-id, not a file path;\naccepted identifiers contain only letters, digits, dots, underscores and\nhyphens. Canonical artifacts are resolved through the bundled contract.\n\nResults: exit 0 means the applicable prerequisites passed for this snapshot;\nit does not perform the station, authorize publication or verify the change.\nConditional interface-surfaces (...) information may appear on stdout for\nengineering intents or applicable needs-design=yes write-plan intake.\nThat information is advisory and may precede a later BLOCK; it is not a\nsuccess result. Other intake paths have no stdout payload.\n\nExit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic\nrequired artifacts through their owning workflow, then rerun. Exit 2 means\ninvalid station/change-id/arguments or an internal failure; correct the\ninvocation or repository/environment from the diagnostic. These checks are\nread-only and synchronous; no previous pass waives the next check.\nStation and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "intake-h",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "-h"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "intake — check the selected station's current prerequisites\nUsage: intake <write-spec|write-plan> <change-id>\nRun inside the selected repository. Supply a change-id, not a file path;\naccepted identifiers contain only letters, digits, dots, underscores and\nhyphens. Canonical artifacts are resolved through the bundled contract.\n\nResults: exit 0 means the applicable prerequisites passed for this snapshot;\nit does not perform the station, authorize publication or verify the change.\nConditional interface-surfaces (...) information may appear on stdout for\nengineering intents or applicable needs-design=yes write-plan intake.\nThat information is advisory and may precede a later BLOCK; it is not a\nsuccess result. Other intake paths have no stdout payload.\n\nExit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic\nrequired artifacts through their owning workflow, then rerun. Exit 2 means\ninvalid station/change-id/arguments or an internal failure; correct the\ninvocation or repository/environment from the diagnostic. These checks are\nread-only and synchronous; no previous pass waives the next check.\nStation and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "intake-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "--help",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station '--help'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "extra",
      "--help"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station 'extra'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "-h",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "unknown station '-h'; intake covers write-spec and write-plan.\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-count--help",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "--help"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "reviewer-count — compute the required independent reviewer floor\nUsage: reviewer-count <change-id>\nRun inside the selected repository with a clean tree and committed functional\ncontent. Supply one nonblank change-id operand. Preserve work and finish and\ncommit the change before requesting the floor; do not discard files to pass.\n\nResults: exit 0 prints the integer floor and newline on stdout. Obtain that\nmany independent reviewers; the number is not a verdict or proof of review,\nacceptance, finalization or completed verification. The policy conservatively\nrequires two when it cannot classify the complete committed delta.\nExit 2 means missing/extra operands, a dirty tree or an internal failure;\nuse the diagnostic to correct the invocation or repository condition, then\nrerun. This read-only command neither dispatches reviewers nor writes evidence.\nReview guidance: <loom-code>/skills/closing-review/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "reviewer-count-h",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "-h"
    ],
    "cwd": "/private/tmp",
    "exit": 0,
    "stdout": "reviewer-count — compute the required independent reviewer floor\nUsage: reviewer-count <change-id>\nRun inside the selected repository with a clean tree and committed functional\ncontent. Supply one nonblank change-id operand. Preserve work and finish and\ncommit the change before requesting the floor; do not discard files to pass.\n\nResults: exit 0 prints the integer floor and newline on stdout. Obtain that\nmany independent reviewers; the number is not a verdict or proof of review,\nacceptance, finalization or completed verification. The policy conservatively\nrequires two when it cannot classify the complete committed delta.\nExit 2 means missing/extra operands, a dirty tree or an internal failure;\nuse the diagnostic to correct the invocation or repository condition, then\nrerun. This read-only command neither dispatches reviewers nor writes evidence.\nReview guidance: <loom-code>/skills/closing-review/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n",
    "stderr": ""
  },
  {
    "name": "reviewer-count-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "--help",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-count-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "extra",
      "--help"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-count-nonexact",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "-h",
      "extra"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-outside",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp",
    "exit": 2,
    "stdout": "",
    "stderr": "/private/tmp is not inside a git work tree.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "docs/loom/2026-11-12-cli-guidance-consistency/plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "name": "intake-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "reviewer-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "2\n",
    "stderr": ""
  },
  {
    "name": "plan-blocked",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "acceptance-invalid-plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 1,
    "stdout": "",
    "stderr": "BLOCK plan.field-caps: Simplicity check section missing or empty (charter 1.1)\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "intake-late-block",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 1,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": "BLOCK plan.field-caps: Simplicity check section missing or empty (charter 1.1)\nHelp: \"<loom-code>/scripts/loom-python\" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "reviewer-dirty",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 2,
    "stdout": "",
    "stderr": "reviewer-count needs a clean tree with completed functional content.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
  },
  {
    "name": "plan-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "plan",
      "docs/loom/2026-11-12-cli-guidance-consistency/plan.md"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "name": "intake-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "intake",
      "write-plan",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)\n",
    "stderr": ""
  },
  {
    "name": "reviewer-recovery",
    "command": [
      "/private/tmp/loom-guidance-independent-acceptance/loom-code/scripts/loom-python",
      "--ready",
      "reviewer-count",
      "2026-11-12-cli-guidance-consistency"
    ],
    "cwd": "/private/tmp/loom-guidance-independent-acceptance",
    "exit": 0,
    "stdout": "2\n",
    "stderr": ""
  }
]
```


