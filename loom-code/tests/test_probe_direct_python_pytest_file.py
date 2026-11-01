# concern: A pytest-style probe run as a bare script runs no test and must not be attested as passing.
"""`python3 <probe>` on a file that only defines pytest test functions imports
the module and exits 0 without calling any of them -- here a test that always
fails. finalize-review must not attest that run as the probe's pass."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "loom-code/scripts"))
sys.path.insert(0, str(REPO / "loom-code/tests"))

from test_selection_finalize import CHANGE  # noqa: E402
from test_selection_finalize import PASSING  # noqa: E402
from test_selection_finalize import commit_all  # noqa: E402
from test_selection_finalize import finalize  # noqa: E402
from test_selection_finalize import make_repo  # noqa: E402
from test_selection_finalize import no_host_session  # noqa: E402,F401
from test_selection_finalize import review_input  # noqa: E402

PROBE = f"docs/loom/{CHANGE}/evidence/probes/test_attack.py"
FAILING_PROBE = (
    "# concern: a boundary input the code never rejects\n"
    "def test_attack() -> None:\n    assert False\n"
)


def test_directPython_pytestStyleProbe_refused(tmp_path: Path) -> None:
    """A bare `python3` run of a failing pytest-style probe yields no attestation."""
    repo = make_repo(tmp_path, "python3 -c pass")
    (repo / PROBE).parent.mkdir(parents=True, exist_ok=True)
    (repo / PROBE).write_text(FAILING_PROBE, encoding="utf-8")
    commit_all(repo, "a pytest-style probe")

    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 {PROBE}", "artifact": PROBE},
    ]))

    assert result.returncode == 1, result.stdout
    assert not (repo / f"docs/loom/{CHANGE}/attestation.json").exists()
