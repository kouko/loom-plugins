# Intake observation comparison — reproducible collection

Scope: Acceptance 3/4 of the [confirmed intent](../../intent/2026-11-11-intake-observation-pilot.md). Collection uses implementation `26f3049d` and existing intake fixtures. This records CLI observations, not agent-consumption results or an acceptance verdict. Independent consumption is pending.

## Experiment boundary

Compare ordinary text, the same text plus explicit interpretation guidance, and opt-in JSON on matched controlled repositories. Keep the same question, fixture inputs and requested answer fields. The guidance-only arm reuses the exact text run; it adds no CLI invocation. Run text and JSON once each per real case, in that order. Elapsed time includes process startup and local Git; this is not a randomized latency benchmark.

Five real CLI cases cover a pass, confirmation early exit, later rule failure, unavailable repository and invalid invocation. A sixth case is an explicitly injected crash-output control (exit 2 with partial output), not a checker defect or runtime observation. Case labels in packets are neutral; the separate answer key identifies construction and expected outcomes. The fixture source and answer key are withheld from consumer agents. No private conversation data or external model is used during collection.

Packets contain `arm`, `instructions`, optional `guidance`, and `cases[]` with `case_id`, `exit_code`, `stdout`, `stderr`. They contain no expected answer, fixture name or measured correctness. The neutral question asks for intake readiness, observed blockers, whether applicable checks completed and whether recovery/rerun is needed. Completeness means only this intake path; it never grants downstream workflow authority. The answer key distinguishes underlying outcomes from observable information: justified unknown completeness in the text-only arm is acceptable, not an agent error. For a crash, uncertainty about completion is also acceptable in every arm. A later scorer must preserve those distinctions rather than rewarding guesses.

## Replay

From the repository root, extract the Python block below and execute it with the locked environment. `--offline` requires the dependencies already cached; failure to resolve them is an environment failure, not an experiment result. Files are written only beneath `/private/tmp/loom-intake-comparison`; inspected fixture content is snapshotted before/after each pair, excluding `.git` metadata from this collection check (the focused implementation test checks Git bytes too).

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -c 'from pathlib import Path; p=Path("docs/loom/2026-11-11-intake-observation-pilot/evidence/comparison.md"); exec(p.read_text().split("```python\n", 1)[1].split("```", 1)[0])'
```

```python
import importlib.util
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

root = Path.cwd()
output = Path("/private/tmp/loom-intake-comparison")
output.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("intake_fixtures", root / "loom-code/tests/test_loom_checker_intake.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
question = (
    "For each observation determine intake readiness, list observed blockers, "
    "say whether applicable intake checks completed, and state whether recovery "
    "or rerun is needed. Distinguish unknown from false. Return JSON answers "
    "keyed by case_id with ready, blockers, checks_complete, recovery_or_rerun, "
    "and a brief reason. Intake readiness alone does not authorize later workflow steps."
)
guidance = (
    "Ordinary text: exit 0 means applicable intake checks passed; exit 1 means "
    "returned rule failures; exit 2 is invalid invocation/unavailable observation "
    "or crash. BLOCK lines carry rule/reason pairs. intake.confirmed failures "
    "stop before later checks, so those checks did not complete. Later returned "
    "rule failures finish the applicable path. Other output is informational. "
    "Recover and rerun errors; preserve blockers and rerun after inputs change."
)
packets = {arm: {"arm": arm, "instructions": question, "cases": []}
           for arm in ("text", "guided_text", "json")}
packets["guided_text"]["guidance"] = guidance
answer_key, metrics = {}, []
constructions = ("pass", "confirmation", "later", "unavailable", "invalid")
with tempfile.TemporaryDirectory(prefix="fixtures-", dir=output) as temporary:
    for index, construction in enumerate(constructions, 1):
        case_id = f"C{index:02}"
        directory = Path(temporary) / case_id
        directory.mkdir()
        repo = directory if construction == "unavailable" else fixture.make_repo(directory)
        if construction != "unavailable":
            fixture.write_intent(repo, status="status: open" if construction == "confirmation" else "status: confirmed 2026-09-02")
        if construction == "later":
            fixture.write_spec(repo)
            path = repo / f"docs/loom/{fixture.CHANGE}/spec.md"
            path.write_text(path.read_text().replace("Acceptance #1", "Acceptance #99"))
        args = ["intake", "build" if construction == "invalid" else "write-plan", fixture.CHANGE]
        before = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob("*")
                  if p.is_file() and ".git" not in p.relative_to(repo).parts}
        results = {}
        for arm in ("text", "json"):
            start = time.perf_counter()
            run = fixture.run_checker(*args, *(["--json"] if arm == "json" else []), cwd=repo)
            elapsed = time.perf_counter() - start
            observation = {"case_id": case_id, "exit_code": run.returncode,
                           "stdout": run.stdout, "stderr": run.stderr}
            packets[arm]["cases"].append(observation)
            results[arm] = observation
            metrics.append({"case_id": case_id, "arm": arm, "seconds": elapsed,
                            "output_bytes": len((run.stdout + run.stderr).encode())})
        packets["guided_text"]["cases"].append(results["text"])
        after = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob("*")
                 if p.is_file() and ".git" not in p.relative_to(repo).parts}
        assert before == after
        payload = json.loads(results["json"]["stdout"])
        expected_exit = 0 if construction == "pass" else 1 if construction in ("confirmation", "later") else 2
        assert results["text"]["exit_code"] == results["json"]["exit_code"] == expected_exit
        expected_rules = [] if expected_exit != 1 else ["intake.confirmed" if construction == "confirmation" else "spec.req-grammar"]
        assert [item["rule"] for item in payload["failures"]] == expected_rules
        assert payload["checks_complete"] == (construction in ("pass", "later"))
        assert payload["state"] == ("passed" if expected_exit == 0 else "blocked" if expected_exit == 1 else "unconfirmed")
        assert fixture.blocked_rules(subprocess.CompletedProcess([], expected_exit, results["text"]["stdout"], results["text"]["stderr"])) == set(expected_rules)
        answer_key[case_id] = {"construction": construction, "source": "real-cli",
                              "ready": construction == "pass", "checks_complete": payload["checks_complete"],
                              "failures": payload["failures"], "error": payload["error"],
                              "recovery_or_rerun": construction != "pass"}
control = {"case_id": "C06", "exit_code": 2, "stdout": '{"state": "passed",',
           "stderr": "loom_checker internal error: RuntimeError: injected control\n"}
for packet in packets.values():
    packet["cases"].append(control)
answer_key["C06"] = {"construction": "injected partial-output crash", "source": "synthetic-control",
                     "ready": False, "checks_complete": False, "failures": [],
                     "error": "injected crash", "recovery_or_rerun": True}
for case_id, answer in answer_key.items():
    complete = answer["checks_complete"]
    answer["acceptable_completeness"] = {
        "text": [complete, None],
        "guided_text": [complete, None] if case_id == "C06" else [complete],
        "json": [complete, None] if case_id == "C06" else [complete],
    }
for arm, packet in packets.items():
    (output / f"packet-{arm}.json").write_text(json.dumps(packet, indent=2) + "\n")
(output / "answer-key.json").write_text(json.dumps(answer_key, indent=2) + "\n")
(output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
sys.path.insert(0, str(root / "loom-code/scripts"))
import dispatch_profile as dispatch
base = {"event": "initial", "main_profile": {"model": "standard", "effort": "medium"},
        "capabilities": {tier: ["medium"] for tier in dispatch.MODELS},
        "inheritance_guaranteed": True, "completed_redispatches": 0}
mechanical = dict.fromkeys(dispatch.MECHANICAL_FIELDS, True)
inputs = [None, {}, {"trust_boundary": False}, {"trust_boundary": True}, mechanical,
          {**mechanical, "trust_boundary": True}, {"trust_boundary": None}]
dispatch_results = []
for evidence in inputs:
    try:
        result = dispatch.resolve({**base, "task_evidence": evidence})
        dispatch_results.append({"input": evidence, "task_class": result["task_class"],
                                 "uncertainty": result["uncertainty"], "effective_profile": result["effective_profile"]})
    except dispatch.InputError as error:
        dispatch_results.append({"input": evidence, "error": str(error)})
assert [row.get("task_class") for row in dispatch_results] == ["ordinary", "ordinary", "ordinary", "complex", "mechanical", "mechanical", None]
assert dispatch_results[0]["uncertainty"] == "insufficient-task-evidence"
assert dispatch_results[1]["uncertainty"] is None
assert "booleans" in dispatch_results[-1]["error"]
(output / "input-reproduction.json").write_text(json.dumps(dispatch_results, indent=2) + "\n")
print(json.dumps({"real_cli_pairs": len(constructions), "injected_controls": 1,
                  "packet_cases": {arm: len(packet["cases"]) for arm, packet in packets.items()},
                  "input_cases": len(dispatch_results), "output": str(output)}))
```

## Recorded collection results

The recipe completed on 2026-11-11: 5 real CLI pairs, 1 injected control, 6 cases in each of 3 packets, and 7 input perturbations. All paired exit codes, blocking rule identities, JSON states/completeness and inspected fixture-content snapshots agreed with the independent construction expectations. The initial collection attempt used the wrong expected rule name (`intake.req-grammar`); source inspection confirmed `spec.req-grammar`, and correcting that setup expectation allowed replay to complete. This was a collection setup error, not a product defect.

Raw materials are under `/private/tmp/loom-intake-comparison`: `packet-text.json`, `packet-guided_text.json`, `packet-json.json`, `answer-key.json`, `metrics.json`, and `input-reproduction.json`. Temporary fixture repositories are removed after collection; the full reconstruction recipe remains above. Random temporary path suffixes and durations vary on replay. Packet bytes include serialization and the shared question; they are not model-token counts.

Measured values from the final recipe replay (single run, text before JSON):

| Case | Text bytes | JSON bytes | Text seconds | JSON seconds |
|---|---:|---:|---:|---:|
| C01 pass | 151 | 301 | 0.1615 | 0.1586 |
| C02 confirmation blocker | 92 | 260 | 0.0794 | 0.0794 |
| C03 later blocker | 252 | 420 | 0.1573 | 0.1601 |
| C04 unavailable repository | 89 | 241 | 0.0756 | 0.0715 |
| C05 invalid station | 66 | 213 | 0.0464 | 0.0466 |

Packet sizes: text 1,765 bytes; guided text 2,236 bytes; JSON 2,681 bytes. The guidance-only packet adds 471 bytes; the JSON packet adds 916 bytes relative to the text packet. The injected crash control is excluded from CLI duration measurements. JSON is larger on these cases, so this collection provides no byte-saving claim.

All seven resolver input results match the research table: missing/empty/negative select ordinary, risk selects complex, mechanical and mixed select mechanical, and a field-level null is rejected. These are real executions of synthetic inputs; they establish handling and precedence, not task-classification accuracy or actual host dispatch.

Independent agent answers, correctness scoring and model-token usage are not yet available. Output byte counts and one local execution duration cannot establish parent-model call reduction, total latency savings or improved semantic correctness. Guidance-only remains a viable adoption alternative; structured output has not yet demonstrated an agent-consumption benefit. The parent orchestrator separately reported a successful current-branch `loom-python --ready intake write-plan 2026-11-11-intake-observation-pilot --json` invocation (passed, complete, no failures); that is self-dogfood, not independent consumption.
