"""Adversarial probes for loom-visualization (change 2026-09-14-loom-visualization).

Abuse and boundary cases against detect_client, the ASCII width engine and
table check, the stdlib markdown renderer, and the Mermaid validator. A probe
marked xfail(strict=True) records a defect reported as a finding; it turns
into an XPASS failure once the defect is fixed.
"""

import os
import pathlib
import shutil
import subprocess
import sys

import pytest

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_cot_html as rch  # noqa: E402
from checks_table import find_issues  # noqa: E402
from detect_client import detect  # noqa: E402
from gen_table import render_table  # noqa: E402
from width import display_width  # noqa: E402

VALIDATOR = HERE.parents[2] / "tests" / "mermaid" / "validate_mermaid.mjs"


# ---------- detect_client ----------

@pytest.mark.parametrize("env", [
    {"CLAUDECODE": "1 "},
    {"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "../../etc/passwd\nmermaid=true"},
    {"CLAUDECODE": "1", "CODEX_THREAD_ID": "x", "GEMINI_CLI": "1"},
    {"CLAUDECODE": "\u0661"},  # Arabic-Indic digit one
    {},
])
def test_detect_client_hostile_env_mermaid_never_true(env):
    """No environment value, however malformed, may switch mermaid on."""
    result = detect(env)
    assert result["mermaid"] is False
    assert set(result) == {"client", "mermaid", "remote_viewer", "obsidian_vault", "reason"}


def test_detect_client_whitespace_marker_not_claude_code():
    """CLAUDECODE='1 ' is not an exact marker, so the client is not Claude Code."""
    assert detect({"CLAUDECODE": "1 "})["client"] == "unknown"


def test_detect_client_symlinked_obsidian_dir_detected_as_vault(tmp_path):
    """A .obsidian symlink to a real dir still marks the vault (isdir follows links)."""
    real = tmp_path / "real_obsidian"
    real.mkdir()
    vault = tmp_path / "vault"
    vault.mkdir()
    os.symlink(real, vault / ".obsidian")
    assert detect({}, target=str(vault / "a" / "b" / "note.md"))["obsidian_vault"] is True


def test_detect_client_obsidian_plain_file_not_vault(tmp_path):
    """A regular file named .obsidian is not a vault marker."""
    (tmp_path / ".obsidian").write_text("x")
    assert detect({}, target=str(tmp_path / "note.md"))["obsidian_vault"] is False


def test_detect_client_dangling_symlink_not_vault(tmp_path):
    """A dangling .obsidian symlink is not a vault marker and does not raise."""
    os.symlink(tmp_path / "missing", tmp_path / ".obsidian")
    assert detect({}, target=str(tmp_path / "x.md"))["obsidian_vault"] is False


def test_detect_client_nul_in_target_no_crash():
    """A NUL byte in the target path returns a boolean instead of raising."""
    assert detect({}, target="/nonexistent/\x00evil")["obsidian_vault"] in (True, False)


def test_detect_client_cwd_in_vault_without_target_returns_none(tmp_path, monkeypatch):
    """Chat output (no --target) from inside a vault is not checked: obsidian_vault is None.

    Records the gate gap reported against loom-visualization.obsidian-boundary.
    """
    (tmp_path / ".obsidian").mkdir()
    monkeypatch.chdir(tmp_path)
    assert detect({})["obsidian_vault"] is None


# ---------- width engine and table check ----------

def test_width_table_combining_only_label_stays_aligned():
    """A label made only of combining marks renders an aligned table and no crash."""
    lines = render_table(["h"], [["\u0301\u0301"], ["xx"]]).split("\n")
    assert len({display_width(l) for l in lines}) == 1
    assert find_issues(lines) == []


def test_width_table_long_cjk_label_stays_aligned():
    """A 300-glyph CJK label renders an aligned table."""
    lines = render_table(["名前"], [["漢" * 300]]).split("\n")
    assert len({display_width(l) for l in lines}) == 1
    assert find_issues(lines) == []


def test_width_table_check_off_by_one_padding_flagged():
    """One extra padding cell in a CJK row is reported by the table check."""
    lines = render_table(["名前", "x"], [["漢字", "b"]]).split("\n")
    lines[1] = lines[1][:-1] + " │"
    assert find_issues(lines) != []


def test_width_table_empty_headers_raises_loudly():
    """An empty header list fails loudly rather than printing an empty frame."""
    with pytest.raises(ValueError):
        render_table([], [])


@pytest.mark.xfail(strict=True, reason="finding: Cc chars (tab, ESC) measured 0 cells; "
                   "generator misaligns and check_table reports clean")
@pytest.mark.parametrize("cell", ["a\tb", "\x1b[31mred\x1b[0m"])
def test_width_table_control_char_label_rejected_or_flagged(cell):
    """A tab or ANSI escape in a cell is rejected, or the check flags the table."""
    try:
        lines = render_table(["h"], [[cell], ["xx"]]).split("\n")
    except ValueError:
        return
    assert find_issues(lines) != []


# ---------- render_cot_html ----------

@pytest.mark.parametrize("md", [
    "<script>alert(1)</script>\n",
    "[x](javascript:alert(1))\n",
    "[x](JaVaScRiPt:alert(1))\n",
    "[x](&#106;avascript:alert(1))\n",
    "<javascript:alert(1)>\n",
    "[x]\n\n[x]: javascript:alert(1)\n",
    "![a](javascript:alert(1))\n",
    "[x](vbscript:msgbox(1))\n",
    "[x](data:text/html,<script>alert(1)</script>)\n",
    '[x](http://a "\\" onmouseover=\\"alert(1)")\n',
    "```mermaid\nflowchart TD\nA[\"<img src=x onerror=alert(1)>\"]-->B\n```\n",
    "```mermaid\nflowchart TD\nA[\"<br/><script>x</script>\"]-->B\n```\n",
])
def test_render_cot_html_hostile_markdown_no_injection(md):
    """No raw script tag, event handler attribute or script-scheme href reaches the page."""
    out = rch.render_body(md).lower()
    assert "<script" not in out
    assert "<img" not in out
    assert 'href="javascript:' not in out and 'href="vbscript:' not in out
    assert 'href="data:text' not in out
    assert '" onmouseover=' not in out


def test_render_cot_html_unclosed_fence_contained_in_code():
    """An unclosed fence runs to end of input inside <code>, with no leftover report."""
    out = rch.render_body("```\n# code\n**bold**\n")
    assert out.startswith("<pre><code>")
    assert rch.leftover_markdown(out) == []


def test_render_cot_html_leftover_heading_inside_tag_detected():
    """A literal heading marker that survived into a paragraph is reported."""
    assert rch.leftover_markdown("<p>## not converted</p>") != []


def test_render_cot_html_deep_nested_list_no_crash():
    """A 400-level nested list renders without raising."""
    rch.render_body("".join("  " * i + "- a\n" for i in range(400)))


@pytest.mark.xfail(strict=True, raises=RecursionError,
                   reason="finding: 3000 nested blockquotes raise RecursionError")
def test_render_cot_html_deep_nested_blockquote_no_crash():
    """3000 nested blockquote markers render without raising."""
    rch.render_body("> " * 3000 + "x\n")


# ---------- validate_mermaid.mjs ----------

def _validate(tmp_path, text):
    if shutil.which("node") is None or not (VALIDATOR.parent / "node_modules").is_dir():
        pytest.skip("node or tests/mermaid/node_modules absent")
    f = tmp_path / "probe.md"
    f.write_text(text, encoding="utf-8")
    return subprocess.run(["node", str(VALIDATOR), str(f)], capture_output=True,
                          text=True, timeout=120)


def test_validate_mermaid_empty_block_fails(tmp_path):
    """An empty mermaid block is a failure, not a vacuous pass."""
    assert _validate(tmp_path, "```mermaid\n```\n").returncode == 1


def test_validate_mermaid_init_directive_only_fails(tmp_path):
    """A block holding only an init directive is a failure."""
    assert _validate(tmp_path, '```mermaid\n%%{init: {"theme":"dark"}}%%\n```\n').returncode == 1


def test_validate_mermaid_indented_bad_fence_fails(tmp_path):
    """An indented fence around a broken diagram is still parsed and fails."""
    text = "    ```mermaid\n    flowchart TD\n    A -> B\n    ```\n"
    assert _validate(tmp_path, text).returncode == 1


def test_validate_mermaid_no_blocks_fails(tmp_path):
    """A file with no mermaid block fails rather than passing vacuously."""
    assert _validate(tmp_path, "plain text\n").returncode == 1


@pytest.mark.xfail(strict=True, reason="finding: ```mermaid <info> fence is skipped by the "
                   "validator but rendered as mermaid by render_cot_html")
def test_validate_mermaid_info_string_bad_block_fails(tmp_path):
    """A broken block whose fence carries an info string after `mermaid` fails validation."""
    assert rch.render_body("```mermaid title\nflowchart TD\n```\n").startswith('<pre class="mermaid">')
    text = "```mermaid title\nflowchart TD\n    A -> B\n```\n```mermaid\nflowchart TD\n  A-->B\n```\n"
    assert _validate(tmp_path, text).returncode == 1
