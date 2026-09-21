"""Adversarial probe: a bound user selection wins over narrow-delta auto-skip.

Acceptance 4: a bound user selection determines the effective steps;
automatic classification cannot add to or remove from the steps the user
selected. The attack surface is `effective_selection` on a NARROW delta,
where an implementation that unions the auto-skip into the user's skip (or
intersects it away) would silently override the typed confirmation.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-20-mechanical-calculations/evidence/probes/test_effective_selection_user_precedence.py -q

Every probe is an attempt to make the change fail. Attempts the change
survives PASS; attempts that expose a defect FAIL on purpose and must not be
weakened.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker import selection
from loom_checker.helpers import load_manifest

CHANGE = "2026-09-20-mechanical-calculations"
AUTO_SKIP = {"spec", "plan", "blind-run"}
HOST_ENV = ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT")


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    """Without this, a session the test process does not hold would make every
    recorded confirmation count as out-of-session and every case below would
    pass vacuously."""
    for name in HOST_ENV:
        monkeypatch.delenv(name, raising=False)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def narrow_repo(tmp_path: Path) -> Path:
    """A feature branch whose committed delta is mechanically narrow."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "base.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "base.py")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "switch", "-q", "-c", "feature")
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
    (repo / "test_feature.py").write_text("def test_feature():\n    pass\n", encoding="utf-8")
    git(repo, "add", "docs/guide.md", "test_feature.py")
    git(repo, "commit", "-q", "-m", "narrow files")
    return repo


def step_names() -> list[str]:
    return [s["name"] for s in selection.step_vocabulary(load_manifest())]


def record_bound(repo: Path, skip: list[str], merge_base: str | None = None) -> None:
    """Write an in-scope proposal plus a valid confirmation for `skip`."""
    names = step_names()
    run = [name for name in names if name not in skip]
    branch, current_base = selection.current_scope(repo)
    base = merge_base if merge_base is not None else current_base
    code = selection.selection_code(CHANGE, run, skip)
    proposal_id = uuid.uuid4().hex
    selection.append_event(repo, CHANGE, {
        "event": "proposal", "id": proposal_id, "code": code, "origin": "user",
        "run": run, "skip": skip, "branch": branch, "merge_base": base,
        "session_id": None, "created_at": selection.now(),
    })
    prompt = f"/loom-code:expert-mode OK {code}"
    selection.append_event(repo, CHANGE, {
        "event": "confirmation", "proposal_id": proposal_id, "code": code,
        "source": "user-typed", "session_id": None, "prompt_ref": "probe",
        "prompt_text": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "branch": branch, "merge_base": base, "at": selection.now(),
    })


def effective(repo: Path) -> dict:
    return selection.effective_selection(repo, CHANGE)


def test_effectiveselection_boundfewer_noautoadd(tmp_path: Path) -> None:
    """A bound selection that skips FEWER steps than the auto-skip must not
    have spec/plan/blind-run added to skip: automatic classification cannot
    add to the steps the user selected."""
    repo = narrow_repo(tmp_path)
    record_bound(repo, skip=["adversarial"])
    state = effective(repo)
    assert state["bound"] is True, state
    assert state["skip"] == ["adversarial"], state
    assert set(state["run"]) == set(step_names()) - {"adversarial"}, state
    assert AUTO_SKIP <= set(state["run"]), (
        f"auto-skip leaked into a bound selection's skip: {state}")


def test_effectiveselection_boundmore_noautoremove(tmp_path: Path) -> None:
    """A bound selection that skips MORE steps than the auto-skip must keep
    every skipped step: automatic classification cannot remove from the steps
    the user selected."""
    repo = narrow_repo(tmp_path)
    user_skip = sorted(AUTO_SKIP | {"reviewers", "adversarial"})
    record_bound(repo, skip=user_skip)
    state = effective(repo)
    assert state["bound"] is True, state
    assert set(state["skip"]) == set(user_skip), state
    assert set(state["run"]) == set(step_names()) - set(user_skip), state


def test_effectiveselection_cancel_autoresume(tmp_path: Path) -> None:
    """After a cancel, no selection is bound and the narrow-delta auto-skip
    applies again — the machine takes over exactly where it did before the
    user typed anything."""
    repo = narrow_repo(tmp_path)
    record_bound(repo, skip=["adversarial"])
    branch, merge_base = selection.current_scope(repo)
    selection.append_event(repo, CHANGE, {
        "event": "cancel", "source": "agent-run", "prompt_ref": None,
        "branch": branch, "merge_base": merge_base, "at": selection.now(),
    })
    state = effective(repo)
    assert state["bound"] is False, state
    assert set(state["skip"]) == AUTO_SKIP, state
    assert "intent" not in state["skip"], state


def test_effectiveselection_wrongscope_unbound(tmp_path: Path) -> None:
    """A confirmation recorded against another merge base never binds; the
    narrow delta then falls back to the auto-skip."""
    repo = narrow_repo(tmp_path)
    record_bound(repo, skip=["adversarial"], merge_base="0" * 40)
    state = effective(repo)
    assert state["bound"] is False, state
    assert set(state["skip"]) == AUTO_SKIP, state


def test_effectiveselection_tampered_unbound(tmp_path: Path) -> None:
    """A confirmation whose prompt no longer hashes to its recorded sha is
    tampered and must not bind; the narrow delta falls back to auto-skip."""
    repo = narrow_repo(tmp_path)
    record_bound(repo, skip=["adversarial"])
    store = selection.store_path(repo, CHANGE)
    lines = [line for line in store.read_text(encoding="utf-8").splitlines() if line.strip()]
    rewritten = []
    for line in lines:
        event = json.loads(line)
        if event.get("event") == "confirmation":
            event["prompt_sha256"] = "0" * 64  # tamper after the fact
        rewritten.append(json.dumps(event, ensure_ascii=False, sort_keys=True))
    store.write_text("\n".join(rewritten) + "\n", encoding="utf-8")
    state = effective(repo)
    assert state["bound"] is False, state
    assert set(state["skip"]) == AUTO_SKIP, state


def test_effectiveselection_emptydelta_fullritual(tmp_path: Path) -> None:
    """A feature branch with no commits of its own has an empty committed
    delta: acceptance 3 keeps the full ritual — no automatic skips."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "base.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "base.py")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "switch", "-q", "-c", "feature")
    state = effective(repo)
    assert state["bound"] is False, state
    assert state["skip"] == [], state
    assert set(state["run"]) == set(step_names()), state


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
