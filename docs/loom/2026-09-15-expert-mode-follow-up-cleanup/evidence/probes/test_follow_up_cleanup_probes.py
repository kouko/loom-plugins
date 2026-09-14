"""Adversarial probes for the expert-mode follow-up cleanup change.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-15-expert-mode-follow-up-cleanup/evidence/probes/test_follow_up_cleanup_probes.py -q

Every probe is an attempt to make the change fail. Attempts the change
survives PASS; attempts that expose a defect FAIL on purpose and must not be
weakened. The defect probes are the three named in the module constant
DEFECT_PROBES below.

Host session variables are removed for every probe, and subprocesses get an
explicit environment, so results match inside and outside Claude Code.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = REPO_ROOT / "loom-code" / "scripts"
assert (SCRIPTS / "loom_checker" / "selection.py").is_file(), SCRIPTS
sys.path.insert(0, str(SCRIPTS))

from loom_checker import attestation as att  # noqa: E402
from loom_checker import selection  # noqa: E402

CHECKER = SCRIPTS / "loom_checker.py"
MANIFEST = REPO_ROOT / "loom-code" / "contract" / "manifest.yaml"
SKILL = REPO_ROOT / "loom-code" / "skills" / "expert-mode" / "SKILL.md"
PRINCIPLES = REPO_ROOT / "PRINCIPLES.md"
BASE = "aa0cffff"
CHANGE = "2026-09-15-probe"
HOST_ENV = ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT")
FULL = ["spec", "plan", "implementer", "tdd", "reviewers",
        "adversarial", "blind-run", "package-tests"]
DEFECT_PROBES = (
    "test_root_readme_loom_code_section_version_equals_manifest",
    "test_expert_mode_skill_dependency_prose_absent",
    "test_principles_pin_indented_pending_line_rejected",
)


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    """Probes never inherit the real Claude Code session running the suite."""
    for name in HOST_ENV:
        monkeypatch.delenv(name, raising=False)


def clean_env(**extra: str) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in HOST_ENV}
    env.update(extra)
    return env


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          text=True, check=True, env=clean_env()).stdout.strip()


def base_file(path: str) -> str:
    result = subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"{BASE}:{path}"],
                            capture_output=True, text=True, env=clean_env())
    if result.returncode != 0:
        pytest.skip(f"base commit {BASE} is not available in this clone")
    return result.stdout


def commit(repo: Path, name: str) -> None:
    (repo / name).write_text(name, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", name)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    commit(repo, "base.txt")
    git(repo, "checkout", "-q", "-b", "feature")
    commit(repo, "work.txt")
    return repo


def checker(repo: Path, *args: str, stdin: str = "", **env: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), "selection", *args],
                          capture_output=True, text=True, cwd=str(repo), input=stdin,
                          env=clean_env(**env))


def capture(repo: Path, prompt: str, session: str, prompt_id: str) -> subprocess.CompletedProcess:
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": prompt,
               "session_id": session, "prompt_id": prompt_id}
    return checker(repo, "capture", "--hook", stdin=json.dumps(payload),
                   CLAUDE_CODE_SESSION_ID=session)


def old_selection_module(tmp_path: Path):
    """The base commit's selection.py, which still reads `requires`."""
    source = tmp_path / "old_selection.py"
    source.write_text(base_file("loom-code/scripts/loom_checker/selection.py"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("old_selection", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- selection refusals survive the removed dependency loop -----------------

HOSTILE = [
    pytest.param(["--skip", "Spec"], id="case-variant"),
    pytest.param(["--skip", "INTENT"], id="intent-uppercase"),
    pytest.param(["--skip", "intent"], id="intent"),
    pytest.param(["--run", "intent"], id="run-intent"),
    pytest.param(["--skip", "spec,intent"], id="intent-with-valid"),
    pytest.param(["--skip", "spec​"], id="zero-width-space"),
    pytest.param(["--skip", "ｓｐｅｃ"], id="fullwidth"),
    pytest.param(["--skip", "../spec"], id="traversal"),
    pytest.param(["--skip", "spec;rm -rf /"], id="injection"),
    pytest.param(["--skip", "tdd", "--run", "tdd"], id="run-skip-overlap"),
    pytest.param(["--skip", "requires"], id="removed-field-name"),
]


@pytest.mark.parametrize("args", HOSTILE)
def test_selection_propose_hostile_name_refused(repo: Path, args: list[str]) -> None:
    """A name outside the vocabulary, the intent, or a run/skip overlap is
    refused with exit 2 and records nothing, after `requires` removal."""
    result = checker(repo, "propose", CHANGE, "--origin", "user", *args)
    assert result.returncode == 2, (result.returncode, result.stdout, result.stderr)
    assert "refused" in result.stderr
    assert selection.read_events(repo, CHANGE) == []


def test_selection_propose_whitespace_duplicates_normalised(repo: Path) -> None:
    """Padded and repeated valid names bind one skip, in manifest order."""
    result = checker(repo, "propose", CHANGE, "--origin", "user",
                     "--skip", " tdd , spec ", "--skip", "spec,,tdd")
    assert result.returncode == 0, result.stderr
    proposal = selection.read_events(repo, CHANGE)[-1]
    assert proposal["skip"] == ["spec", "tdd"]
    assert proposal["run"] == [n for n in FULL if n not in ("spec", "tdd")]


def test_validate_selection_every_subset_equals_base(tmp_path: Path) -> None:
    """On the shipped manifest, the new validator refuses exactly what the base
    validator refused, for all 256 skip subsets plus hostile extras."""
    old = old_selection_module(tmp_path)
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    cases = [list(c) for r in range(len(FULL) + 1) for c in itertools.combinations(FULL, r)]
    extras = [["intent"], ["Spec"], [""], ["spec", "spec"], [None]]
    for skip in cases + extras:
        for run in ([], ["plan"], ["intent"]):
            assert selection.validate_selection(skip, run, manifest) == \
                old.validate_selection(skip, run, manifest), (skip, run)


def test_step_vocabulary_legacy_requires_manifest_same_names() -> None:
    """A manifest that still carries `requires` (older install) loads the same
    names in the same order, without error."""
    legacy = yaml.safe_load(base_file("loom-code/contract/manifest.yaml"))
    assert all("requires" in s for s in legacy["step_selection"]["steps"])
    current = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert [s["name"] for s in selection.step_vocabulary(legacy)] == FULL
    assert selection.step_vocabulary(current) == [{"name": n} for n in FULL]


def test_step_vocabulary_old_checker_new_manifest_reads_no_dependencies(tmp_path: Path) -> None:
    """An older checker reading the new manifest sees every step with no
    dependency, so a mixed install refuses nothing new."""
    old = old_selection_module(tmp_path)
    current = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert old.step_vocabulary(current) == [{"name": n, "requires": []} for n in FULL]
    assert old.validate_selection(FULL, [], current) == []


def test_step_names_skill_manifest_attestation_same_order(repo: Path) -> None:
    """SKILL.md §1, the manifest and the attestation read one vocabulary."""
    text = " ".join(SKILL.read_text(encoding="utf-8").split())
    listed = re.search(r"Steps: (.*?)\. The intent", text)
    assert listed, "SKILL.md step list missing"
    assert re.findall(r"`([a-z-]+)`", listed.group(1)) == FULL
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert [s["name"] for s in manifest["step_selection"]["steps"]] == FULL
    assert "intent" not in [s["name"] for s in selection.step_vocabulary(manifest)]


# --- the session sentence against the code -----------------------------------

def _bound(repo: Path, session: str) -> dict:
    result = checker(repo, "show", CHANGE, CLAUDE_CODE_SESSION_ID=session)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_session_new_session_old_code_binds_nothing(repo: Path) -> None:
    """A confirmation from session A does not apply in session B, and typing
    the old code again in B records nothing."""
    result = checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "reviewers",
                     CLAUDE_CODE_SESSION_ID="sess-A")
    assert result.returncode == 0, result.stderr
    code = selection.read_events(repo, CHANGE)[-1]["code"]
    capture(repo, f"/loom-code:expert-mode {code}", "sess-A", "p1")
    assert _bound(repo, "sess-A")["bound"] is True
    assert _bound(repo, "sess-B")["bound"] is False
    before = len(selection.read_events(repo, CHANGE))
    capture(repo, f"/loom-code:expert-mode {code}", "sess-B", "p2")
    assert len(selection.read_events(repo, CHANGE)) == before
    assert _bound(repo, "sess-B")["bound"] is False


def test_session_new_session_repropose_binds(repo: Path) -> None:
    """Re-running propose in session B and typing the code there binds in B."""
    checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "reviewers",
            CLAUDE_CODE_SESSION_ID="sess-A")
    code = selection.read_events(repo, CHANGE)[-1]["code"]
    capture(repo, f"/loom-code:expert-mode {code}", "sess-A", "p1")
    again = checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "reviewers",
                    CLAUDE_CODE_SESSION_ID="sess-B")
    assert again.returncode == 0, again.stderr
    capture(repo, f"/loom-code:expert-mode {code}", "sess-B", "p2")
    shown = _bound(repo, "sess-B")
    assert shown["bound"] is True and shown["skip"] == ["reviewers"]


def test_session_attestation_evidence_other_session_none(repo: Path, monkeypatch) -> None:
    """Finalization and publication recompute `selection` per session: a
    binding from session A is absent in session B, so an attestation carrying
    it no longer matches there."""
    checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "adversarial",
            CLAUDE_CODE_SESSION_ID="sess-A")
    code = selection.read_events(repo, CHANGE)[-1]["code"]
    capture(repo, f"/loom-code:expert-mode {code}", "sess-A", "p1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-A")
    in_a = att.selection_evidence(repo, CHANGE)
    assert in_a is not None and in_a["skip"] == ["adversarial"]
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "sess-B")
    assert att.selection_evidence(repo, CHANGE) is None


# --- release metadata ----------------------------------------------------------

def test_root_readme_loom_code_section_version_equals_manifest() -> None:
    """DEFECT PROBE. Every README surface naming the loom-code version shows
    the manifest version, including the root README's `## loom-code` prose."""
    version = json.loads((REPO_ROOT / "loom-code/.claude-plugin/plugin.json")
                         .read_text(encoding="utf-8"))["version"]
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    section = text.split("\n## loom-code\n", 1)[1].split("\n## ", 1)[0]
    stated = re.findall(r"Version (\d+\.\d+\.\d+)", section)
    assert stated, "root README loom-code section states no version"
    assert stated == [version], f"README.md ## loom-code says {stated}, manifest {version}"


def test_contract_version_patch_bump_consumers_accept() -> None:
    """The 2.3.1 contract still satisfies loom-design's `requires-contract`."""
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    major, minor, _ = (int(p) for p in str(manifest["version"]).split("."))
    pin = json.loads((REPO_ROOT / "loom-design/.claude-plugin/plugin.json")
                     .read_text(encoding="utf-8"))["requires-contract"]
    need = re.fullmatch(r">=(\d+)\.(\d+)", pin)
    assert need and (major, minor) >= (int(need.group(1)), int(need.group(2)))


# --- stale dependency prose ----------------------------------------------------

DEPENDENCY_PROSE = re.compile(
    r"\b(requires?|needs|depends? on|dependenc(y|ies))\b[^.]*\bstep\b"
    r"|\bstep\b[^.]*\b(requires?|needs|depends? on)\b", re.I)


def _dependency_sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [s for s in re.split(r"(?<=[.:])\s", flat) if DEPENDENCY_PROSE.search(s)]


def test_dependency_detector_affirmative_example_flagged() -> None:
    """Self-test: a sentence saying one step needs another is flagged."""
    assert _dependency_sentences("Name a skip another selected step needs.")


def test_dependency_detector_unrelated_sentence_ignored() -> None:
    """Self-test: a step sentence without a dependency verb is not flagged."""
    assert not _dependency_sentences("Map the user's words onto step names.")


def test_expert_mode_skill_dependency_prose_absent() -> None:
    """DEFECT PROBE. With `requires` gone, SKILL.md must not tell the agent to
    refuse a skip because another selected step needs it (§1)."""
    section = SKILL.read_text(encoding="utf-8").split("## 1.", 1)[1].split("## 2.", 1)[0]
    assert _dependency_sentences(section) == []


# --- PRINCIPLES ratification ----------------------------------------------------

def test_principles_amendment_body_unchanged_since_base() -> None:
    """Only the header changed: the ratified amendment wording is untouched."""
    old = base_file("PRINCIPLES.md").splitlines()
    new = PRINCIPLES.read_text(encoding="utf-8").splitlines()
    strip = lambda lines: [l for l in lines if not l.startswith(("ratified-by:", "pending-ratification:"))]  # noqa: E731
    assert strip(old) == strip(new)


def test_principles_pending_marker_any_spelling_absent() -> None:
    """No pending-ratification marker in any spelling or indentation remains."""
    pattern = re.compile(r"^\s*pending[\s_-]*ratification\s*:", re.I | re.M)
    assert not pattern.search(PRINCIPLES.read_text(encoding="utf-8"))


def _load_ratification_test(principles: Path):
    spec = importlib.util.spec_from_file_location(
        "ratification_pin", REPO_ROOT / "scripts" / "test_principles_ratification.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PRINCIPLES = principles
    return module


@pytest.mark.parametrize("line", ["  pending-ratification: x — awaiting kouko",
                                  "Pending-Ratification: x — awaiting kouko"])
def test_principles_pin_indented_pending_line_rejected(tmp_path: Path, line: str) -> None:
    """DEFECT PROBE. The committed pin must fail on a pending-ratification
    line that is only indented or re-cased; it passes instead."""
    real = PRINCIPLES.read_text(encoding="utf-8").splitlines()
    synthetic = tmp_path / "PRINCIPLES.md"
    synthetic.write_text("\n".join([real[0], real[1], line, *real[2:]]) + "\n", encoding="utf-8")
    module = _load_ratification_test(synthetic)
    with pytest.raises(AssertionError):
        module.test_pending_ratification_line_absent()


def test_principles_pin_exact_pending_line_rejected(tmp_path: Path) -> None:
    """Control: the committed pin does catch the exact base spelling."""
    real = PRINCIPLES.read_text(encoding="utf-8").splitlines()
    synthetic = tmp_path / "PRINCIPLES.md"
    synthetic.write_text("\n".join([real[0], real[1], "pending-ratification: x", *real[2:]]) + "\n",
                         encoding="utf-8")
    module = _load_ratification_test(synthetic)
    with pytest.raises(AssertionError):
        module.test_pending_ratification_line_absent()
