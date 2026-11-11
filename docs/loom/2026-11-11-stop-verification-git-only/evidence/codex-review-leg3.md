**1. Verdict: NEEDS_REVISION**
The new Stop check can reach file writes and test collection through the `no_program` attestation path, violating A6.

Reviewed `a8ec84e0..b9ab515c4df506bbde77b80471040d874a33d68a`, read-only. The publication reminder is expected hook noise; publication remains the orchestrator’s responsibility.

**2. Acceptance table**

Pass results reflect source inspection and isolated checks, not a full pytest run.

| Acceptance | pass/fail/cannot-verify | Evidence `path:line` |
|---|---|---|
| A1 | pass | [loom-code/scripts/loom_checker/command_handlers/publish.py:538](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/command_handlers/publish.py:538): `if verification_status(repo, change_id) != "valid":` then `return 0`. Actual absent-attestation checkout returned exit 0, empty stdout/stderr, and no remote observation. |
| A2 | pass | [loom-code/scripts/loom_checker/command_handlers/publish.py:550](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/command_handlers/publish.py:550): `{"decision": "block", "reason": feedback}`. With verification returning valid, unpublished output matched the base exactly. |
| A3 | pass | [loom-code/scripts/loom_checker/verification.py:127](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/verification.py:127): `return f"stale ({failures[0][1]})"`. Absent and three stale-result cases were silent through the new gate. |
| A4 | pass | [loom-code/scripts/loom_checker/command_handlers/publish.py:545](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/command_handlers/publish.py:545): `if payload.get("stop_hook_active") or observed.state == "unconfirmed":`. Fourteen state/payload combinations matched the base, conditional on verification returning valid. |
| A5 | pass | [loom-code/scripts/loom_checker/command_handlers/publish.py:607](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/command_handlers/publish.py:607): `observed = observe_delivery(...)`. Manual functions are unchanged; seven isolated JSON-state checks bypassed verification and retained exit codes. |
| A6 | **fail** | [loom-code/scripts/loom_checker/attestation.py:287](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/attestation.py:287): `stored_probe_programs(repo, head_sha, change_id) if no_program else 0,`. This reaches temporary-file creation and pytest collection. The existing single 20-second timer remains. |
| A7 | pass | [loom-code/hooks/hooks.json:3](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/hooks/hooks.json:3) and [loom-code/hooks/hooks-codex.json:3](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/hooks/hooks-codex.json:3): both invoke `--ready delivery --hook`; configurations match after root-variable normalization. Live cross-host behavior was not tested. |

**3. Findings**

**fatal · [loom-code/scripts/loom_checker/command_handlers/publish.py:538](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/command_handlers/publish.py:538) · Stop now reaches validation that can write files and execute repository code.**

```python
if verification_status(repo, change_id) != "valid":
    return 0
```

**Prior reviewer’s claim: CONFIRMED, conditionally.** An attestation passing preceding checks, containing an adversarial `no_program` record, and associated with an added program file reaches this path:

| Step | Evidence |
|---|---|
| Verification invokes attestation validation. | [verification.py:124](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/verification.py:124) |
| `no_program` triggers stored-program counting. | [attestation.py:285](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/attestation.py:285) |
| Counting includes programs added to the package suite. | [probes.py:569](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/probes.py:569) |
| Added programs undergo collection before their concern marker is checked. | [probes.py:512](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/probes.py:512) |
| Python collection creates temporary files and launches pytest. | [probes.py:195](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/probes.py:195), [probes.py:204](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/probes.py:204) |

The in-memory reproduction intercepted a write to `_loom_pytest_collection.py` and an attempted launch of:

```text
python3 -m pytest -q --collect-only -p _loom_pytest_collection
```

Neither operation was allowed to execute. The Go route also launches `go list -json` ([probes.py:339](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/probes.py:339)); the inspected Cargo route reads metadata without launching Cargo.

The absent-attestation exception is real: [verification.py:110](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/loom-code/scripts/loom_checker/verification.py:110) returns `absent` before validation. That short circuit was independently checked.

**Why wrong:** the added call introduces writes and repository-controlled execution into Stop, violating A6. Collection also reads working-tree configuration and consumes the shared deadline. The new fixtures use direct adversarial execution records and miss this conditional path.

**Fix direction:** separate collection from committed-evidence validation so attestation recomputation remains read-only, including valid `no_program` records. Add a regression with an added ordinary Python test that rejects file writes and non-Git subprocesses during Stop.

**4. What I ran or read**

- Read the governing [intent](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/docs/loom/intent/2026-11-11-delivery-reminder-publication-boundary.md), [plan](/Users/kouko/GitHub/loom-plugins-wt-2026-11-11-delivery-reminder-session-scope/docs/loom/2026-11-11-delivery-reminder-publication-boundary/plan.md), requested diffs, both changed test files and fixtures, verification/attestation helpers, and host hook configurations.
- Ran Python with `-B`: actual absent-attestation check; intercepted collection/write reachability checks; 14 base/HEAD hook comparisons; four absent/stale cases; seven manual JSON cases; host-configuration comparison.
- Ran `git diff --check a8ec84e0..HEAD`: passed. HEAD remained unchanged and the working tree clean.
- Did not run filesystem-backed pytest suites: their fixtures require writes prohibited in this session.
- Ran the required installed `loom-python --ready delivery --json`: exit 1, `unconfirmed`, because GitHub connectivity was unavailable. No publication action was taken.
