"""A graduated Rust probe counts as suite-collected only where plain
`cargo test` (or `cargo nextest run`, which builds the same test targets)
builds it: a root Cargo.toml `[[test]]` target's `path`, or `tests/<name>.rs`
at the repository root when autotests is on."""
# concern: A Rust probe graduated to tests/ must not be refused as uncollected.
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from loom_checker.probes import suite_collection


def make_rust_repo(tmp_path: Path, cargo_toml: str, kickoff: str | None) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    (repo / "Cargo.toml").write_text(cargo_toml, encoding="utf-8")
    if kickoff is not None:
        path = repo / "docs/loom/KICKOFF-DEFAULTS.md"
        path.parent.mkdir(parents=True)
        path.write_text(f"- package-tests: {kickoff} — fixture (2026-10-16)\n", encoding="utf-8")
    for name in ("tests/probe.rs", "tests/a/b.rs", "tests/probe.txt"):
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text("#[test]\nfn t() {}\n", encoding="utf-8")
    return repo


PACKAGE = '[package]\nname = "demo"\nversion = "0.1.0"\n'


@pytest.mark.parametrize("kickoff", [None, "cargo test --release -q", "cargo nextest run --release"],
                         ids=["cargo-tests-dir-collected-marker",
                              "cargo-tests-dir-collected-kickoff",
                              "cargo-tests-dir-collected-nextest"])
def test_cargo_tests_dir_collected(tmp_path: Path, kickoff: str | None) -> None:
    repo = make_rust_repo(tmp_path, PACKAGE, kickoff)
    assert suite_collection(repo, "tests/probe.rs") == (True, "")


@pytest.mark.parametrize("cargo_toml, artifact", [
    (PACKAGE + '[[test]]\nname = "attack"\npath = "tests/a/b.rs"\n', "tests/a/b.rs"),
    (PACKAGE + 'autotests = false\n[[test]]\nname = "probe"\npath = "tests/probe.rs"\n',
     "tests/probe.rs"),
    (PACKAGE + 'autotests = false\n[[test]]\nname = "probe"\n', "tests/probe.rs"),
], ids=["cargo-declared-test-target-collected-outside-autodiscovery",
        "cargo-declared-test-target-collected-autotests-off",
        "cargo-declared-test-target-collected-name-only"])
def test_cargo_declared_test_target_collected(tmp_path: Path, cargo_toml: str, artifact: str) -> None:
    repo = make_rust_repo(tmp_path, cargo_toml, None)
    assert suite_collection(repo, artifact) == (True, "")


@pytest.mark.parametrize("cargo_toml, kickoff, artifact", [
    (PACKAGE + 'autotests = false\n[[test]]\nname = "b"\npath = "tests/a/b.rs"\n', None,
     "tests/probe.rs"),
    (PACKAGE, None, "tests/a/b.rs"),
    (PACKAGE, None, "tests/probe.txt"),
    (PACKAGE, None, "tests/missing.rs"),
    (PACKAGE, "cargo test --manifest-path Cargo.toml", "tests/probe.rs"),
    ('[workspace]\nmembers = ["crates/a"]\n', None, "tests/probe.rs"),
    (PACKAGE, "cargo nextest run --workspace", "tests/probe.rs"),
    (PACKAGE + '[[test]]\nname = "b"\npath = "tests/a/b.rs"\ntest = false\n', None, "tests/a/b.rs"),
    (PACKAGE + '[[test]]\nname = "b"\npath = "tests/a/b.rs"\nrequired-features = ["x"]\n', None,
     "tests/a/b.rs"),
    (PACKAGE + '[[test]]\nname = "probe"\npath = "tests/probe.rs"\ntest = false\n', None,
     "tests/probe.rs"),
], ids=["cargo-autotests-off-or-subdir-refused-autotests",
        "cargo-autotests-off-or-subdir-refused-subdir",
        "cargo-autotests-off-or-subdir-refused-non-rs",
        "cargo-autotests-off-or-subdir-refused-missing",
        "cargo-autotests-off-or-subdir-refused-other-option",
        "cargo-autotests-off-or-subdir-refused-virtual-workspace",
        "cargo-autotests-off-or-subdir-refused-nextest-other-option",
        "cargo-autotests-off-or-subdir-refused-test-false",
        "cargo-autotests-off-or-subdir-refused-required-features",
        "cargo-autotests-off-or-subdir-refused-test-false-overrides-autodiscovery"])
def test_cargo_autotests_off_or_subdir_refused(
    tmp_path: Path, cargo_toml: str, kickoff: str | None, artifact: str
) -> None:
    repo = make_rust_repo(tmp_path, cargo_toml, kickoff)
    assert suite_collection(repo, artifact) == (False, "")


def test_cargo_manifest_parse_error_is_undeterminable(tmp_path: Path) -> None:
    repo = make_rust_repo(tmp_path, "[package\n", None)
    collected, reason = suite_collection(repo, "tests/probe.rs")
    assert collected is None and reason
