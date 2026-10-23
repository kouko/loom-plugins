# concern: A Go package-form probe must not be accepted when a sibling test file the duplicate scan cannot read (a committed symlink) declares the same test name, so a pass of that name cannot be attributed to the artifact.
"""Acceptance 3: a same-name test in another test file of the artifact's
directory refuses the package form. The scan reads each sibling with
`git show <rev>:<path>`, which for a committed symlink yields the link
target's path, not the Go source that `go test` compiles through it. With
the artifact build-excluded, the sibling alone supplies the `pass` of the
name, so the route must refuse the command before any run is read."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from loom_checker.attestation import adversarial_route  # noqa: E402

COMMAND = "go test -json -count=1 -run '^TestAttack$' ./pkg"
ARTIFACT = "pkg/attack_test.go"
DECLARES = 'package attack\nimport "testing"\nfunc TestAttack(t *testing.T) {}\n'


def _commit(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", "fixture"], cwd=root, check=True)


def test_goPackageRoute_symlinkedSiblingDeclaresName_refused(tmp_path: Path) -> None:
    """A committed symlinked `*_test.go` sibling declaring the same name refuses the route."""
    (tmp_path / "go.mod").write_text("module example.test/attack\n\ngo 1.23\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "shared").mkdir()
    (tmp_path / ARTIFACT).write_text("//go:build never\n\n" + DECLARES, encoding="utf-8")
    (tmp_path / "shared/attack.go.txt").write_text(DECLARES, encoding="utf-8")
    (tmp_path / "pkg/dup_test.go").symlink_to("../shared/attack.go.txt")
    _commit(tmp_path)

    route, _row = adversarial_route(COMMAND, ARTIFACT, tmp_path)

    assert route == "not-accepted"
