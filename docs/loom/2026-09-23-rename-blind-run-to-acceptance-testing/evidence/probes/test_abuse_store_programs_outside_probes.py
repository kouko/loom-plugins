"""Adversarial probe: the change's own store holds programs the probe cap refuses.

concern: a change that commits runnable programs in its store outside
`evidence/probes/`, so the checker rule `adversarial.proportionate` refuses the
change at finalize-review and the change cannot be attested as it stands.

The A/B re-run committed `ab/run_ab.py` and `ab/test_run_ab.py` under this
change's store, copying the layout of the 2026-09-14 change, which merged before
the rule refused programs outside `evidence/probes/`. The rule now counts every
program anywhere under `docs/loom/<change-id>/` and refuses one that sits
outside the probes directory. The probe runs that rule itself, unchanged,
against the committed HEAD.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CHANGE_ID = Path(__file__).resolve().parents[2].name
sys.path.insert(0, str(ROOT / "loom-code/scripts"))

from loom_checker.probes import check_adversarial_proportionate  # noqa: E402


def test_proportionate_rule_committed_head_raises_no_refusal() -> None:
    """`adversarial.proportionate` recomputed at HEAD returns no refusal for this change."""
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert check_adversarial_proportionate(ROOT, head, CHANGE_ID) == []
