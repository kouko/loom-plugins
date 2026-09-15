"""Mutation probes: does the committed package suite notice lane wording coming back?

Run from the repo root:

    python3 -m pytest -q -p no:cacheprovider \
        docs/loom/2026-09-15-second-vendor-without-lanes/evidence/probes/test_suite_mutation_probes.py

Each case extracts committed HEAD into a fresh temp directory, applies one
mutation that breaks intent Acceptance 2 or 3, and runs the change's own
committed test files there (the production assertions, not a copy of them).
The case PASSES when at least one of those tests goes red.

  -k control   mutations the suite catches; these PASS (proves the harness is live)
  -k uncaught  mutations the suite does NOT catch; these FAIL on purpose and
               each is reported as a finding. Do not weaken them.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]

SUITES = {
    "loom-code": [
        "loom-code/scripts/test_contract_manifest.py",
        "loom-code/scripts/test_write_plan_station_text.py",
        "loom-code/scripts/test_second_vendor_policy.py",
    ],
    "loom-design": [
        "loom-design/scripts/spec/test_capture_intent_contract.py",
        "loom-design/scripts/spec/test_write_spec_contract.py",
    ],
}


def extract_head() -> Path:
    root = Path(tempfile.mkdtemp(prefix="svwl-mut-"))
    archive = subprocess.run(["git", "archive", "HEAD"], cwd=REPO, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=BytesIO(archive)) as tar:
        tar.extractall(root, filter="data") if sys.version_info >= (3, 12) else tar.extractall(root)
    return root


def mutate(root: Path, rel: str, pattern: str, repl: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    new, count = re.subn(pattern, repl, text, count=1)
    assert count == 1, f"mutation anchor not found in {rel}: {pattern!r}"
    path.write_text(new, encoding="utf-8")


def suite_failures(root: Path) -> int:
    failed = 0
    for tests in SUITES.values():
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *tests],
            cwd=root, capture_output=True, text=True, check=False,
        )
        assert proc.returncode in (0, 1), proc.stdout[-2000:] + proc.stderr[-2000:]
        failed += proc.returncode
    return failed


def test_mutationHarness_unmutatedHead_suiteGreen() -> None:
    """Baseline: HEAD itself is green, so any red below is caused by the mutation."""
    assert suite_failures(extract_head()) == 0


MUTATIONS = {
    # control: the implementer's scans do cover these files
    "control-writePlanSkillLane": (
        "loom-code/skills/write-plan/SKILL.md",
        r"`second-vendor: ask` question, and required",
        "full-lane `second-vendor: ask` question, and required",
    ),
    "control-captureIntentRefLane": (
        "loom-design/skills/capture-intent/references/second-vendor.md",
        r"pass the accepted CLI or decline directly to Closing\nReview\.",
        "pass the accepted CLI or decline directly to Closing\nReview. In the small lane this opt-in question is not asked.",
    ),
    # uncaught: the contract note this change edited has no lane guard
    "uncaught-manifestNoteFullLane": (
        "loom-code/contract/manifest.yaml",
        r"`ask` blocks once per change;",
        "`ask` blocks once per full-lane change;",
    ),
    # uncaught: an A2-scope file outside the five scanned ones
    "uncaught-closingReviewSkillSmallLane": (
        "loom-code/skills/closing-review/SKILL.md",
        r"The output is the computed reviewer floor:",
        "In the small lane the second-vendor opt-in is not offered. The output is the computed reviewer floor:",
    ),
    # uncaught: the "on every change" pin is negation-blind (Acceptance 3 reversed)
    "uncaught-writePlanRefNegatedEveryChange": (
        "loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md",
        r"`ask` is a standing choice that puts one",
        "`ask` is a standing choice that never puts one",
    ),
    "uncaught-captureIntentRefNegatedEveryChange": (
        "loom-design/skills/capture-intent/references/second-vendor.md",
        r"\*\*`ask`\*\* puts one",
        "**`ask`** does not put one",
    ),
}


@pytest.mark.parametrize("name", list(MUTATIONS))
def test_laneMutation_appliedToHead_packageSuiteGoesRed(name: str) -> None:
    root = extract_head()
    mutate(root, *MUTATIONS[name])
    assert suite_failures(root) > 0, f"mutation {name} survived the committed suite"
