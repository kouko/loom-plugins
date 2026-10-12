def test_attestation_has_only_generated_evidence_fields() -> None:
    document = json.loads(ATTESTATION_TEMPLATE.read_text(encoding="utf-8"))
    assert list(document) == [
        "schema", "change_id", "content_digest", "executions", "verdicts", "findings", "selection",
        "intent_confirmed_sha", "tested_commit", "reviewed_commit", "acceptance_status"
    ]
    assert not ({"reviewed_sha", "scope", "dispatch", "cost", "questions", "charter"} & document.keys())