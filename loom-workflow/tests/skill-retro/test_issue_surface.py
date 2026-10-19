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
