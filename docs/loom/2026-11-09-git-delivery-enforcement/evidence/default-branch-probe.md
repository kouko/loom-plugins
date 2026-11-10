# Default-branch identity probe

The user selected A after being told the exact scope: validate main/custom/missing cases, correct the spec, and authorize one limited supplemental check by the same reviewer. The user reply was `Ａ`. This overrides the third-round stop only for that supplemental check, not a fresh episode, a different reviewer, another external review, or changed Acceptance requirements.

## Observed local fixtures

All Git operations occurred under /private/tmp/loom-default-branch-evidence-20261109; no adopting project was changed.

1. Created a bare origin with initial/default branch develop and one empty seed commit. Initialized a client separately, added origin, fetched develop into origin/develop and switched to its tracking branch. `git symbolic-ref --quiet refs/remotes/origin/HEAD` had no ref, although `git ls-remote --symref origin HEAD` returned `ref: refs/heads/develop HEAD` and the seed commit. The client branch was develop. This confirms the review's missing-metadata premise, not execution of an unimplemented protection hook.
2. Created a separate bare origin-main with HEAD main, pushed the same seed commit as main, and cloned it. The client's remote-default symref was origin/main and the live read reported refs/heads/main.
3. Ran `git remote set-head origin --auto` in the develop client. Git reported that origin/HEAD was created and points to develop; the local symbolic ref then resolved to origin/develop. This demonstrates a concrete metadata-repair route after an appropriate fetch, not an automatic installer mutation.

## Correction to the proposed installer and hook

Install only after a bounded live default-ref observation agrees with a valid local remote-default symref and existing commit. Otherwise refuse with a repair suggestion and no hook/config writes. At runtime, a missing/invalid local identity refuses; main/master are additional protected names, never guesses establishing the default. Hook removal is independent of remote metadata. The shell hook remains free of Python and installed-plugin paths.

The remote can later change its default while the client is offline; no local-only hook can certify an unobserved remote change. Document last-known-local identity and retain server rules as the remote authority. Tests still need to exercise the actual installer/hooks after implementation; these fixtures only establish Git observations and repair feasibility.
