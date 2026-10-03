"""W0-05 / REQ-8 — the SessionStart injection must shrink to at most half
the pre-change baseline (plan §0: baseline 923fb84a = 5278 words, target
<= 2639) and must carry only the orientation a session cannot derive: the
station order, the three human decision points in plain words, a pointer
to the entry station's SKILL.md for the full summary table, and the
repo's KICKOFF-DEFAULTS lines when that file exists.

The measurement command is fixed by concept-model §11:
``bash loom-code/hooks/session-start </dev/null | python3 -c
'import sys;print(len(sys.stdin.read().split()))'`` with cwd = an empty
git repo. The budget test below counts with Python's ``str.split()``;
the recorded baseline number of 5278 is itself produced by that same
counter (``check_mechanisms.py --measure`` uses it too).

Station names and decision-point numbers are asserted against
``loom-code/contract/manifest.yaml`` — the hook derives them from the
manifest rather than carrying a second hand-typed copy.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / "loom-code" / "hooks" / "session-start"
MANIFEST = REPO / "loom-code" / "contract" / "manifest.yaml"

WORD_CAP = 2639


@pytest.fixture(scope="module")
def manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def empty_repo(tmp_path_factory) -> Path:
    repo = tmp_path_factory.mktemp("empty-git-repo")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return repo


def _run(cwd: Path, env: dict | None = None) -> str:
    # R30-O3: capture bytes and decode explicitly (errors="replace") rather
    # than text=True, so a non-UTF-8 byte in the hook's output cannot raise
    # a UnicodeDecodeError inside subprocess.run itself.
    proc = subprocess.run(
        ["bash", str(HOOK)],
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        env=env,
    )
    assert proc.returncode == 0, proc.stderr.decode("utf-8", errors="replace")
    return proc.stdout.decode("utf-8", errors="replace")


def _context(stdout: str) -> str:
    payload = json.loads(stdout)
    return payload["hookSpecificOutput"]["additionalContext"]


def test_word_count_is_within_budget(empty_repo):
    assert len(_run(empty_repo).split()) <= WORD_CAP


def test_emits_only_the_canonical_context_key(empty_repo):
    """Codex 0.154 marks a hook Failed when its JSON carries keys beside
    hookSpecificOutput, so every host gets only that key."""
    payload = json.loads(_run(empty_repo))
    assert payload["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    assert payload["hookSpecificOutput"]["additionalContext"]
    assert set(payload) == {"hookSpecificOutput"}


def test_routes_software_development_requests_into_loom(empty_repo):
    """A4: without outside rules, the text alone says which requests enter."""
    context = _context(_run(empty_repo))
    assert "adds a feature or fixes a bug starts at capture-intent (write-plan when loom-design is not installed) before you edit any file" in context
    assert "in any repository, even when the user never says loom and there is no docs/loom folder" in context
    assert "Outside an active change, a feature or bug-fix request goes through loom however small" in context
    assert "edits that add no feature and fix no bug (a typo, a rename that changes no behaviour, comment or doc wording) and work that is not software development (research, notes) go direct unless the user asks for loom" in context
    assert "this repo runs through stations" not in context


def test_names_every_station_in_manifest_order(empty_repo, manifest):
    context = _context(_run(empty_repo))
    names = [s["name"] for s in manifest["stations"]]
    positions = [context.find(n) for n in names]
    assert all(p >= 0 for p in positions), dict(zip(names, positions))
    flow = [n for n in names if n != "maintain"]
    assert " → ".join(flow) in context
    assert "maintain" in context


def test_states_the_three_decision_points_in_plain_words(empty_repo):
    context = _context(_run(empty_repo))
    for marker in ("①", "②", "③"):
        assert marker in context, marker
    # plain-language content, not mechanism names
    assert "this is what I want" in context
    assert "product" in context  # ② is product-only


def test_points_at_the_entry_station_instead_of_inlining_the_table(empty_repo):
    context = _context(_run(empty_repo))
    assert "SKILL.md" in context
    assert "capture-intent" in context and "write-plan" in context
    # the summary table itself must NOT be inlined
    assert "|---" not in context


def test_kickoff_defaults_lines_are_injected_when_the_file_exists(empty_repo, tmp_path):
    repo = tmp_path / "repo-with-defaults"
    (repo / "docs" / "loom").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "# KICKOFF-DEFAULTS\n\n- second-vendor: codex — user picked (2026-09-02)\n"
        "- standing-docs: waived — spike repo (2026-09-02)\n",
        encoding="utf-8",
    )
    context = _context(_run(repo))
    assert "second-vendor: codex — user picked (2026-09-02)" in context
    assert "standing-docs: waived — spike repo (2026-09-02)" in context


def test_kickoff_defaults_control_characters_do_not_break_the_json(tmp_path, manifest):
    repo = tmp_path / "repo-with-control-chars"
    (repo / "docs" / "loom").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "# KICKOFF-DEFAULTS\n\n- second-vendor: codex\f \x1b[31mred\x1b[0m (2026-09-02)\n"
        "- standing-docs: waived — spike repo (2026-09-02)\n"
        "-\x1b 語言: 繁體中文 (2026-09-02)\n"
        "-\fa: one\n-\vb: two\n",
        encoding="utf-8",
    )
    context = _context(_run(repo))
    assert "- a: one" in context and "- b: two" in context
    flow = [s["name"] for s in manifest["stations"] if s["name"] != "maintain"]
    assert " → ".join(flow) in context
    assert "standing-docs: waived — spike repo (2026-09-02)" in context
    assert "- 語言: 繁體中文 (2026-09-02)" in context
    assert "\f" not in context and "\x1b" not in context


def test_kickoff_defaults_survive_an_iconv_that_fails_without_reading(tmp_path):
    repo = tmp_path / "repo-with-broken-iconv"
    (repo / "docs" / "loom").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "- standing-docs: waived — spike repo (2026-09-02)\n" + "# pad\n" * 20000,
        encoding="utf-8",
    )
    shim = tmp_path / "bin"
    shim.mkdir()
    (shim / "iconv").write_text("#!/bin/sh\nexit 127\n", encoding="utf-8")
    (shim / "iconv").chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}{os.pathsep}{os.environ['PATH']}"}
    assert "standing-docs: waived — spike repo (2026-09-02)" in _context(_run(repo, env))


def test_no_kickoff_section_when_the_file_is_absent(empty_repo):
    assert "KICKOFF-DEFAULTS" not in _context(_run(empty_repo))


def test_escape_hatch_still_returns_empty_context(empty_repo):
    proc = subprocess.run(
        ["bash", str(HOOK)],
        cwd=str(empty_repo),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        env={**os.environ, "LOOM_CODE_MODE": "off"},
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload == {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ""}}


def test_no_deleted_mechanism_is_mentioned(empty_repo):
    context = _context(_run(empty_repo))
    for gone in ("router", "reception", "relay", "on-ramp", "waiver", "batch"):
        assert gone not in context.lower(), gone


def test_suggest_notice_is_after_plan_and_not_a_decision_point(empty_repo):
    context = _context(_run(empty_repo))
    assert "after the plan's risk evidence exists" in context
    assert "continues without waiting" in context
    dp1 = context[context.index("①"):context.index("②")]
    assert "second-vendor suggestion" not in dp1


if __name__ == "__main__":  # pragma: no cover - manual measurement helper
    sys.exit(pytest.main([__file__, "-q"]))


def test_a_decision_point_with_no_match_does_not_abort_the_hook(tmp_path):
    """`set -e` kills the script when a command substitution's last command
    fails, and `grep` fails on no match -- so a manifest whose stations
    declare no decision point used to produce an empty injection instead of
    the station order. The lookup must tolerate the empty result."""
    plugin = tmp_path / "plugin"
    (plugin / "hooks").mkdir(parents=True)
    (plugin / "contract").mkdir()
    (plugin / "hooks" / "session-start").write_text(
        HOOK.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (plugin / "contract" / "manifest.yaml").write_text(
        "version: 1.0.0\n"
        "stations:\n"
        "  - {name: write-plan, owner: loom-code, produces: plan}\n"
        "  - {name: build,      owner: loom-code, produces: diff}\n"
        "  - {name: maintain,   owner: loom-code, produces: intent}\n",
        encoding="utf-8",
    )
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    proc = subprocess.run(
        ["bash", str(plugin / "hooks" / "session-start")],
        cwd=str(repo), stdin=subprocess.DEVNULL, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "write-plan" in _context(proc.stdout), proc.stdout
