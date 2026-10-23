# concern: Validating an attestation must not depend on uncommitted working-tree files; the declared package-test command must come from the validated commit.
"""Proposed outcome: validating a generated attestation depends only on the
validated commit's committed content and the attestation, never on the
working tree's current files. An uncommitted edit to
docs/loom/KICKOFF-DEFAULTS.md changes the declared package-test command
that `validate_attestation` compares the recorded package run against."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from loom_checker import digest  # noqa: E402
from loom_checker.attestation import validate_attestation  # noqa: E402

CHANGE = "2026-09-08-example"
MANIFEST = {"publication_only_paths": ["docs/loom/<change-id>/attestation.json"]}
PACKAGE = "python3 -m pytest -q"
PROBE = f"docs/loom/{CHANGE}/evidence/probes/test_probe.py"
KICKOFF = "docs/loom/KICKOFF-DEFAULTS.md"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def _execution(kind: str, command: str, artifact: str) -> dict:
    return {"kind": kind, "command": command, "artifact": artifact, "result": "pass",
            "command_digest": hashlib.sha256(command.encode()).hexdigest()}


def test_validateAttestation_worktreeKickoffDiffers_valid(tmp_path: Path) -> None:
    """An uncommitted KICKOFF-DEFAULTS edit leaves a matching attestation valid."""
    (tmp_path / "docs/loom").mkdir(parents=True)
    (tmp_path / KICKOFF).write_text(f"- package-tests: {PACKAGE} — fixture (2026-09-08)\n",
                                    encoding="utf-8")
    (tmp_path / PROBE).parent.mkdir(parents=True)
    (tmp_path / PROBE).write_text("# concern: fixture\nprint('probe')\n", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "-c", "user.name=Test", "-c", "user.email=test@example.test",
         "commit", "-qm", "fixture")
    sha = _git(tmp_path, "rev-parse", "HEAD")
    attestation = {
        "schema": "loom-attestation/v1", "change_id": CHANGE,
        "content_digest": digest.functional_content_digest(tmp_path, sha, CHANGE, MANIFEST),
        "executions": [_execution("package-tests", PACKAGE, ""),
                       _execution("adversarial", f"python3 {PROBE}", PROBE)],
        "verdicts": [{"reviewer": f"reviewer-{n}", "vendor": "v", "model": "m", "lens": "code",
                      "verdict": "PASS", "findings": []} for n in (1, 2)],
        "findings": [],
    }
    assert validate_attestation(tmp_path, sha, CHANGE, attestation, MANIFEST) == []

    (tmp_path / KICKOFF).write_text("- package-tests: go test ./... — edit (2026-10-23)\n",
                                    encoding="utf-8")

    assert validate_attestation(tmp_path, sha, CHANGE, attestation, MANIFEST) == []
