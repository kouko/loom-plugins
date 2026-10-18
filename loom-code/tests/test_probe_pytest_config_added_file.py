# concern: A pytest probe whose own tests never pass must not borrow another file's passes from config addopts.
"""A config `addopts` positional adds a second test file to the run, so the
summary's `passed` count can come entirely from that file while every test of
the probe is skipped; finalize-review must still refuse the probe."""

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
SKIPPED_PROBE = (
    "# concern: a boundary input the code never rejects\n"
    "import pytest\n"
    "@pytest.mark.skip\n"
    "def test_attack() -> None:\n    assert False\n"
)


def test_pytestProbe_configAddsPassingFile_refused(tmp_path: Path) -> None:
    """Every probe test is skipped; only a config-added file passes, so no attestation."""
    repo = make_repo(tmp_path, "python3 -c pass")
    (repo / PROBE).parent.mkdir(parents=True, exist_ok=True)
    (repo / PROBE).write_text(SKIPPED_PROBE, encoding="utf-8")
    (repo / "pytest.ini").write_text("[pytest]\naddopts = test_other.py\n", encoding="utf-8")
    (repo / "test_other.py").write_text("def test_other() -> None:\n    assert True\n",
                                        encoding="utf-8")
    commit_all(repo, "a config positional adds another passing file")

    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 -m pytest {PROBE}", "artifact": PROBE},
    ]))

    assert result.returncode == 1, result.stdout
    assert "BLOCK finalize.adversarial" in result.stderr
    assert not (repo / f"docs/loom/{CHANGE}/attestation.json").exists()
