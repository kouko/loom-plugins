# concern: recovery hints must preserve literal shell characters in installed plugin paths.
"""Pin the observed dollar-path replay failure using the existing hook test."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "recovery_hook_tests", ROOT / "loom-code/tests/test_hooks_json.py"
)
hooks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hooks)


@pytest.mark.parametrize("host", ["claude", "codex"])
def test_hint_dollarpath_preservesroot(host, tmp_path):
    """A valid literal dollar in the installed path survives recovery replay."""
    hooks.test_failed_hook_hint_replays_operation_without_launcher_on_path(
        host, "Stop", tmp_path / "literal$cash"
    )
