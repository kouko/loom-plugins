# Independent fresh-reader observations

Target: a689bd1547306d1788888169b06f0dc429782931.
Clean clone: /private/tmp/loom-scope-acceptance-20261111-a689.
Reader: independent acceptance-tester agent, not an implementer.

## First execution: unprompted-case.md

Recorded before opening the six-case fixture or prior baseline results.
I applied the changed Skill lens to the entire supplied target and its
project instructions, Acceptance, and reference manual.

Raw result: PASS; findings: [].

Omission: none. The request, command, and reporting action are supplied.
Ambiguity: none affecting execution. Inconsistency: none. Incorrect fact:
none; `quill version` matches the supplied manual. Missing population:
not applicable; there is no measurement. User-judgment-leak: none; the
executor is not asked to defer a settled technical choice. Deletion-first:
no added mechanism to remove. No governing gate-registration contract is
present; absence of a Loom marker or registry is not a defect.

This is actual execution of prose review instructions by a fresh reader,
not a CLI invocation, runtime benchmark, or independent tool-manual check.

## Six supplied cases: actual review results

These results were recorded before reading either baseline result file.

- `external-clean`: PASS; findings []. The ordinary-prose contract imposes
  no gate requirement; command and reporting action satisfy Acceptance.
- `workflow-only-adoption`: PASS; findings []. Using the workflow does not
  change the supplied target contract; no marker or registration requested.
- `governed-missing-marker`: PASS_WITH_NOTES; omission, important, anchored
  at `release-helper/SKILL.md` sentence `Before publication, run...`.
  The explicitly adopted contract requires its registered marker, which is
  absent. Fix: enclose the blocking rule in `release.clean-tree` gate markers.
- `governed-marked`: PASS; findings []. The supplied registry and checker
  already cover the marked blocking rule; no extra mechanism is necessary.
- `real-command-error`: NEEDS_REVISION; incorrect-fact, fatal, anchored at
  `quill-guide/SKILL.md` command `quill --version`. The supplied manual says
  it fails rather than displaying the version. Fix: use `quill version`.
- `correct-command`: PASS; findings []. The command matches the reference
  and the instruction reports the requested result.

## Independent bounded extensions: inputs and actual outputs

### test_release_registry_missing_reports_omission

Input: use `governed-marked` unchanged except its project contract now says
the registry is empty and no checker implements `release.clean-tree`.
The contract still requires registration and recomputation for blocking
rules, and Acceptance still requires the marked dirty-tree publication block.

Output: NEEDS_REVISION. Omission, fatal, anchored at the
`release.clean-tree` marker and the supplied empty registry: the purported
gate has no recomputation, losing the promised enforcement guarantee.
Fix: register `release.clean-tree` and implement its specified dirty-tree
check. The marker alone does not satisfy the adopted contract.

### test_governed_command_invalid_reports_usage_error

Input: the `real-command-error` reference manual and target, enclosed in
`<!-- gate: quill.version -->` and `<!-- /gate -->`. Project contract:
explicitly adopts Loom registration; `quill.version` is registered and its
checker verifies the version-report instruction exists. Acceptance remains
displaying the installed version. Registration does not certify command validity.

Output: NEEDS_REVISION. Incorrect-fact, fatal, anchored at
`quill-guide/SKILL.md` command `quill --version`. It is unsupported even
though the gate is registered. Fix: change it to `quill version`.

### test_external_acceptance_unmet_reports_omission

Input: `external-clean` project contract and manual. Acceptance additionally
requires explaining how to locate Quill's configuration. Supplied manual:
`quill config path` prints that location. Target remains exactly the
version-only skill in `external-clean`.

Output: NEEDS_REVISION. Omission, fatal, anchored at the complete target's
version-only instruction and the configuration-location Acceptance clause.
The requested capability is absent. Fix: add the instruction to run
`quill config path` and report its output when that location is requested.
No Loom registration mechanism is requested.

### test_governed_acceptance_unmet_reports_omission

Input: `governed-marked` unchanged, except Acceptance also requires stopping
publication when tests fail. Contract registers both `release.clean-tree`
and `release.tests-pass`, and their recomputation. The supplied test command
is `project-test`; a nonzero exit means failure. The target still contains
only its correctly marked dirty-tree rule.

Output: NEEDS_REVISION. Omission, fatal, anchored at the target's sole
dirty-tree block versus the failing-tests Acceptance clause. Registration
and one valid gate do not implement the second required release check.
Fix: add the registered `release.tests-pass` block that runs `project-test`
and stops publication on nonzero exit.

These are ten case executions plus the first unprompted execution, all by
one independent reader. They do not estimate repeatability or model-wide
failure frequency. Synthetic reference manuals are ground truth, not claims
about an installed executable.
