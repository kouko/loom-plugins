"""Adversarial probe: the rename guard misses near-miss spellings of the retired name.

concern: a retired-name guard that matches only the hyphen and space spellings on
one line lets the old step name return in a YAML key, a Python identifier, a
hard-wrapped Markdown sentence, or the Chinese term the repo used before.

Target: `retired_step_names` in `loom-code/scripts/test_legacy_contract_removed.py`,
the guard this change adds so the retired step name cannot come back into the
runtime trees. Its own comment says it covers the name "in its id, agent and
prose forms". The probe feeds it the input it was written to catch, then the
same input one character different:

* `_` instead of `-` -- the identifier form a YAML key or a Python name takes;
* a line break instead of the space -- every station file is hard-wrapped, so
  the prose form lands split across two lines as often as on one;
* the Chinese term AGENTS.md used for this step before the change (a runtime
  file the guard scans).

The retired spellings are assembled from pieces so that this file, once
graduated into a runtime tree, does not trip the guard itself.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
GUARD = ROOT / "loom-code/scripts/test_legacy_contract_removed.py"

_spec = importlib.util.spec_from_file_location("rename_guard_under_attack", GUARD)
_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_guard)

OLD = "blind"


def test_rename_guard_hyphen_form_is_flagged() -> None:
    """Control: the spelling the guard was written for is reported."""
    assert _guard.retired_step_names("x.md", f"skip {OLD}-run") == ["x.md:1"]


def test_rename_guard_underscore_form_is_flagged() -> None:
    """The identifier form (`<old>_run_report:` as a YAML key) is reported."""
    text = f"{OLD}_run_report: docs/loom/<change-id>/report.md"
    assert _guard.retired_step_names("x.yaml", text) == ["x.yaml:1"]


def test_rename_guard_wrapped_prose_form_is_flagged() -> None:
    """The prose form split by a hard wrap is reported on one of its lines."""
    text = f"When a {OLD}\nrun is needed, finish it and commit its report."
    assert _guard.retired_step_names("x.md", text) != []


def test_rename_guard_chinese_form_is_flagged() -> None:
    """The Chinese term AGENTS.md used for the step before this change is reported."""
    text = "三個人類決策點：③" + "盲" + "跑報告驗收"
    assert _guard.retired_step_names("AGENTS.md", text) == ["AGENTS.md:1"]
