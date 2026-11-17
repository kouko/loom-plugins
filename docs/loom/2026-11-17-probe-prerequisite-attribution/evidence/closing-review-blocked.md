# Closing review: unresolved Round 1 findings and missing runtime

## State

- Change: `2026-11-17-probe-prerequisite-attribution`.
- Branch/worktree: `testing-file-limit` in the active worktree.
- Branch base: `d3faa624d436f22aaa083b8f2b163bb924c2e7ba`.
- Round 1 review target: `6ec90d1c8678ca4d2551372a52118114e3748ecb`.
- Closing review has consumed **one functional-content digest**. No Round 2
  or finalizer has run. This is the new Loom correction, not a reset of the
  separate finance terminal episode.
- Source release metadata is `3.84.0`, local only. Nothing was pushed,
  published, merged remotely or installed by this task.

## Completed evidence

Build package runner exited 0: 4040 pytest passes, five skips and passing
shell tests. Independent adversary: 17 attack points, zero successful attacks,
one reused program. Independent clean-copy acceptance: six `works` rows,
84 focused passes. These observations do not cover the newly identified
glob-significant filename defect below and are not a final passing review.

Acceptance evidence distinguishes pure Git/JSON provenance at the finance
handoff pin `9de82a7` from an additional collection query against its moving
working tree. That query collected tests but executed no test cases or
finalizer; subsequent tracked/untracked status was clean. The pinned helper
proved the original five prerequisites. Live finance delivery is unverified.

## Reviewer 1: `/root/closing_code`

Lens: `code`. Verdict: **NEEDS_REVISION**.
Scores: security, architecture, naming, tests, refactoring,
cross-task-coherence, deliberate-simplification and deletion-first PASS;
correctness, external-surface-grounding and principles-conformance
NEEDS_REVISION; architecture-conformance N/A (no ratified ARCHITECTURE.md).

1. **Fatal correctness**, `loom-code/scripts/loom_checker/probe_attribution.py:69`:
   Git log treats an artifact filename as a wildcard pathspec. A literal
   `test_[x].py` modified and restored has equal old/current tree identities,
   but its history query can search `test_x.py` and miss both alterations,
   falsely granting a prerequisite exclusion. Fix the artifact history query
   with literal pathspec semantics. Extend the existing reverted-path fixture
   using a glob-significant filename, observe RED, then fix to GREEN.
2. **Fatal external-surface-grounding**, same anchor: add official Git
   documentation for literal pathspec and ancestry/history traversal semantics
   alongside the correction. Both findings belong to the same defect class:
   incorrect assumptions about external Git path/history interpretation.

The reviewer independently ran the changed repository test modules: nine
attribution tests and 43 release-pin tests passed. Read-only existing-tree
commands confirmed the asymmetry: `ls-tree` with
`loom-code/scripts/loom_checker/probe_[a]ttribution.py` returned no entry,
whereas `log` with that pattern selected a commit for `probe_attribution.py`.
No adversarial program or finance execution was created by the reviewer.

## Runtime blocker

Before dispatching the second required reviewer, the mandatory dispatch
resolver invocation failed with exit 127:

```text
zsh:1: no such file or directory: /Users/kouko/.codex/plugins/cache/loom/loom-code/3.82.0/scripts/loom-python
```

The same installed path had worked throughout Build and acceptance. Its
disappearance does not establish which version, if any, is now installed.
No alternative cache version or PATH checker was searched or executed.
The installed first-contact policy requires restart after losing a live
versioned checker path; runtime-dependent dispatch and finalization cannot
continue here. No completion or valid current attestation is claimed.

## Resume without resetting the episode

After restarting the host session with its current installed plugin, retain
this intent, spec, plan, branch, all evidence, the Round 1 target and findings.
First recover the runtime through the installed skill's normal contract check.
Complete the second independent Round 1 review on the same target before
batching fixes. Search the changed files for every instance of the Git
literal-pathspec defect class; hand all instances and both findings to an
implementer under Build. Preserve the frozen prerequisite horizon, identity,
explicit reuse and full review scope guarantees. Confirm RED for the filename
case before fixing; source changes then require complete Build checks,
affected acceptance re-testing and the same reviewers' Round 2 verification.
Do not treat a new session, branch or reviewer label as a new episode.
Finalization and local delivery observation remain outstanding. Keep the
finance episode and historical evidence untouched; no publication is authorized.
