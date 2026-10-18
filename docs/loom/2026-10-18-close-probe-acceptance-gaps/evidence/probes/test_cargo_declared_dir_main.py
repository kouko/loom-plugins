# concern: A Rust test target cargo really runs must not be refused because its declared entry omits `path`.
"""A path-less `[[test]] name = "bar"` resolves, in cargo, to
`tests/bar/main.rs` when `tests/bar.rs` does not exist (real `cargo test
--test bar` runs `tests/bar/main.rs`). With its `required-features` listed in
`[features] default`, the graduated probe at `tests/bar/main.rs` is the very
case Acceptance 4 accepts, so `cargo test --test bar` must be a parsed row,
not a hard `not-accepted` refusal."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from loom_checker.attestation import adversarial_route  # noqa: E402

MANIFEST = (
    '[package]\nname = "demo"\nversion = "0.1.0"\nedition = "2021"\n\n'
    '[features]\ndefault = ["a"]\na = []\n\n'
    '[[test]]\nname = "bar"\nrequired-features = ["a"]\n'
)
ARTIFACT = "tests/bar/main.rs"


def test_cargoRow_declaredDirMainTarget_accepted(tmp_path: Path) -> None:
    """A declared path-less target backed by tests/<name>/main.rs is parsed and collected."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src/lib.rs").write_text("\n", encoding="utf-8")
    (tmp_path / "tests/bar").mkdir(parents=True)
    (tmp_path / ARTIFACT).write_text("#[test]\nfn bar_main() {}\n", encoding="utf-8")
    (tmp_path / "Cargo.toml").write_text(MANIFEST, encoding="utf-8")

    route, row = adversarial_route("cargo test --test bar", ARTIFACT, tmp_path)

    assert (route, row and row.name) == ("parsed", "cargo test")
