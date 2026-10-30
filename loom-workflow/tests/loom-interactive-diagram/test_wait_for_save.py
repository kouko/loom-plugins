"""A bounded wait observes content changes to one diagram file."""

import select
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/wait_for_save.py"


def line_from(process):
    readable, _, _ = select.select([process.stdout], [], [], 2)
    assert readable, "waiter did not report promptly"
    return process.stdout.readline().strip()


def start_wait(path, timeout="0.3"):
    process = subprocess.Popen(
        [sys.executable, str(SCRIPT), str(path), "--timeout", timeout, "--interval", "0.02"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return process


@pytest.mark.parametrize("atomic", [False, True])
def test_changed_save_reports_after_ready(tmp_path, atomic):
    diagram = tmp_path / "flow.drawio"
    diagram.write_text("before")
    process = start_wait(diagram)
    try:
        assert line_from(process) == "READY"
        if atomic:
            replacement = tmp_path / "replacement.tmp"
            replacement.write_text("after")
            replacement.replace(diagram)
        else:
            diagram.write_text("after")
        assert line_from(process) == "CHANGED"
        assert process.wait(timeout=2) == 0
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()


def test_unchanged_save_and_unrelated_sibling_time_out(tmp_path):
    diagram = tmp_path / "flow.drawio"
    sibling = tmp_path / "other.drawio"
    diagram.write_text("before")
    process = start_wait(diagram)
    try:
        assert line_from(process) == "READY"
        diagram.touch()
        diagram.write_text("before")
        sibling.write_text("changed")
        assert line_from(process) == "TIMEOUT"
        assert process.wait(timeout=2) == 1
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()


def test_missing_diagram_is_named(tmp_path):
    diagram = tmp_path / "missing.drawio"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(diagram), "--timeout", "0.1"],
        text=True, capture_output=True, timeout=2,
    )
    assert result.returncode != 0
    assert str(diagram) in result.stderr


def test_disappearing_diagram_is_named(tmp_path):
    diagram = tmp_path / "flow.drawio"
    diagram.write_text("before")
    process = start_wait(diagram)
    try:
        assert line_from(process) == "READY"
        diagram.unlink()
        assert process.wait(timeout=2) != 0
        assert str(diagram) in process.stderr.read()
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()


def test_unreadable_diagram_is_named(tmp_path):
    diagram = tmp_path / "flow.drawio"
    diagram.mkdir()
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(diagram), "--timeout", "0.1"],
        text=True, capture_output=True, timeout=2,
    )
    assert result.returncode != 0
    assert str(diagram) in result.stderr
