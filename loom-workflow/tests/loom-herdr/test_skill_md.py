"""Text contract for loom-herdr SKILL.md; live behaviour needs acceptance testing."""
from pathlib import Path
import re

import pytest

SKILL = Path(__file__).resolve().parents[2] / "skills" / "loom-herdr" / "SKILL.md"


def _text():
    return SKILL.read_text()


def _frontmatter():
    return _text().split("---")[1]


def _body():
    return _text().split("---", 2)[2]


def test_loads_herdr_skill_first():
    body = _body()
    assert "herdr --skill" in body
    assert body.index('test "${HERDR_ENV:-}" = 1') < body.index("herdr --skill")


def test_skill_failure_stops():
    body = _body()
    assert re.search(r"non-zero or prints nothing.*herdr --version.*stop", body, re.S)
    assert "without guessing" in body


def test_env_gate_stops():
    assert re.search(r"not (running )?inside herdr.*stop", _body(), re.S | re.I)


def test_no_herdr_command_outside():
    assert re.search(r"no herdr control command", _body(), re.I)


def test_description_requires_herdr_mention():
    assert re.search(r"^name: loom-herdr$", _frontmatter(), re.M)
    assert re.search(r"(explicitly|only when).*herdr", _frontmatter(), re.I | re.S)


def test_no_background_trigger():
    fm = _frontmatter().lower()
    assert re.search(r"not .*background.*parallel.*delegat|not .*parallel.*background", fm, re.S)


def test_full_reply_read_beyond_screen():
    body = _body()
    assert "mktemp -d" in body
    assert re.search(r"outside the repo", body)
    assert re.search(r"delete", body, re.I)
    assert re.search(r"delete the directory whenever the conversation ends", body)


def test_timeout_or_blocked_ends_with_report():
    body = _body()
    assert "--timeout 300000" in body
    assert re.search(r"timeout.*blocked.*report", body, re.S | re.I)
    assert re.search(r"never resend|no resend|do not resend", body, re.I)
    assert "$HERDR_PANE_ID" in body and "--current" in body


def test_operation_not_permitted_message():
    body = _body()
    assert "Operation not permitted" in body
    assert "network_access=true" in body


def test_no_retry():
    section = _body().split("Operation not permitted", 1)[1][:600]
    assert "not retry" in section.lower()


OFFICIAL_SENTENCES = [
    "Herdr organizes terminals into workspaces, tabs, and panes",
    "Do not run bare `herdr` for discovery",
    "Public IDs are opaque stable handles",
    "The installed binary is the authority for command syntax",
    "Do not use merely because a task could benefit from a background terminal",
]


@pytest.mark.parametrize("sentence", OFFICIAL_SENTENCES)
def test_no_official_text_copied(sentence):
    assert sentence not in _text()


def test_no_pinned_version():
    assert not re.search(r"\b\d+\.\d+\.\d+\b", _text())
