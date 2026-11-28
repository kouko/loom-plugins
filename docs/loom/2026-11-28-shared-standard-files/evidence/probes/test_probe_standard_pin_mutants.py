"""Adversary probe: hand-written mutation testing of the shared-standard pins.
concern: a moved rule whose polarity flips (a finding becomes not a finding) or a reader pointer that drops, while the change's own pin tests stay green.

The change moves rules out of engineering-baseline.md and lenses.md into
three standards and pins each moved rule with a bare `count(literal) == 1`.
Acceptance 9 says no prohibition became a permission, and the prose-pin rule
(tests-standard.md section 5) says a pin rejects a negated sentence. Each
mutant below copies the real files into a temporary directory, flips ONE
pinned sentence (or drops one reader pointer), points the change's test
modules at the copies, and runs every test in them. A mutant that every test
still passes is a surviving mutant.

The real files are never modified.

Run from the repo root:
    python3 -m pytest docs/loom/2026-11-28-shared-standard-files/evidence/probes/test_probe_standard_pin_mutants.py
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
import types
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    """Walk upward until a directory holding docs/loom and loom-code is found."""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-code").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

TESTS_DIR = ROOT / "loom-code/tests"
FILES = {
    "tests": ROOT / "loom-code/references/tests-standard.md",
    "code": ROOT / "loom-code/references/code-design-standard.md",
    "docs": ROOT / "loom-code/references/docs-standard.md",
    "baseline": ROOT / "loom-code/references/engineering-baseline.md",
    "lenses": ROOT / "loom-code/skills/closing-review/references/lenses.md",
    "write_plan": ROOT / "loom-code/skills/write-plan/SKILL.md",
}
# Test module -> {module attribute holding a path: FILES key}.
MODULES = {
    "test_tests_standard_text": {"STANDARD": "tests", "BASELINE": "baseline", "LENSES": "lenses"},
    "test_prose_pin_rule_text": {"TESTS_STANDARD_MD": "tests", "BASELINE_MD": "baseline"},
    "test_code_design_standard_text": {
        "STANDARD": "code", "BASELINE": "baseline", "LENSES": "lenses", "WRITE_PLAN": "write_plan",
    },
    "test_docs_standard_text": {"STANDARD": "docs", "BASELINE": "baseline", "LENSES": "lenses"},
}

# (id, FILES key, anchor, replacement). Each anchor occurs exactly once.
MUTANTS = [
    ("tests-s1-cannot-fail-not-a-finding", "tests",
     "it names is a finding — one", "it names is not a finding — one"),
    ("code-s1-length-becomes-a-finding", "code",
     "is a prompt to look, never itself a finding;", "is a prompt to look, and itself a finding;"),
    ("code-s4-three-sites-never-a-candidate", "code",
     "doing the same thing are\nan extraction candidate", "doing the same thing are\nnever an extraction candidate"),
    ("code-s7-shortcut-never-annotated", "code",
     "A shortcut taken on purpose is annotated", "A shortcut taken on purpose is never annotated"),
    ("docs-s1-omission-not-a-finding", "docs",
     "needs and lacks is a finding: a step", "needs and lacks is not a finding: a step"),
    ("docs-s2-unsupported-absolute-not-a-finding", "docs",
     "with no support is a finding, and so\nis a sentence", "with no support is not a finding, and neither\nis a sentence"),
    ("docs-s3-contradiction-not-a-finding", "docs",
     "Two passages contradicting is a finding", "Two passages contradicting is not a finding"),
    ("docs-s5-no-population-not-a-finding", "docs",
     "no denominator or scope is a finding", "no denominator or scope is not a finding"),
    ("docs-s7-unjustified-text-not-a-finding", "docs",
     "otherwise it is a finding, and the finding names", "otherwise it is not a finding, and the finding names"),
    ("baseline-item6-tests-pointer-dropped", "baseline",
     "6. **Test rules live in [`tests-standard.md`](tests-standard.md).** Read it\n"
     "   before writing a test: the reviewer judges every test against it.",
     "6. **Tests.** Write the tests the task needs."),
    ("lenses-tests-row-breach-not-a-finding", "lenses",
     "is judged here, and a breach of it is a finding", "is advisory, and a breach of it is never a finding"),
]


def _load(name: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(f"_probe_{name}", TESTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _mutate(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"mutation anchor must occur exactly once: {old!r}"
    return text.replace(old, new, 1)


def _surviving_modules(tmp: Path, key: str, old: str, new: str) -> list[str]:
    """Names of the test modules reading the mutated file that still pass every test."""
    copies = {}
    for k, path in FILES.items():
        copies[k] = tmp / f"{k}-{path.name}"
        shutil.copy(path, copies[k])
    copies[key].write_text(_mutate(copies[key].read_text(encoding="utf-8"), old, new), encoding="utf-8")
    survivors = []
    for name, attrs in MODULES.items():
        if key not in attrs.values():
            continue
        module = _load(name)
        for attr, k in attrs.items():
            setattr(module, attr, copies[k])
        killed = False
        for test_name in [n for n in dir(module) if n.startswith("test_")]:
            try:
                getattr(module, test_name)()
            except Exception:
                killed = True
                break
        if not killed:
            survivors.append(name)
    return survivors


def test_standardpins_unmutatedfiles_pass(tmp_path: Path) -> None:
    """Control: with a no-op mutation every reading module still passes, so a kill below is real."""
    anchor = "# Tests standard"
    assert _surviving_modules(tmp_path, "tests", anchor, anchor) == [
        "test_tests_standard_text", "test_prose_pin_rule_text",
    ]


def test_standardpins_guardedsentenceflipped_killed(tmp_path: Path) -> None:
    """Control: a flip the change's pins do guard (section 2 "must" to "may") is killed, so the harness sees kills."""
    assert _surviving_modules(
        tmp_path, "tests", "must come from an independent source", "may come from an independent source"
    ) == ["test_prose_pin_rule_text"]


@pytest.mark.parametrize("mutant", MUTANTS, ids=[m[0] for m in MUTANTS])
def test_standardpins_polarityflippedorpointerdropped_killed(tmp_path: Path, mutant) -> None:
    """Every module that reads the mutated file must fail at least one test on the mutant."""
    _id, key, old, new = mutant
    survivors = _surviving_modules(tmp_path, key, old, new)
    reading = [n for n, attrs in MODULES.items() if key in attrs.values()]
    assert len(survivors) < len(reading), f"mutant {_id} survived every module reading it: {survivors}"
