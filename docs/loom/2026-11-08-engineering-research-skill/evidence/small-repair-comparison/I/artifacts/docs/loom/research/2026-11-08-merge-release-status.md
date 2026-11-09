---
title: "Merge and release status of the research-fixture branch"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Merge and release status of the research-fixture branch

## Question and scope

Has `research-fixture` been merged into `main` in this temporary local git fixture, and is there any evidence of a release or installation? The answer decides whether finishing may offer an optional long-term (Obsidian) preservation proposal. No active change is known, so there is no `change` property. The fixture is a harness-built temporary repository, not the original project's deployment.

## Method and rationale

Local history and state inspection. Reused evidence: the harness-supplied [observations](../../../fixture-observations.json) and [cleanup record](../../../fixture-cleanup.json), which are actual git query output captured before this session. I did not run git (no command tool). I independently read the ref files `.git/refs/heads/main` and `.git/refs/heads/research-fixture`. This is enough for a local merge/release-state question.

## Findings

- Observed (harness): `main` = `4959e620a78e15678a3cc2a8a0c18f79de58dc73`, `research-fixture` = `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`.
- Observed (harness): `git merge-base --is-ancestor research-fixture main` exited 0, so the branch tip is an ancestor of `main`. The log shows merge commit `4959e62` on top of `00fa764`.
- Observed (this session, direct file read): both ref files contain exactly those two hashes, consistent with the harness output.
- Observed (harness): `git tag --list` was empty and `git remote -v` was empty. No tag, no remote, and no hosting evidence exist.
- Observed (harness): the post-merge working tree was clean apart from the untracked cleanup JSON. No linked worktree was created. The topic branch is retained as audit evidence.
- Inference: the merge into the local `main` is verified. A release is not evidenced, since there is no tag, remote or release record. Installation is not evidenced either. A merge is not a release, an approval or an installation.
- Not established: the harness observations predate this session. I did not re-run git and cannot confirm the current working tree (this session's start-up status also lists untracked `skill/` and `fixture-observations.json`, which are harness artifacts). The harness supplied no post-write hash for the actor copy.
- Provenance hashes: the harness SHA256 values for the `src/` snapshot files equal the entries in [provenance](../../../provenance.json) for the runner, the test file, `repo_files.py` and `git_exec.py`. I did not recompute them. The fixture's merged research record hash (`c54f2872…1283`) was not recomputed either.

## Evidence

| Claim | Source | Kind |
|---|---|---|
| Merge into main | [fixture-observations.json](../../../fixture-observations.json) `git[0..2]`; `.git/refs/heads/*` | harness output; direct file read |
| No tags or remote | same file, `git[4]`, `git[5]` | harness output |
| Clean tree, cleanup scope | [fixture-cleanup.json](../../../fixture-cleanup.json) | harness output |
| Source snapshot origin | [provenance.json](../../../provenance.json), original commit `d5a7f0da…` | supplied record; remote freshness "not checked" |

## Decision impact

- Merge is verified for this temporary fixture, so the optional preservation proposal is eligible (see [preservation proposal draft](../../../scratch/obsidian-preservation-proposal.md)).
- Release-dependent claims must be deferred. The one candidate finding ([package test roots](2026-11-08-package-test-roots.md)) is a source finding at a pinned snapshot and does not depend on a release.
- Nothing here authorizes a Vault write, publication or installation. Each needs a separate user decision.

## Limitations and open questions

- Observations are pre-session harness data, not commands I ran.
- The local `main` has no remote, so remote freshness and hosting merge state are unknowable here.
- Whether the original project released the underlying commit `d5a7f0da…` is outside the evidence.
