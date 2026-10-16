"""Go, Node and Rust adversarial probe commands are recognized by
`command_names_artifact` and `command_executes_artifact`, the predicates
finalize-review and the attestation validator share; a command that names
the file but would not run it stays refused, and Python/shell is unchanged.
"""
from __future__ import annotations

import pytest

from loom_checker.probes import command_executes_artifact
from loom_checker.probes import command_names_artifact

GO = "docs/loom/x/evidence/probes/add_test.go"
JS = "docs/loom/x/evidence/probes/attack.test.ts"
RUST = "tests/attack.rs"


def accepted(command: str, artifact: str) -> bool:
    return command_names_artifact(command, artifact) and command_executes_artifact(command, artifact)


@pytest.mark.parametrize("command", [
    f"go test {GO}",
    f"go test -v -race -count 1 -timeout 30s -tags integration {GO}",
    f"go test -count=1 -timeout=30s -tags=integration {GO} docs/loom/x/evidence/probes/helper_test.go",
])
def test_go_test_file_list_accepted(command: str) -> None:
    assert accepted(command, GO)


@pytest.mark.parametrize("command", [
    f"go vet {GO}",
    f"go build {GO}",
    f"go test -run TestNothing {GO}",
    f"go test -list . {GO}",
    f"go test -c {GO}",
    f"go test -n {GO}",
    f"go test -vet=off {GO}",
    f"go test ./... {GO}",
    f"go test -count {GO}",
])
def test_go_vet_or_run_filter_refused(command: str) -> None:
    assert not accepted(command, GO)


@pytest.mark.parametrize(("command", "artifact"), [
    (f"node {JS}", JS),
    (f"node --test {JS}", JS),
    (f"node --test --experimental-strip-types {JS}", JS),
    ("node --experimental-strip-types docs/p/a.mjs", "docs/p/a.mjs"),
    ("node docs/p/a.cjs", "docs/p/a.cjs"),
    (f"npx vitest run {JS}", JS),
    ("npx jest docs/p/a.test.js", "docs/p/a.test.js"),
    (f"cargo test --test attack", RUST),
    (f"cargo test --release -q --test=attack", RUST),
    (f"cargo test --quiet --test attack", RUST),
])
def test_node_vitest_jest_cargo_accepted(command: str, artifact: str) -> None:
    assert accepted(command, artifact)


@pytest.mark.parametrize("command", [
    "cargo test --test attack some_case",
    "cargo test --test attack -- --ignored",
    "cargo test --no-run --test attack",
    "cargo test --test other",
    "cargo test --test attack --test attack",
    "cargo build --test attack",
])
def test_cargo_name_filter_refused(command: str) -> None:
    assert not accepted(command, RUST)


@pytest.mark.parametrize("command", [
    f"npx vitest list {JS}",
    f"npx jest --config {JS}",
    f"npx jest --listTests {JS}",
    f"node --check {JS}",
    f"node docs/p/other.js {JS}",
    f"npx vitest run docs/p/other.ts {JS}",
])
def test_vitest_list_or_jest_config_refused(command: str) -> None:
    assert not accepted(command, JS)


@pytest.mark.parametrize(("command", "artifact"), [
    (f"go test -exec true {GO}", GO),
    (f"node --test --watch {JS}", JS),
    (f"npx vitest run --passWithNoTests {JS}", JS),
    (f"npx jest --ci {JS}", JS),
    ("cargo test --doc --test attack", RUST),
])
def test_unlisted_flag_refused(command: str, artifact: str) -> None:
    assert not accepted(command, artifact)


@pytest.mark.parametrize(("command", "artifact"), [
    ("python3 tests/probe.py", "tests/probe.py"),
    ("python3 -m pytest -q tests/probe.py", "tests/probe.py"),
    ("bash tests/probe.sh", "tests/probe.sh"),
    ("./tests/probe", "tests/probe"),
])
def test_python_shell_unchanged(command: str, artifact: str) -> None:
    assert accepted(command, artifact)


@pytest.mark.parametrize("command", [
    "python3 noop.py  # tests/probe.py",
    "true tests/probe.py",
    "python3 -m pytest --ignore tests/probe.py tests/other.py",
    "go test tests/probe.py",
])
def test_python_noop_refused(command: str) -> None:
    assert not accepted(command, "tests/probe.py")
