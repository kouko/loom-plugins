# concern: A package test in another file must not satisfy a commented declaration in the artifact.
"""A selected Go file with only a comment must not own another file's test."""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code/scripts"))

from loom_checker.attestation import adversarial_route


def test_go_commented_declaration_refuses_other_file_pass(tmp_path: Path) -> None:
    """Refuse a pass when the artifact's apparent test is only a comment."""
    repo = tmp_path / "go"
    repo.mkdir()
    (repo / "go.mod").write_text("module example.test/attack\n\ngo 1.23\n")
    artifact = "attack_test.go"
    (repo / artifact).write_text(
        'package attack\n/*\nfunc TestAttack(t *testing.T) {}\n*/\n'
    )
    (repo / "other_test.go").write_text(
        'package attack\nimport "testing"\nfunc/**/TestAttack(t *testing.T) {}\n'
    )
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
         "commit", "-qm", "fixture"], cwd=repo, check=True,
    )
    command = "go test -json -count=1 -run '^TestAttack$' ."
    run = subprocess.run(shlex.split(command), cwd=repo, text=True, capture_output=True)
    assert run.returncode == 0, run.stderr
    route, row = adversarial_route(command, artifact, repo)
    assert route != "parsed" or row is None or row.passed(run.stdout, artifact) == 0
