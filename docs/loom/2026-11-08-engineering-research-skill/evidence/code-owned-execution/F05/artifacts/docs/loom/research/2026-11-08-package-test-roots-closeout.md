---
title: "Package-test research merge, release and preservation closeout"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

## Question and scope

Has the local research-fixture change merged, what release and cleanup evidence exists, and which research can be proposed for later Obsidian preservation? Scope is this temporary fixture on 2026-11-08, not the original repository's deployment. This is a lifecycle question distinct from the [original source investigation](2026-11-08-package-test-roots.md), which remains unchanged.

## Method and rationale

Inspect local Git history and supplied evidence, and recheck the bounded source findings for preservation. No experiment is needed to establish ancestry or inspect the runner's branches. No tests, sample commands, network, apps, installation, external models or agents were used. Source inspection and hash verification are not execution validation.

## Findings and evidence

### Merge and cleanup

- `git log --all --decorate --oneline --graph -8` and `git show --no-patch --format=fuller HEAD` show main/HEAD at merge `4959e620a78e15678a3cc2a8a0c18f79de58dc73`, with parents `3236024` and `00fa764`. `research-fixture` points to `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`; `git branch --contains research-fixture` lists main and research-fixture. This directly verifies the exact local merge, not a real upstream merge.
- `git show --stat 00fa764` identifies the retained research, original snapshot and executor receipt as the merged change's three added files. The supplied source snapshot is older, separately attributed by [provenance](../../../provenance.json) to `d5a7f0da247214bdb9c61fe90c550256432e5f76`. These revision identities must not be conflated.
- [Cleanup receipt](../../../fixture-cleanup.json) reports an empty `git status --porcelain` result at the exact merge revision, no generated build artifact or linked worktree, and topic-branch retention for audit. Its cleanup destination `.` is this current project directory. This supports historical, fixture-only lifecycle completion within its stated scope.
- Before this closeout's writes, `git status --short --branch` showed main with untracked `fixture-cleanup.json` and `skill/`. `git status --porcelain --untracked-files=no` returned no output; `git worktree list --porcelain` listed only this main worktree. Thus tracked contents were clean, but the current complete working tree was not clean. The receipt and current observation describe different moments; neither justifies deleting supplied inputs. Closeout records and scratch drafts will add intentional untracked files.

### Release and installed behavior

- `git tag --list` and `git remote -v` both returned no output. No supplied artifact establishes a release containing the change. This means release is unverified, not that an upstream release does not exist.
- [Existing executor receipt](../../../sample-receipt.json) reports exit code 0, source unchanged and the added research record for a prior isolated invocation. Its requested model is not server-confirmed (`server_confirmed_model: null`). It does not establish plugin installation, complete CI, deployed behavior, release, user acceptance or this invocation's runtime behavior. Its embedded command was read only.

### Enduring research eligible for a proposal

- Re-read [runner](../../../src/scripts/run_package_tests.py), especially lines 51–55, 68–114 and 116–175, and [test definitions](../../../src/tests/test_run_package_tests.py), lines 222–235 and 285–310. The four roots and preset-specific direct `local/` exclusions remain source-supported; explicit-argument mode does not add that local exclusion. The original findings need no change. Nested-repository behavior is outside the proposed scope.
- `shasum -a 256` reproduced the runner hash `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and test hash `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`, matching provenance. `git diff --exit-code HEAD -- docs/loom/research/2026-11-08-package-test-roots.md src provenance.json snapshots sample-receipt.json` exited 0 without output. These are static checks, not test results.

## Decision impact

The local merged research can be closed out. The historical cleanup evidence is sufficient for a bounded optional preservation proposal; the current untracked fixture inputs are explicitly accounted for. No release-dependent claim is eligible.

The [reviewable preservation draft](../../../scratch/package-test-roots-obsidian-proposal.md) proposes only the runner's root inventory, local exclusion boundary, test-placement implication and evidence limitations. It includes local revision-pinned evidence copies extracted with `git show` into scratch, leaving project originals in place. These are fixture-local links, not published upstream permalinks.

Proposed destination is `<user-selected fixtureVault path>/Engineering/package-test-roots-and-local-exclusion.md`; the Vault path remains unresolved. The Obsidian CLI is unavailable and no destination discovery was attempted. No fixtureVault file was inspected or written. Saving requires the user's selection of the exact fixture destination and approval of this draft's scope; an existing destination note would require separate overwrite approval. This optional decision does not block project closeout.

## Limitations and open questions

Real upstream merge, release contents, installation, CI and runtime outcomes are unverified. The source snapshot is incomplete. The preservation candidate is a saved project scratch draft, not a saved Obsidian note. Its absolute fixture-local evidence links will stop resolving if this temporary workspace is removed; a durable source location must be agreed before relying on it for long-term access. No automatic release watching or synchronization is planned.
