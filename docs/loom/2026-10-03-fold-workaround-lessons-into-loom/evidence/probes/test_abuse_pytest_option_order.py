"""Adversary probe for the pytest option-order relaxation in
`loom_checker.probes.command_executes_artifact`.

concern: a probe command whose option values are mistaken for the test
file -- a valued pytest option before the file is refused, and an option
value naming the artifact lets a different program run in its place.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))

from loom_checker import probes  # noqa: E402

ARTIFACT = "tests/probe.py"


def test_command_executes_artifact_valued_option_before_file_accepted() -> None:
    """A real runner option with a value before the file still runs the file."""
    assert probes.command_executes_artifact(
        "python3 -m pytest -p no:cacheprovider tests/probe.py", ARTIFACT
    )


@pytest.mark.parametrize("command", [
    "python3 -m pytest --deselect tests/probe.py tests/other.py",
    "python3 -m pytest --ignore tests/probe.py tests/other.py",
])
def test_command_executes_artifact_value_names_artifact_refused(command: str) -> None:
    """An option value that names the artifact while another file runs is refused."""
    assert not probes.command_executes_artifact(command, ARTIFACT)
