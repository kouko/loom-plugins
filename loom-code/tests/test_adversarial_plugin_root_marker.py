"""Adversarial probes for the plugin-root fallback lint in
``check_contract_citations.py`` (``lacks_other_host_fallback`` /
``scan_plugin_root_fallbacks``).

The lint exists so no host other than Claude Code meets a bare
``${CLAUDE_PLUGIN_ROOT}`` with no way to find the plugin root. Probes feed it
the input it was written to catch, then the same input one step different.
A failing probe is a finding; a passing probe records a survived attack.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import check_contract_citations as ccc  # noqa: E402

REPO_ROOT = HERE.parents[1]

FALLBACK = ("The plugin root is `${CLAUDE_PLUGIN_ROOT}` on Claude Code; on any other host it "
            "is the directory two levels above this SKILL.md.")


def test_pluginrootlint_bare_token_flags():
    """The exact input the lint targets is flagged (survived attempt)."""
    assert ccc.lacks_other_host_fallback("Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py`.")


def test_pluginrootlint_wrapped_marker_accepted():
    """A marker wrapped across lines and capitalised still counts (survived attempt)."""
    text = "Use `${CLAUDE_PLUGIN_ROOT}` on Claude Code.\nOn any\n   other HOST it is two levels up."
    assert not ccc.lacks_other_host_fallback(text)


def test_pluginrootlint_marker_in_unrelated_sentence_flags():
    """A marker phrase that gives no plugin-root location must not satisfy the lint."""
    text = ("Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py`.\n\n"
            "Telemetry is disabled on any other host.")
    assert ccc.lacks_other_host_fallback(text)


def test_pluginrootlint_negated_marker_flags():
    """A sentence denying any fallback must not satisfy the lint."""
    text = ("Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py`. "
            "There is no supported path on any other host.")
    assert ccc.lacks_other_host_fallback(text)


def test_pluginrootlint_marker_only_in_code_fence_flags():
    """A marker that appears only inside a fenced example is not prose the reader follows."""
    text = ("Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/x.py`.\n\n"
            "```text\n# on any other host: TODO\n```\n")
    assert ccc.lacks_other_host_fallback(text)


def test_pluginrootlint_unbraced_env_token_flags():
    """``$CLAUDE_PLUGIN_ROOT`` is the same Claude-only root and needs the same fallback."""
    assert ccc.lacks_other_host_fallback("Run `python3 $CLAUDE_PLUGIN_ROOT/scripts/x.py`.")


def test_pluginrootlint_affirmative_fallback_example_accepted():
    """Synthetic self-test: the canonical affirmative fallback sentence passes."""
    assert not ccc.lacks_other_host_fallback(FALLBACK)


def test_pluginrootlint_live_runtime_markdown_outside_scope_carries_fallback():
    """Runtime prose outside the lint's scan scope (plugin ``references/``, agent and
    skill trees) that names the token also carries the marker."""
    offenders = []
    for plugin in ("loom-code", "loom-design", "loom-workflow"):
        for path in (REPO_ROOT / plugin).rglob("*.md"):
            if path.name.startswith(("CHANGELOG", "README")) or "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if ccc.lacks_other_host_fallback(text):
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert offenders == []


def test_pluginrootlint_scan_scope_includes_plugin_references_dir(tmp_path):
    """A token-bearing ``loom-code/references/*.md`` without the marker is reported by the scan."""
    ref = tmp_path / "loom-code" / "references"
    ref.mkdir(parents=True)
    (ref / "tools.md").write_text("Run `${CLAUDE_PLUGIN_ROOT}/scripts/x.py`.\n", encoding="utf-8")
    assert ccc.scan_plugin_root_fallbacks(tmp_path) == ["loom-code/references/tools.md"]
