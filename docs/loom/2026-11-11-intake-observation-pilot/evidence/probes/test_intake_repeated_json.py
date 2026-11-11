# concern: Repeated JSON flags must not become a change id and yield a valid observation.
"""Pin a malformed invocation that was accepted as a blocking observation."""
import importlib.util
import json
from pathlib import Path


def test_intake_repeatedflags_unconfirmed(tmp_path):
    """A duplicate JSON flag without a change id remains an invocation error."""
    root = next(parent for parent in Path(__file__).resolve().parents
                if (parent / "loom-code/tests/test_loom_checker_intake.py").is_file())
    spec = importlib.util.spec_from_file_location(
        "intake_fixtures", root / "loom-code/tests/test_loom_checker_intake.py"
    )
    fixtures = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixtures)
    repo = fixtures.make_repo(tmp_path)
    result = fixtures.run_checker("intake", "write-plan", "--json", "--json", cwd=repo)
    payload = json.loads(result.stdout)
    assert result.returncode == 2
    assert payload["state"] == "unconfirmed"
    assert payload["checks_complete"] is False
    assert payload["failures"] == []
    assert payload["error"]
