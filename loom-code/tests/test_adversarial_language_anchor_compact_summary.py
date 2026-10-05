# concern: the new SessionStart compact trigger reads Claude Code's English
# compaction summary (a user-role turn) as the user's language and stays silent
# for a Chinese conversation at exactly the moment it was added to cover.
"""Adversarial probe for 2026-10-04-relay-results-in-user-language (W1-02).

Claude Code writes each compaction summary into the transcript as a
main-chain user turn with ``isCompactSummary: true`` whose text is English
("This session is being continued from a previous conversation ...").
``lang_detect`` does not filter it, so at a SessionStart compact event the
summary votes 'en' and the anchor goes silent for a zh user.
"""
import json
import sys
import tempfile
from pathlib import Path

import pytest

_TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_TESTS))
from test_language_anchor_hook import ZH_FRAGMENT, ZH_TURN, run_hook  # noqa: E402

SUMMARY = (
    "This session is being continued from a previous conversation that ran "
    "out of context. The summary below covers the earlier portion of the "
    "conversation. Summary: 1. Primary Request and Intent: the user asked to "
    "relay agent results in the user's language. 2. Key Technical Concepts: "
    "hooks, transcripts, language detection. 3. Pending Tasks: run review."
)


def _transcript(entries):
    fh = tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    )
    for text, is_summary in entries:
        entry = {"type": "user", "isSidechain": False, "message": {"content": text}}
        if is_summary:
            entry["isCompactSummary"] = True
        fh.write(json.dumps(entry) + "\n")
    fh.close()
    return fh.name


@pytest.mark.parametrize(
    "entries",
    [
        [(ZH_TURN, False), (SUMMARY, True)],
        [(ZH_TURN, False), (ZH_TURN, False), (SUMMARY, True), (SUMMARY, True)],
    ],
    ids=["one-compaction", "two-auto-compactions-in-one-run"],
)
def test_sessionStartAnchor_zhTurnsThenCompactSummary_emitsZhDirective(entries):
    """A zh conversation that was just compacted still gets the zh anchor."""
    result = run_hook(
        {"hook_event_name": "SessionStart", "source": "compact",
         "transcript_path": _transcript(entries)}
    )
    assert result.returncode == 0
    assert result.stdout, "anchor stayed silent after compaction of a zh conversation"
    payload = json.loads(result.stdout)
    assert ZH_FRAGMENT in payload["hookSpecificOutput"]["additionalContext"]
