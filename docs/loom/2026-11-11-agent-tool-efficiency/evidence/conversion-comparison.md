# Review conversion comparison

Recommendation: **do not add a production adapter in this change**. The temporary
candidate detects ambiguous YAML and absent attribution earlier, but still needs
the same caller-supplied identities and finalization context. This experiment
does not demonstrate fewer agent operations, lower latency, or lower token cost.

Scope: W3-01 / Acceptance 3, following the implemented W1/W2 changes.
The [intent](../../intent/2026-11-11-agent-tool-efficiency.md),
[spec](../spec.md), and [research](../research/01-agent-interface-conventions.md)
bound this experiment. Only public synthetic fixtures are used. No historical
private sessions, outside providers, actual reviewers, production converter,
finalization execution or package-suite execution are involved.

## Contracts and comparison design

[Closing Review](../../../../loom-code/skills/closing-review/SKILL.md) assigns the
orchestrator the YAML-to-temporary-JSON conversion, attribution, findings and
adversarial declarations. There is no existing production data converter.
The baseline below is a retained representative ad hoc recipe: safe-load YAML,
copy fields, attach explicit caller identity, wrap with explicit caller context.

[Finalization](../../../../loom-code/scripts/loom_checker/command_handlers/finalize.py)
accepts a JSON object with verdicts, findings and adversarial lists. Its reviewer
verdict gate accepts PASS or PASS_WITH_NOTES; further checks require distinct
reviewers, outside receipts where selected, executable evidence and acceptance.
A successful transform is not finalization admissibility. Every fixture here has
only one reviewer and no execution evidence, so **none establishes admissibility
of a complete finalization request**.

The candidate additionally uses the existing duplicate-rejecting loader and
reviewer YAML checker from
[reviewers.py](../../../../loom-code/scripts/loom_checker/reviewers.py).
These are private outside-review validation helpers, not a supported converter
API. Their reuse makes this experiment small but brings coupling to that specific
schema. It does not replace receipt, provenance authentication, target-commit,
reviewer independence or complete finalization checks.

The orchestrator's explicit identity is trusted for this comparison; raw reviewer
self-identification is not authoritative. Baseline overwrite of a conflicting raw
identity is therefore a legitimate attribution policy, not demonstrated wrong
attribution. Candidate rejection is a deliberately stricter conflict policy that
costs recovery work. Both retain the exact raw YAML in
[fixtures](conversion-fixtures.json); baseline's attributed JSON loses the
self-reported value, but the retained source still exposes the conflict. Neither
arm invents identity. Both preserve the supplied provenance field verbatim;
that proves preservation only, not authenticity.

## Observations and recovery

| Fixture | Baseline | Candidate | Interpretation / recovery |
|---|---|---|---|
| valid | Converts | Converts | Same JSON and caller-supplied attribution |
| needs_revision | Converts, keeps rejection | Converts, keeps rejection | Transformation-valid; finalizer verdict predicate rejects |
| malformed | Parser failure | Parser failure | Obtain corrected source; never guess YAML |
| duplicate | Last key wins | Rejects | Baseline yields NEEDS_REVISION here; candidate requests unambiguous source |
| missing_identity | Converts without reviewer | Rejects | Supply real dispatch identity; do not generate one |
| identity_conflict | Caller identity replaces raw identity | Rejects | Baseline follows trusted attribution; candidate requires explicit reconciliation |
| malformed_shape | Conversion failure | Explicit shape failure | Obtain a reviewer object |
| raw_identity | Converts | Converts | Matching raw identity and provenance preserved |

No failed verdict is filtered, rewritten to PASS or silently removed.
The duplicate fixture deliberately starts with PASS and ends with NEEDS_REVISION:
the baseline result records the latter, rather than making this experiment look
like it discovered an observed false approval. Duplicate YAML remains ambiguous.
Error classes and original parser diagnostics are retained in
[results](conversion-results.json), alongside every executed command and raw
stdout/stderr. Differing errors are results, not normalized away.

Caller operations, counted as semantic tasks rather than shell syntax:
both arms require (1) capture raw YAML, (2) obtain dispatch identity, (3) assemble
findings/adversarial context, (4) invoke conversion, and (5) inspect errors/output
and preserve the raw-source association before finalization. The candidate
automates extra local checks inside task 4; it does not eliminate any of those
five tasks. After materializing the snippets, each fixture/arm is one Python
invocation. The replay harness is one outer locked uv invocation plus sixteen
child invocations using that same environment. Counts describe this fixture
workflow, not measured model tool calls in a real review session.

Candidate maintenance: see the mechanically recorded function-line counts in the
results; they include blank/comment lines, excluding shared imports and harness.
It adds three identity checks, a raw/caller conflict policy, and dependencies on
two private helpers and their changing reviewer schema. Shared imports, CLI,
fixture handling, error reporting and replay assertions are experiment overhead,
retained below in full. Production integration would additionally need supported
input/output contracts, consumer documentation, tests and version maintenance;
those costs are not estimated as a line count here.

The strict loader/schema checker may improve early error detection. That is
distinct from proving reduced agent work. This bounded candidate also does not
validate all context or caller identity correctness. Keep the production workflow
unchanged; this evidence supports reconsidering a validator only when repeated
real caller work and its integration costs can be measured.

## Exact replay

Run from the repository root. Extract the only Python fence in this document to
a temporary file; then replay under the repository's locked environment:

```sh
python3 -c 'from pathlib import Path; p=Path("docs/loom/2026-11-11-agent-tool-efficiency/evidence/conversion-comparison.md"); Path("/private/tmp/loom-conversion-replay.py").write_text(p.read_text().split("```python\n",1)[1].split("\n```",1)[0]+"\n")'
uv run --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-conversion-replay.py --replay > /private/tmp/loom-conversion-replayed.json
```

The initial run used the second command with stdout redirected to
`docs/loom/2026-11-11-agent-tool-efficiency/evidence/conversion-results.json`.
Individual arm commands are retained per record in that result. Their interpreter
path is environment-specific; the locked replay command resolves it anew.
Python version and PyYAML version are recorded. Result metadata HEAD changes on
later replay; interpreter paths may change with uv cache location. Compare case
outputs, exit codes and assertions rather than requiring byte-identical metadata.

The replay asserts expected conversion success/failure for all sixteen runs,
explicitly preserves rejected verdicts, and checks context/provenance retention.
Its finalizer predicate flag models only the passing-verdict check directly
visible in finalize.py; it is not a gate result. This is evidence replay, not
production code or a new package test.

```python
import argparse
import json
from pathlib import Path
import subprocess
import sys
import yaml

ROOT = Path.cwd()
STORE = ROOT / "docs/loom/2026-11-11-agent-tool-efficiency/evidence"
sys.path.insert(0, str(ROOT / "loom-code/scripts"))
from loom_checker.reviewers import _UniqueKeyLoader, _review_yaml_failure


def baseline(case):
    # Representative ad hoc conversion, not an existing production converter.
    parsed = yaml.safe_load(case["raw_yaml"])
    attributed = dict(parsed)
    attributed.update(case["identity"])
    return dict(case["context"], verdicts=[attributed])


def candidate(case):
    parsed = yaml.load(case["raw_yaml"], Loader=_UniqueKeyLoader)
    if not isinstance(parsed, dict):
        raise ValueError("review must be an object")
    identity = case["identity"]
    for key in ("reviewer", "vendor", "model"):
        if not isinstance(identity.get(key), str) or not identity[key].strip():
            raise ValueError("missing caller identity: " + key)
        if key in parsed and parsed[key] != identity[key]:
            raise ValueError("raw/caller identity conflict: " + key)
    attributed = dict(parsed, **identity)
    failure = _review_yaml_failure(parsed, attributed)
    if failure:
        raise ValueError(failure)
    return dict(case["context"], verdicts=[attributed])


def run_arm(arm, case):
    try:
        output = globals()[arm](case)
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, TypeError, yaml.YAMLError) as error:
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        return 1


def replay():
    fixture = json.loads((STORE / "conversion-fixtures.json").read_text())
    records = []
    for case in fixture["cases"]:
        for arm in ("baseline", "candidate"):
            command = [sys.executable, __file__, "--arm", arm, "--case", case["id"]]
            process = subprocess.run(command, text=True, capture_output=True)
            output = json.loads(process.stdout) if process.returncode == 0 else None
            assert (process.returncode == 0) == case["expected"][arm + "_ok"]
            if output is not None:
                assert output["findings"] == case["context"]["findings"]
                assert output["adversarial"] == case["context"]["adversarial"]
                assert output["verdicts"][0]["provenance"] == {
                    "source": "public-synthetic-fixture"}
                if case["id"] == "needs_revision":
                    assert output["verdicts"][0]["verdict"] == "NEEDS_REVISION"
            # This is only finalize.py's passing-verdict predicate.
            # It is NOT invocation of finalize-review or an attestation claim.
            passing = (output is not None and all(
                v.get("verdict") in {"PASS", "PASS_WITH_NOTES"}
                for v in output["verdicts"]))
            records.append({
                "case": case["id"], "arm": arm, "command": command,
                "exit_code": process.returncode, "stdout": process.stdout,
                "stderr": process.stderr,
                "passes_finalizer_verdict_predicate_only": passing,
            })
    source = Path(__file__).read_text()
    def lines(start, end):
        return len(source.split(start, 1)[1].split(end, 1)[0].strip().splitlines()) + 1
    result = {
        "source_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True).strip(),
        "python": sys.version, "pyyaml": yaml.__version__,
        "replay_command": "uv run --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-conversion-replay.py --replay",
        "scope": "Transformation only. No finalization, external providers or suite.",
        "footprint_function_lines_including_blank_and_comment": {
            "baseline": lines("def baseline(case):", "def candidate(case):"),
            "candidate": lines("def candidate(case):", "def run_arm(arm, case):"),
        },
        "results": records,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


parser = argparse.ArgumentParser()
parser.add_argument("--replay", action="store_true")
parser.add_argument("--arm", choices=("baseline", "candidate"))
parser.add_argument("--case")
args = parser.parse_args()
if args.replay:
    replay()
else:
    cases = json.loads((STORE / "conversion-fixtures.json").read_text())["cases"]
    selected = next(case for case in cases if case["id"] == args.case)
    raise SystemExit(run_arm(args.arm, selected))
```
