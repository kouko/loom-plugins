# concern: A Rust test target cargo really runs must not be refused because its declared entry omits `path`.
"""A path-less `[[test]] name = "bar"` resolves, in cargo, to
`tests/bar/main.rs` when `tests/bar.rs` does not exist (real `cargo test
--test bar` runs `tests/bar/main.rs`). With its `required-features` listed in
`[features] default`, the graduated probe at `tests/bar/main.rs` is the very
case Acceptance 4 accepts, so `cargo test --test bar` must be a parsed row,
not a hard `not-accepted` refusal."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from loom_checker.attestation import adversarial_route  # noqa: E402

MANIFEST = (
    '[package]\nname = "demo"\nversion = "0.1.0"\nedition = "2021"\n\n'
    '[features]\ndefault = ["a"]\na = []\n\n'
    '[[test]]\nname = "bar"\nrequired-features = ["a"]\n'
)
BARE_MANIFEST = '[package]\nname = "demo"\nversion = "0.1.0"\nautotests = false\n'
ARTIFACT = "tests/bar/main.rs"


def _commit(root: Path, message: str) -> str:
    """Commit everything in a fixture repository; return the new HEAD."""
    if not (root / ".git").exists():
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test",
                    "commit", "-qm", message], cwd=root, check=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                          text=True, capture_output=True).stdout.strip()


def _crate(root: Path, manifest: str) -> None:
    (root / "src").mkdir(exist_ok=True)
    (root / "src/lib.rs").write_text("\n", encoding="utf-8")
    (root / "tests/bar").mkdir(parents=True, exist_ok=True)
    (root / ARTIFACT).write_text("#[test]\nfn bar_main() {}\n", encoding="utf-8")
    (root / "Cargo.toml").write_text(manifest, encoding="utf-8")


def test_cargoRow_declaredDirMainTarget_accepted(tmp_path: Path) -> None:
    """A declared path-less target backed by tests/<name>/main.rs is parsed and collected."""
    _crate(tmp_path, MANIFEST)
    _commit(tmp_path, "fixture")

    route, row = adversarial_route("cargo test --test bar", ARTIFACT, tmp_path)

    assert (route, row and row.name) == ("parsed", "cargo test")


def test_cargoRow_manifestAndTargetFile_readAtValidatedSha(tmp_path: Path) -> None:
    """Cargo.toml and the tests/<name>/main.rs it resolves to come from the
    validated revision, whatever the working tree holds."""
    _crate(tmp_path, MANIFEST)
    validated = _commit(tmp_path, "fixture")
    (tmp_path / "Cargo.toml").write_text(BARE_MANIFEST, encoding="utf-8")
    shutil.rmtree(tmp_path / "tests/bar")
    assert adversarial_route("cargo test --test bar", ARTIFACT, tmp_path)[0] == "parsed"
    _commit(tmp_path, "drop the target")
    assert adversarial_route("cargo nextest run --test bar", ARTIFACT, tmp_path)[0] == "not-accepted"
    assert adversarial_route("cargo nextest run --test bar", ARTIFACT, tmp_path,
                             revision=validated)[0] == "parsed"


def test_cargoRow_targetOnlyInWorktree_refused(tmp_path: Path) -> None:
    (tmp_path / "Cargo.toml").write_text(BARE_MANIFEST, encoding="utf-8")
    _commit(tmp_path, "fixture")
    _crate(tmp_path, MANIFEST)
    assert adversarial_route("cargo test --test bar", ARTIFACT, tmp_path)[0] == "not-accepted"
