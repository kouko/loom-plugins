# concern: Source provenance or capture bounds may be lost across retrospective stages.
import pytest

from cluster import cluster_memory_items
from propose import normalize_memory_item, render_proposals_markdown


def integration(session, *, subtype='hook', mechanism='hook suppresses activation', pointer='plugin/hooks/activate.sh'):
    return normalize_memory_item({
        'title': 'Activation lost', 'description': 'Observed activation failed',
        'content': mechanism, 'kind': 'failure',
        'issue_surface': 'plugin-integration', 'integration_subtype': subtype,
        'failure_mechanism': mechanism, 'source_pointer': pointer,
        '_source_session': session,
    })


def test_integration_requires_source_and_does_not_invent_anchor():
    with pytest.raises(ValueError, match='source_pointer'):
        integration('s1', pointer='')
    item = integration('s1')
    assert item['section_anchor'] == ''
    with pytest.raises(ValueError, match='issue_surface'):
        normalize_memory_item({'title': 'unclassified', 'section_anchor': 'Examples'})


def test_source_provenance_roundtrip(tmp_path):
    import json
    from ingest import ingest_claude_jsonl, ingest_codex_jsonl
    from main import _build_subagent_entries
    from propose import extract_memory_items
    from report import build_dispatch_payload

    results = []
    target = '/plugins/demo/skills/activate/SKILL.md'
    for host, adapter in [('claude-code', ingest_claude_jsonl), ('codex', ingest_codex_jsonl)]:
        root = tmp_path / host
        root.mkdir()
        path = root / f'{host}.jsonl'
        record = ({'type': 'user', 'sessionId': host, 'timestamp': '2026-10-23T00:00:00Z',
                   'message': {'role': 'user', 'content': 'observable'}} if host == 'claude-code' else
                  {'type': 'response_item', 'timestamp': '2026-10-23T00:00:00Z',
                   'payload': {'type': 'message', 'role': 'user', 'content': 'observable'}})
        path.write_text(json.dumps(record) + '\n')
        stream_events = adapter(root)
        events = [next(stream_events)]
        assert events[0].source_path == str(path) and events[0].source_line == 1
        entry = _build_subagent_entries('demo:activate', [host], {host: events}, {}, target_skill_path=target)[0]
        captured = json.dumps(entry)
        with path.open('a') as stream:
            stream.write(json.dumps(record) + '\n')
        assert list(stream_events) == []
        assert json.dumps(entry) == captured
        snapshot = entry['input']['session_snapshot']
        assert snapshot['event_count'] == 1 and snapshot['captured_at']
        assert snapshot['tools'] == [host] and snapshot['last_ts'] == record['timestamp']
        evidence = {'session_id': host, 'tool': host, 'path': target, 'location': 'Usage:2',
                    'version_status': 'historical', 'version_evidence': f'{host} recorded revision',
                    'observation': 'source text', 'uncertainty': ''}
        results.append({'session_id': host, 'target_skill_path': target,
                        'session_snapshot': snapshot, 'source_inspections': [evidence],
                        'memory_items': [integration(host)]})
    items = extract_memory_items(results, target)
    promoted, _ = cluster_memory_items([{**i, 'session_id': i['_source_session']} for i in items])
    assert {p['tool'] for p in promoted[0]['source_inspections']} == {'claude-code', 'codex'}
    assert len(promoted[0]['session_snapshots']) == 2
    rendered = render_proposals_markdown(items, target_skill_path=target, target_skill_md_content='# Activate')
    for host in ('claude-code', 'codex'):
        assert f'{host} recorded revision' in rendered
    assert build_dispatch_payload(results, 'en', '2026-10-23', 'out.md')['dispatch_payload']['input']['merged_data'] == results


@pytest.mark.parametrize('status', ['current', 'unknown'])
def test_unavailable_historical_source_is_explicit(status):
    item = integration('s1')
    item['source_inspections'] = [{'session_id': 's1', 'path': '/unavailable/SKILL.md',
        'version_status': status, 'version_evidence': '', 'uncertainty': 'historical source missing or access denied'}]
    normalized = normalize_memory_item(item)
    rendered = render_proposals_markdown([normalized], target_skill_path='/unavailable/SKILL.md', target_skill_md_content='')
    assert 'historical source missing or access denied' in rendered
    assert status in rendered
    assert normalize_memory_item(integration('legacy'))['source_inspections'] == []
    for invalid in ('not a list', ['not a record'], [{'version_status': 'historical'}]):
        with pytest.raises(ValueError):
            normalize_memory_item({**item, 'source_inspections': invalid})


def test_two_distinct_sessions_promote_integration_and_one_stays_pending():
    items = [integration('s1'), integration('s2', pointer='plugin/hooks/activate.ts'), integration('s2', mechanism='loader drops registration', subtype='loading')]
    promoted, pending = cluster_memory_items([{**i, 'session_id': i['_source_session']} for i in items])
    assert len(promoted) == 1
    assert promoted[0]['supporting_sessions'] == ['s1', 's2']
    assert promoted[0]['supporting_source_pointers'] == ['plugin/hooks/activate.sh', 'plugin/hooks/activate.ts']
    assert len(pending) == 1
    rendered = render_proposals_markdown(items, target_skill_path='/tmp/a/SKILL.md', target_skill_md_content='# A\n## Examples\n', run_date='2026-10-15')
    assert '## Plugin integration proposals' in rendered
    assert 'plugin/hooks/activate.sh' in rendered
    assert 'plugin/hooks/activate.ts' in rendered
    assert '**Supporting sessions**: `s1`, `s2`' in rendered
    assert 'loader drops registration' in rendered
    assert '§Examples' not in rendered.split('## Plugin integration proposals', 1)[1].split('## Anchor mismatch', 1)[0]
    assert 'apply.py' not in rendered


def test_promoted_integration_reference_request_stays_integration_proposal():
    from propose import extract_memory_items

    results = [
        {
            'session_id': session,
            'target_skill': 'demo:activate',
            'target_skill_path': '/plugins/demo/skills/activate/SKILL.md',
            'memory_items': [{
                'title': 'Hook activation gap',
                'description': 'Hook blocks activation',
                'content': 'Investigate hook registration and add integration coverage.',
                'kind': 'failure',
                'issue_surface': 'plugin-integration',
                'integration_subtype': 'hook',
                'failure_mechanism': 'hook blocks activation',
                'source_pointer': f'plugin/hooks/{session}.sh',
                'requires_new_reference_file': True,
            }],
        }
        for session in ('session-a', 'session-b')
    ]
    items = extract_memory_items(results, '/plugins/demo/skills/activate/SKILL.md')
    rendered = render_proposals_markdown(
        items,
        target_skill_path='/plugins/demo/skills/activate/SKILL.md',
        target_skill_md_content='# Activate\n## Usage\n',
    )
    integration_section = rendered.split('## Plugin integration proposals', 1)[1].split('## Anchor mismatch', 1)[0]
    deferred_section = rendered.split('## Marked for v0.2', 1)[1]
    assert '### Hook activation gap' in integration_section
    assert '`session-a`, `session-b`' in integration_section
    assert 'plugin/hooks/session-a.sh' in integration_section
    assert 'plugin/hooks/session-b.sh' in integration_section
    assert 'new reference file' in integration_section.lower()
    assert 'Hook activation gap' not in deferred_section
    assert '§' not in integration_section
