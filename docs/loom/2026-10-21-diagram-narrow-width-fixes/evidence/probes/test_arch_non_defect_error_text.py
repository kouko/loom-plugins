# concern: a non-defect input whose trunk error text silently changes (intent Acceptance 4 and Constraint)
"""An arch layer whose structured title is empty and whose body is one cell
wide hits neither named defect: the title is not wider than the layer, and
the body holds no two-cell character. On trunk 114ad1ce it raises
ValueError('max_width must be positive'); Acceptance 4 requires that error
text to stay byte-identical."""

import pathlib
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[5] / "loom-workflow" / "skills" / "loom-visualization" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from gen_arch import render_arch  # noqa: E402


@pytest.mark.parametrize("name", [{"title": "", "body": ["x"]}, "\nx"])
def test_render_arch_empty_title_one_cell_body_keeps_trunk_error(name):
    """The trunk ValueError text is kept for a dict name and a multi-line string name."""
    with pytest.raises(ValueError) as error:
        render_arch([{"name": name, "components": []}])
    assert str(error.value) == "max_width must be positive"
