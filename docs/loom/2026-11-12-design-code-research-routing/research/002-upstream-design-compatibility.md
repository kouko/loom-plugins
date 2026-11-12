---
title: "Does the new CLI progress release conflict with research routing?"
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
change: 2026-11-12-design-code-research-routing
tags:
  - loom/research
---

# Upstream design compatibility

## Question and scope

Assess upstream `ab40f0e6` (PR #145, code 3.67.0) against this change's reviewed
`d1142de8`, before committing the integration. Preserve separate research
ownership, proportionate triggering, authorization and independent verification.
This assessment does not authorize merge of the PR or updating installed plugins.

## Method and rationale

Inspect the two specifications, cumulative changed paths and connected upstream
source/test definitions. Use concrete compatibility scenarios: progress without
completion, failed evidence with exit zero, missing publication evidence, and
discovery of our marked test. Source inspection resolves design overlap; complete
integration execution and independent review remain separate obligations.

## Findings

| Surface | Source observation | Compatibility assessment |
|---|---|---|
| Research ownership and triggers | Upstream changes no research skill, stage research handoff or capability manifest. | No competing ownership or trigger policy was found. |
| Publication progress | `_observe_required_ci` adds stderr progress; existing observed-state branches retain their returns and no mutation retry is introduced. | Research still cannot create missing publication proof. Waiting/passed stage text is not a new authority source. |
| Finalization progress | `_finalize` emits stage success only after existing evidence checks; final attestation generation remains distinct. | Supports rather than replaces our separation of research conclusions and execution evidence. |
| Probe discovery | `_carries_concern` now precedes `suite_collection`, preserving `is not False` and moved exclusion. | Our package test has the concern marker, so the reordered eligibility check does not exclude it. Execution remains to be verified. |
| Ship prose | Upstream edits unchanged-wait reporting in Observe CI; ours adds bounded research in authorization intake. | The two passages have different responsibilities and no contradictory instruction was found. |
| Release metadata | Both branches independently used code 3.67.0; dry-run sync identified README/changelog conflicts. | Actual integration defect: preserve upstream 3.67.0 history and issue our code change as 3.68.0; design remains 2.24.0. |

## Evidence

Inspected actual Git objects, not only release summaries:

- `git show origin/main:docs/loom/2026-11-11-agent-tool-efficiency/spec.md`
  and its confirmed intent: bounded progress, concern-first collection, no
  production converter, unchanged authority and verification.
- `git diff 70a05fd7..origin/main -- loom-code/scripts/loom_checker/command_handlers/publish.py`:
  `_observe_required_ci` writes progress via stderr and catches progress-only
  OSError without modifying the existing result/return branches.
- The same upstream diff for `command_handlers/finalize.py`: stage `passed`
  follows `_runner_evidence`, pytest summary and own-pass validation; failure
  returns remain in place. For `probes.py`, only predicate ordering changes.
- Upstream `test_loom_publish.py` and `test_selection_finalize.py` define
  cadence, unchanged stdout, broken-stream authority, exit-zero invalid evidence
  and marker/moved/unknown-collection checks. Reading definitions does not claim
  they ran on this integrated tree.
- Our [spec](../spec.md), plus `git diff 70a05fd7..d1142de8` for Ship,
  Closing Review, manifest, mechanism budget and design package test.
  `loom-design/tests/test_design_research_package.py` begins with its concern
  marker; skill-count admission is independent of probe discovery order.
- `sync-trunk` fetched upstream and reported conflicts only in README.md and
  loom-code/CHANGELOG.md, leaving HEAD untouched. Subsequent uncommitted merge
  work is an integration attempt, not proof of successful verification.

## Decision impact

No semantic conflict requiring a research redesign was found in the inspected
delta. Proceed with a combined integration that preserves upstream behavior and
our bounded handoffs, fixes release identity, and repeats full mechanical checks,
affected acceptance and the original reviewers' terminal round. Dropping either
feature is unnecessary; postponing sync leaves the known release collision.
This is a source-supported recommendation, not a measured runtime guarantee.

## Limitations and open questions

At the initial assessment the merge was uncommitted and integrated tests had not
passed. The old attestation is stale after functional integration and must be
regenerated. Installed code remains separate from repository source: an upstream
merge does not establish that the host is already running its progress behavior.
New upstream commits or a failed integration check require re-evaluation.

## Subsequent bounded integration verification

The implementer observed the existing release check reject the intermediate
3.68.0 SSOT against the old 3.67.0 pin, then synchronized release surfaces.
Release, manifest, Ship, finalization and publication focused checks passed:
210 passed in 98.90s. Derived-manifest check and staged/unstaged diff checks
passed. These are implementer-reported operations, not independent acceptance.

The upstream README CLI section and 3.67.0 changelog were compared byte-for-byte;
finalize/publish/probes match `origin/main`. Ship retains upstream waiting text
and our bounded research paragraph. Integration commit `b95e28e5` preserves both
parents; Git normally restored the saved W5 plan after committing. Complete
suite execution, current acceptance and terminal independent review remain
pending and are recorded separately when actually complete.
