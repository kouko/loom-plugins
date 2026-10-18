"""A probe that defines pytest-style tests must be run with `python -m pytest`:
a bare `python3 <probe>` imports it and exits 0 without calling one test, so
finalize-review refuses that run. Attestations already written are not
re-judged, so the validator keeps accepting them."""
# concern: A pytest-style probe run as a bare script must not be attested as passing.
from __future__ import annotations

import sys
from pathlib import Path

from loom_checker.attestation import _command_digest

from test_selection_finalize import CHANGE
from test_selection_finalize import PASSING
from test_selection_finalize import commit_all
from test_selection_finalize import finalize
from test_selection_finalize import make_repo
from test_selection_finalize import no_host_session  # noqa: F401
from test_selection_finalize import review_input
from test_selection_finalize import validate
from test_selection_finalize import written

PROBE = f"docs/loom/{CHANGE}/evidence/probes/probe_attack.py"
HEAD = "# concern: a boundary input the code never rejects\n"


def commit_probe(repo: Path, source: str) -> None:
    (repo / PROBE).parent.mkdir(parents=True, exist_ok=True)
    (repo / PROBE).write_text(HEAD + source, encoding="utf-8")
    commit_all(repo, "probe")


def test_plain_script_probe_run_directly_is_accepted(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    commit_probe(repo, "assert 1 + 1 == 2\n")

    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 {PROBE}", "artifact": PROBE}]))

    assert result.returncode == 0, result.stderr


def test_test_function_probe_run_directly_is_refused(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    commit_probe(repo, "def test_x() -> None:\n    assert True\n")

    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 {PROBE}", "artifact": PROBE}]))

    assert result.returncode == 1
    assert f"python -m pytest {PROBE}" in result.stderr
    assert not (repo / f"docs/loom/{CHANGE}/attestation.json").exists()


def test_existing_direct_run_of_test_function_probe_still_validates(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    commit_probe(repo, "def test_x() -> None:\n    assert True\n")
    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"{sys.executable} -m pytest {PROBE}", "artifact": PROBE}]))
    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    direct = f"python3 {PROBE}"
    for run in attestation["executions"]:
        if run["kind"] == "adversarial":
            run.update(command=direct, command_digest=_command_digest(direct))

    assert validate(repo, attestation) == []
