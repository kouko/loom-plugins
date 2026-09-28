"""Adversarial probes: direct sentence pins the widened census does not see (A1).

concern: a census that reports zero direct sentence pins while test files still assert skill or agent sentences verbatim, because a frontmatter-parsing helper or an installed copy hides the markdown read.
"""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

_CLASSIFIER = Path(__file__).resolve().parents[3] / "2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py"
_SPEC = importlib.util.spec_from_file_location("classify_test_files", _CLASSIFIER)
ctf = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ctf)

# Test file -> the production markdown whose sentences it reads (through a helper the census treats as output).
RESIDUAL = {
    "loom-workflow/tests/distill-sessions/test_prompts_parseable.py": (
        "loom-workflow/skills/distill-sessions/agents/prompt-failure-analysis.md",
        "loom-workflow/skills/distill-sessions/agents/prompt-success-analysis.md",
    ),
    "tests/test_loom_plugin_install_layout.py": ("loom-code/skills/write-plan/SKILL.md",),
}


def _flat(s: str) -> str:
    return " ".join(s.split()).casefold()


def _sentence_literals(test_src: str, prose: str, headings: list[str]) -> list[tuple[int, str]]:
    """Prose literals asserted with `in` that occur verbatim in the markdown body, not only in a heading."""
    hits = []
    for node in ast.walk(ast.parse(test_src)):
        if isinstance(node, ast.Compare) and isinstance(node.ops[0], ast.In) \
                and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
            lit = node.left.value
            if ctf._prose_literal(lit) and _flat(lit) in prose and not any(_flat(lit) in h for h in headings):
                hits.append((node.lineno, lit))
    return hits


def test_census_yaml_frontmatter_helper_flags_pin() -> None:
    """A sentence asserted against a prompt body split off by a yaml-parsing frontmatter helper is a direct pin."""
    src = ('import yaml\nfrom pathlib import Path\nP = Path("skills/x/agents/prompt.md")\n\n'
           'def _split(text):\n    return yaml.safe_load(text.split("---")[1]), text.split("---", 2)[2]\n\n'
           'def test_x():\n    fm, body = _split(P.read_text())\n    assert "never mention ground truth" in body\n')
    assert ctf.direct_pin_lines(src) == [10]


def test_residual_pins_named_files_absent_or_overridden() -> None:
    """Each named file asserts no skill or agent body sentence verbatim, or carries a MANUAL_OVERRIDES row."""
    left = {}
    for test_file, md_files in RESIDUAL.items():
        if test_file in ctf.MANUAL_OVERRIDES:
            continue
        texts = [(ctf.REPO / m).read_text(encoding="utf-8") for m in md_files]
        headings = [_flat(line) for t in texts for line in t.splitlines() if line.lstrip().startswith("#")]
        hits = _sentence_literals((ctf.REPO / test_file).read_text(encoding="utf-8"), _flat(" ".join(texts)), headings)
        if hits:
            left[test_file] = hits
    assert not left, left
