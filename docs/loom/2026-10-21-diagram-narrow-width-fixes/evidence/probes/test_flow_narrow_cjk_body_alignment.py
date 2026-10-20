# concern: the wrap_label fix turns a flow hang into a misaligned box at a width budget of zero or less
"""render_flow sizes a box as max(title, min(body, budget)) + 2, so an empty
title with a budget of 0 or less gives a 2-cell interior and wraps the body
at 1 cell. Trunk 114ad1ce looped forever there; with the wrap_label fix the
two-cell character overflows the right border instead. The box must finish
and its borders must line up."""

import json
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[5] / "loom-workflow" / "skills" / "loom-visualization" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from width import display_width  # noqa: E402


def _render_flow_isolated(steps, width):
    code = ("import json, sys; from gen_flow import render_flow; "
            "a = json.loads(sys.argv[1]); print(render_flow(a['steps'], width=a['width']))")
    result = subprocess.run(
        [sys.executable, "-c", code, json.dumps({"steps": steps, "width": width})],
        cwd=SCRIPTS, capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.rstrip("\n")


@pytest.mark.parametrize("width", [0, -1])
@pytest.mark.parametrize("step", [{"title": "", "body": ["中"]}, "\n中"])
def test_render_flow_empty_title_cjk_body_at_nonpositive_width_is_aligned(step, width):
    """Every box line of the rendered flow has the same display width."""
    out = _render_flow_isolated([step], width)
    widths = {display_width(ln) for ln in out.split("\n")}
    assert len(widths) == 1, out
