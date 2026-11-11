"""Malformed JSON discriminators must not abort subsequent usable events."""

import json
import subprocess

import pytest

from ingest import ingest_codex_jsonl


@pytest.mark.parametrize("invalid", [[], {}], ids=["array", "object"])
@pytest.mark.parametrize("location", ["record", "payload", "role", "content"])
def test_codex_skips_unhashable_discriminators(tmp_path, invalid, location):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    payload = {"type": "message", "role": "user", "content": []}
    malformed = {"type": "response_item", "timestamp": "now", "payload": payload}
    if location == "record":
        malformed["type"] = invalid
    elif location == "payload":
        payload["type"] = invalid
    elif location == "role":
        payload["role"] = invalid
    else:
        payload["content"] = [{"type": invalid, "text": "must not surface"}]
    invocation = {"type": "response_item", "timestamp": "now", "payload": {
        "type": "function_call", "name": "Skill", "arguments": '{"skill":"test"}'}}
    records = [malformed, {"type": "session_meta", "payload": {"cwd": str(tmp_path)}},
               invocation, {"type": "turn_context", "payload": {}}, invocation]
    (tmp_path / "session.jsonl").write_text("\n".join(map(json.dumps, records)))

    events = list(ingest_codex_jsonl(tmp_path))
    calls = [event for event in events if event.skill_invocation]
    assert [event.project_path for event in calls] == [str((tmp_path / ".git").resolve()), None]
    assert [event.cwd for event in calls] == [str(tmp_path), None]
    assert [event.source_line for event in calls] == [3, 5]
    assert all("must not surface" not in event.text for event in events)
