# host-memory-trigger — trigger-rate measurement

This eval measures whether `loom-memory` fires at the moment the agent is
about to save a lesson to its own host-managed memory, and whether Record
then keeps only a repo-wide lesson. It is not automated and it does not run
in CI.

| Failure | Guard | Runs |
|---|---|---|
| The trigger or exclusion text is deleted | `loom-workflow/tests/loom-memory/test_skill_contract.py` | every push |
| The text is kept but the description no longer makes the skill fire | this eval | when the description or activation text changes |

A string assertion cannot tell whether a description fires. Only a live
session can, so the guard is a live session.

## Method

1. Use a repository with loom-workflow installed and a fresh `claude -p`
   session per trial: no prior context, no resumed session.
2. Never pass `--disable-slash-commands`. It disables skills too, so the
   trial would run and test nothing.
3. For each candidate in `host-memory-trigger-cases.json`, tell the session
   about the lesson and ask it to save it to its own memory.
4. Run every case with the OLD description and with the NEW description
   from that file, the same number of trials each.
5. Before counting a trial, confirm from its transcript that `loom-memory`
   actually fired. A session with no skill invocation counts as not fired,
   never as a pass.
6. Record per case and per description: trials, fired, recorded to the
   store, kept only in host memory with a stated reason.

Expected: only candidate 1 (repo-wide) is recorded; candidate 2 (personal
preference) and candidate 3 (machine-specific fact) stay only in host
memory. Description triggering is probabilistic: report counts, never a
guaranteed rate.

## Results

Pending. The run is performed at acceptance testing, and its counts for
OLD against NEW are recorded here then.
