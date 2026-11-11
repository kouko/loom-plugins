# Intake observation comparison — reproducible collection

Scope: Acceptance 3/4 of the [confirmed intent](../../intent/2026-11-11-intake-observation-pilot.md). Collection uses implementation `26f3049d` and existing intake fixtures. This records CLI observations, not agent-consumption results or an acceptance verdict. Independent consumption and replay at `7da5d59` are now recorded in [witnessed acceptance evidence](acceptance-test-evidence.md), with the original packets, answers and scoring retained alongside it.

## Final adoption and continuity

The final design selects **guidance-only** under the original REQ-3 alternative. The witnessed guided-text and JSON answers made equivalent decisions across six cases; JSON added 445 packet bytes over guided text without a demonstrated consumption or error-handling benefit. The JSON handler, help additions and implementer-owned JSON tests are therefore withdrawn, while the existing text command and all its checks remain unchanged. Station guidance explains the existing exit codes, confirmation early exit, blockers, uncertainty and rerun boundaries. This is a bounded selection from measured alternatives, not a claim that text is universally superior or cheaper in model tokens.

The canonical acceptance report at `4fe583e5` remains an unchanged report of the candidate, including Acceptance 3 = partly; it does not certify this revised tree. Raw answers, key, scoring and runtime outputs remain unchanged. Fresh acceptance and adversarial evaluation must address the final scope. The candidate-specific repeated-JSON probe is left unchanged for its independent author to re-evaluate; a failure after withdrawal is expected until that scope is reconciled, and is not hidden as a passing full suite.

| Stage | Retained evidence and cost |
|---|---|
| Initial implementation `26f3049d` | 15 RED failures / 191 passes, then 206 passes; handler +40 net lines, tests +67 and guidance +9 |
| Comparison `15e6d328` | Five real pairs and one injected control; initial expected-rule typo corrected from source, then recipe passed; seven synthetic dispatch cases retained |
| Release `4c362237` | 3.66.0 metadata; 1 RED release check, then 6 passes |
| Adversary `fd65d1f1` and repair `7da5d59` | Repeated option became an id; 5 RED failures / 11 passes, then 215 focused passes; unchanged 24-line adversarial probe graduated, regression gained 6 net lines, handler gained 2 |
| Independent acceptance `4fe583e5` | 377 focused passes and unchanged 3,946-file snapshot at candidate `7da5d59`; all guided-text/JSON decisions equivalent, adoption condition unmet |
| Final adoption repair | Removes the candidate's 42 net handler lines, help extension and 73 implementer-owned test lines; retains station guidance, release metadata and all experiment records. No new classifier, format, check or authority rule |

The consumer was one fresh agent in a sequential text → guidance → JSON crossover, not independent randomized samples. Text's two justified unknown-completeness answers are information limits, not errors. No measured model-token, parent-turn, monetary or total-latency saving is available. The crash control establishes safe recovery, not the actual number of checks completed before a crash.

### Final guidance acceptance entry

A fresh tester should use a clean checkout of the final candidate, read the final write-plan intake guidance, and invoke `loom-code/scripts/loom-python --ready intake write-plan 2026-11-11-intake-observation-pilot` without a format flag. Retain actual text/exit observations and before/after file snapshots. Reuse the existing fixtures for pass, confirmation blocker, later blocker and unavailable input, then assess consumption of those observations with the final guidance. Check changed-input rerun and downstream-authority boundaries; treat a crash as unknown completeness. The existing focused entry is `python -m pytest -q loom-code/tests/test_loom_checker_intake.py loom-code/tests/test_write_plan_station_text.py` in the locked uv environment. These are replay instructions, not an assertion that final independent acceptance has happened. Update the canonical report through the independent tester; preserve the earlier candidate results and partly finding as history.

Implementer verification of the adoption repair: the existing intake/station modules passed **191 tests in 44.17s**. Handler, checker help and original intake tests are byte-identical to branch base `91ee3610`. The pinned historical replay completed all five pairs, one control and seven input cases at its separate temporary destination. The first final text self-check exposed plan field caps/formatting; reducing that plan's entries and wording restored the existing intake pass. The unchanged candidate-specific adversary probe failed as expected (`JSONDecodeError`, 1 failed in 0.19s) because it still demands the removed output; its SHA-256 remains `b0bbf303000b87268f3eed92cab8959165e51a96824fe52a369441c15f571537`. No complete-suite success or final independent acceptance is claimed by this repair.

## Experiment boundary

Compare ordinary text, the same text plus explicit interpretation guidance, and opt-in JSON on matched controlled repositories. Keep the same question, fixture inputs and requested answer fields. The guidance-only arm reuses the exact text run; it adds no CLI invocation. Run text and JSON once each per real case, in that order. Elapsed time includes process startup and local Git; this is not a randomized latency benchmark.

Five real CLI cases cover a pass, confirmation early exit, later rule failure, unavailable repository and invalid invocation. A sixth case is an explicitly injected crash-output control (exit 2 with partial output), not a checker defect or runtime observation. Case labels in packets are neutral; the separate answer key identifies construction and expected outcomes. The fixture source and answer key are withheld from consumer agents. No private conversation data or external model is used during collection.

Packets contain `arm`, `instructions`, optional `guidance`, and `cases[]` with `case_id`, `exit_code`, `stdout`, `stderr`. They contain no expected answer, fixture name or measured correctness. The neutral question asks for intake readiness, observed blockers, whether applicable checks completed and whether recovery/rerun is needed. Completeness means only this intake path; it never grants downstream workflow authority. The answer key distinguishes underlying outcomes from observable information: justified unknown completeness in the text-only arm is acceptable, not an agent error. For a crash, uncertainty about completion is also acceptable in every arm. A later scorer must preserve those distinctions rather than rewarding guesses.

## Historical candidate replay

The recipe below exercises the withdrawn JSON candidate; it is not a command for the final guidance-only tree. Reproduce it in a separate clone at `7da5d59bbf49f415dc61fbedcaeb6e494bddc006`. The following commands read that historical recipe and change only the temporary output destination, leaving the original packets and committed tester results intact. Choose unused clone/output paths for another replay. `--offline` requires cached locked dependencies; environment setup failures are not product findings.

```sh
git clone --local --no-hardlinks . /private/tmp/loom-intake-json-history-7da5d59
git -C /private/tmp/loom-intake-json-history-7da5d59 checkout --detach 7da5d59bbf49f415dc61fbedcaeb6e494bddc006
cd /private/tmp/loom-intake-json-history-7da5d59
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -c 'from pathlib import Path; p=Path("docs/loom/2026-11-11-intake-observation-pilot/evidence/comparison.md"); code=p.read_text().split("```python\n", 1)[1].split("```", 1)[0]; exec(code.replace("/private/tmp/loom-intake-comparison", "/private/tmp/loom-intake-historical-replay"))'
```

The unchanged historical Python recipe follows for inspection. Its original output destination was `/private/tmp/loom-intake-comparison`; use the substitution above for replay. Fixture content snapshots exclude `.git` here; the candidate's focused read-only test also checked Git bytes. Removal of that candidate test does not rewrite its historical result.

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

Independent agent answers and scoring are retained in [witnessed acceptance evidence](acceptance-test-evidence.md); model-token usage remains unavailable. Output byte counts and one local execution duration cannot establish parent-model call reduction, total latency savings or improved semantic correctness. Guidance-only is now selected because structured output demonstrated no added benefit in this sequential comparison. The parent orchestrator's earlier successful `loom-python --ready intake write-plan 2026-11-11-intake-observation-pilot --json` invocation was candidate self-dogfood, not a current supported command or independent consumption result.
