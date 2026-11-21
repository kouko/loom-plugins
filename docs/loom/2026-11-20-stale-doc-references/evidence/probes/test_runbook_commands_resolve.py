# concern: a runnable command in a living runbook names a script path, presented as current, that does not resolve from the repository the runbook lives in
"""Adversary probe for Acceptance 1 of 2026-11-20-stale-doc-references.

Every `python3 <path>.py` line inside a fenced bash block of the listed
living docs must name a file that exists in this repository, unless the
same block marks the command historical. A command that only works from
another repository (for example a plugin shipped elsewhere) is not a
current reference here.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]

DOCS = [
    "loom-workflow/docs/quarterly-audit-runbook.md",
    "loom-workflow/docs/skill-governance.md",
    "loom-workflow/docs/telemetry-setup.md",
]

FENCE = re.compile(r"```bash\n(.*?)```", re.S)
CMD = re.compile(r"^\s*python3\s+([\w./-]+\.py)\b", re.M)


def _unresolved(text, exists=lambda p: (ROOT / p).is_file()):
    misses = []
    for block in FENCE.findall(text):
        if re.search(r"#[^\n]*\bhistorical\b", block, re.I):
            continue
        for path in CMD.findall(block):
            if not exists(path):
                misses.append(path)
    return misses


def test_runbook_python_commands_resolve_in_repo():
    """Each current python3 command in a living runbook names an existing repo file."""
    misses = []
    for rel in DOCS:
        for path in _unresolved((ROOT / rel).read_text(encoding="utf-8")):
            misses.append(f"{rel}: {path}")
    assert not misses, "unresolved runnable paths:\n" + "\n".join(misses)


def test_unresolved_historical_block_skipped():
    """Synthetic: a missing path is reported unless its block says historical."""
    live = "```bash\npython3 gone/tool.py run\n```\n"
    old = "```bash\n# historical: removed\npython3 gone/tool.py run\n```\n"
    assert _unresolved(live, exists=lambda p: False) == ["gone/tool.py"]
    assert _unresolved(old, exists=lambda p: False) == []
