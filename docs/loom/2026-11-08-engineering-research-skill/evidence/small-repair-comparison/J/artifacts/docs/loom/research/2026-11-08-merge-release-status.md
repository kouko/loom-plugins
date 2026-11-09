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

Has the local `research-fixture` branch been merged into `main` in this temporary git fixture, and is there any evidence of a release or installation? The answer decides whether the finished engineering research may be proposed for long-term preservation. Scope is the temporary local fixture only; it is not the original project, a real deployment, CI, or a user Vault. This is a separate question from the test-roots finding in [the earlier record](2026-11-08-package-test-roots.md), which is left unchanged.

## Method and rationale

Reuse of harness-supplied local git observations ([fixture-observations.json](../../../fixture-observations.json), [fixture-cleanup.json](../../../fixture-cleanup.json)), read as files. This fits because no command tool was available to the executor; the observations are a harness record, not commands I ran. Stop once merge, cleanup and release evidence are each either supported or shown absent.

## Findings

- **Merged (observation):** `main` = `4959e620a78e15678a3cc2a8a0c18f79de58dc73` ("merge temporary research fixture"); `research-fixture` = `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`. `git merge-base --is-ancestor research-fixture main` exited 0, so the branch tip is contained in `main`. The log shows `4959e62` over `00fa764` over `3236024`.
- **Cleanup (observation, scoped):** the cleanup record reports a clean post-merge `main` working tree (`git status --porcelain` empty), no linked worktree or build artifact created, and the topic branch deliberately retained. Cleanup destination is `.`.
- **Release: no evidence.** `git tag --list` returned nothing and `git remote -v` returned nothing: no tag, no remote, no hosting or publication record. Nothing shows installation either.
- **Merge is not release or approval.** A local merge says nothing about release, publication, installation, or user approval of any action.
- **Current tree (inference from the session's initial git status):** untracked `fixture-cleanup.json`, `fixture-observations.json` and `skill/` exist now; they are harness/executor additions, not part of the merged revision.

## Evidence

| Claim | Source | Kind |
|---|---|---|
| main/branch revisions, ancestry, log | `git` entries in [fixture-observations.json](../../../fixture-observations.json) (exit codes 0) | harness-recorded runtime observation; not re-run by me |
| clean tree, topic branch retained | [fixture-cleanup.json](../../../fixture-cleanup.json) | harness-recorded observation, fixture only |
| no tags, no remotes | same observations file, empty stdout | harness-recorded observation |
| source provenance of the earlier finding | [provenance.json](../../../provenance.json): upstream HEAD `d5a7f0da247214bdb9c61fe90c550256432e5f76`, remote freshness "not checked" | file inspection |

## Decision impact

The merge into the fixture's `main` is verified, so a preservation proposal for the earlier source-supported finding is eligible to be prepared. Nothing supports any release-dependent claim, so none should be made. No Vault write is authorized; the proposal remains a candidate awaiting the user's decision. See `scratch/vault-preservation-proposal.md`.

## Limitations and open questions

- I ran no git command; all git facts come from pre-recorded harness observations taken before the executor's files were inserted.
- Fixture-only: no real host, release, installed cache, CI or user Vault was checked. The absence of tags and remotes only shows no release in this local repository.
- Upstream remote freshness was "not checked" in provenance.
- Revalidate if a tag, remote or installation appears.
