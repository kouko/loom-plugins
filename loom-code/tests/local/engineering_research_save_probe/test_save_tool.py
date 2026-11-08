"""Offline persisted-output and boundary tests; no model or network requests."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import pytest

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('save_probe_tool', HERE / 'save_tool.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def tool(root, **overrides):
    return m.SaveTool({'root': str(root), 'create_roots': ['docs/loom/research'], **overrides})


def test_full_result_is_actual_persisted_unicode_body_and_local_links(tmp_path):
    source = tmp_path / 'source code.py'; source.write_text('evidence')
    body = '# Question\n\n結論、來源與限制。\n[code](../../../source%20code.py)\n[missing](absent.md)\n[section](#scope)\n[web](https://example.invalid/x)\n[outside](../../../../outside.md)\n'
    result = tool(tmp_path).save_record('docs/loom/research/q.md', body)
    saved = (tmp_path / result['path']).read_bytes()
    assert result['persisted_content'] == saved.decode() == body
    assert result['sha256'] == hashlib.sha256(saved).hexdigest()
    assert [x['status'] for x in result['links']] == ['exists', 'missing', 'anchor-unchecked', 'external-unchecked', 'outside-unchecked']
    assert result['written'] and result['readback_complete']
    assert 'research_correct' not in result and 'verified' not in result


def test_confirmation_mode_has_same_write_but_no_body_or_link_checks(tmp_path):
    a, b = tmp_path/'a', tmp_path/'b';a.mkdir();b.mkdir()
    full = tool(a).save_record('docs/loom/research/q.md', '# Same')
    brief = tool(b, result_mode='confirmation').save_record('docs/loom/research/q.md', '# Same')
    assert (a/full['path']).read_bytes() == (b/brief['path']).read_bytes()
    assert brief == {'written': True, 'path': 'docs/loom/research/q.md'}


@pytest.mark.parametrize('path', ['../escape.md', '/outside.md', 'src/code.md', 'skill/SKILL.md', '.git/config', 'provenance.json', 'fixtureVault/research/not-approved.md'])
def test_unapproved_paths_do_not_write(tmp_path, path):
    with pytest.raises(m.SaveError): tool(tmp_path).save_record(path, 'no')
    assert not list(tmp_path.rglob('*.md'))


def test_no_write_and_exact_authorized_copy(tmp_path):
    with pytest.raises(m.SaveError): m.SaveTool({'root':str(tmp_path)}).save_record('docs/loom/research/q.md','no')
    t=m.SaveTool({'root':str(tmp_path),'create_files':['fixtureVault/research/exact.md']})
    assert t.save_record('fixtureVault/research/exact.md','# approved')['written']
    with pytest.raises(m.SaveError):t.save_record('fixtureVault/research/other.md','# no')


def test_preexisting_collision_and_explicit_update_preserve_stale_changes(tmp_path):
    p=tmp_path/'docs/loom/research/q.md';p.parent.mkdir(parents=True);p.write_text('original')
    with pytest.raises(m.SaveError, match='collision'):tool(tmp_path).save_record(str(p),'overwrite')
    t=tool(tmp_path,update_files=['docs/loom/research/q.md'])
    p.write_text('other writer')
    with pytest.raises(m.SaveError,match='stale'):t.save_record(str(p),'overwrite')
    assert p.read_text()=='other writer'
    fresh=tool(tmp_path,update_files=['docs/loom/research/q.md'])
    assert fresh.save_record(str(p),'allowed update')['persisted_content']=='allowed update'
    assert fresh.save_record(str(p),'second update')['persisted_content']=='second update'


def test_session_created_file_updates_require_unchanged_saved_hash(tmp_path):
    t=tool(tmp_path);t.save_record('docs/loom/research/q.md','# first')
    p=tmp_path/'docs/loom/research/q.md';p.write_text('external change')
    with pytest.raises(m.SaveError,match='stale'):t.save_record('docs/loom/research/q.md','# second')
    assert p.read_text()=='external change'


def test_symlink_parent_and_file_cannot_escape_or_alias(tmp_path):
    outside=tmp_path.parent/(tmp_path.name+'-external');outside.mkdir()
    (tmp_path/'docs').symlink_to(outside,target_is_directory=True)
    with pytest.raises(m.SaveError):tool(tmp_path).save_record('docs/loom/research/q.md','no')
    assert not list(outside.rglob('*'))
    (tmp_path/'docs').unlink();p=tmp_path/'docs/loom/research';p.mkdir(parents=True)
    target=outside/'victim.md';target.write_text('safe');(p/'q.md').symlink_to(target)
    with pytest.raises(m.SaveError):tool(tmp_path).save_record('docs/loom/research/q.md','no')
    assert target.read_text()=='safe'


def test_code_examples_images_and_reference_links_are_not_false_checks(tmp_path):
    body='```md\n[x](missing.md)\n```\n`[y](missing.md)`\n![image](missing.png)\n[ref][id]\n[id]: absent.md\n[real](missing.md)\n'
    result=tool(tmp_path).save_record('docs/loom/research/q.md',body)
    assert len(result['links'])==1 and result['links'][0]['status']=='missing'
    assert result['unsupported_reference_links']
    assert 'limited' in result['link_scope']


def test_size_rejected_before_mutation(tmp_path):
    with pytest.raises(m.SaveError,match='size'):tool(tmp_path).save_record('docs/loom/research/q.md','界'*12000)
    assert not (tmp_path/'docs').exists()


def test_instruction_config_names_cannot_become_research_writes(tmp_path):
    for path in ['docs/loom/research/CLAUDE.md', 'docs/loom/research/AGENTS.md', 'docs/loom/research/.claude/rules/x.md']:
        with pytest.raises(m.SaveError): tool(tmp_path).save_record(path, 'not a research record')
    assert not (tmp_path/'docs').exists()


def test_outside_link_does_not_probe_outside_filesystem(tmp_path, monkeypatch):
    original = Path.exists
    def only_inside(self):
        if not self.is_relative_to(tmp_path): raise AssertionError('outside filesystem probe')
        return original(self)
    monkeypatch.setattr(Path,'exists',only_inside)
    result=tool(tmp_path).save_record('docs/loom/research/q.md','[outside](../../../../private.md)')
    assert result['links'][0]['status']=='outside-unchecked'


def test_link_symlink_is_not_followed(tmp_path):
    (tmp_path/'link').symlink_to(tmp_path.parent/'outside-absent',target_is_directory=True)
    result=tool(tmp_path).save_record('docs/loom/research/q.md','[symlink](../../../link/a.md)')
    assert result['links'][0]['status']=='symlink-unchecked'


def test_malformed_url_retains_complete_truthful_save_result(tmp_path):
    result=tool(tmp_path).save_record('docs/loom/research/q.md','[x](http://[)')
    assert result['written'] and result['readback_complete']
    assert result['persisted_content']=='[x](http://[)'
    assert result['links'][0]['status']=='malformed-unchecked'


def test_failed_persisted_read_does_not_claim_success(tmp_path, monkeypatch):
    original=Path.read_bytes
    def fail_saved(self):
        if self.name=='q.md':raise OSError('simulated read failure')
        return original(self)
    monkeypatch.setattr(Path,'read_bytes',fail_saved)
    with pytest.raises(m.SaveError) as exc:tool(tmp_path).save_record('docs/loom/research/q.md','# saved but unread')
    assert exc.value.written is True
    assert (tmp_path/'docs/loom/research/q.md').read_text()=='# saved but unread'


def test_stdio_protocol_and_modes_share_tool_contract(tmp_path):
    policy=tmp_path/'policy.json';root=tmp_path/'project';root.mkdir();policy.write_text(json.dumps({'root':str(root),'create_roots':['docs/loom/research']}))
    request=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05'}},
      {'jsonrpc':'2.0','method':'notifications/initialized'},
      {'jsonrpc':'2.0','id':2,'method':'tools/list'},
      {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'save_record','arguments':{'path':'docs/loom/research/q.md','content':'# Complete\n\nActual body'}}},
      {'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'save_record','arguments':{'path':'../outside.md','content':'no'}}}]
    p=subprocess.run([sys.executable,str(HERE/'server.py'),'--policy',str(policy)],input=''.join(json.dumps(r)+'\n' for r in request),text=True,capture_output=True,check=True)
    replies=[json.loads(l) for l in p.stdout.splitlines()]
    assert [x['id'] for x in replies]==[1,2,3,4]
    assert replies[0]['result']['protocolVersion']=='2024-11-05'
    contract=replies[1]['result']['tools'];assert [x['name'] for x in contract]==['save_record']
    result=json.loads(replies[2]['result']['content'][0]['text']);assert result['persisted_content']=='# Complete\n\nActual body'
    assert not replies[2]['result']['isError'] and replies[3]['result']['isError']
    assert json.loads(replies[3]['result']['content'][0]['text'])['written'] is False
    policy.write_text(json.dumps({'root':str(root),'result_mode':'confirmation'}))
    q=subprocess.run([sys.executable,str(HERE/'server.py'),'--policy',str(policy)],input=json.dumps(request[2])+'\n',text=True,capture_output=True,check=True)
    assert json.loads(q.stdout)['result']['tools']==contract


def test_stdio_invalid_params_are_errors_without_process_crash(tmp_path):
    policy=tmp_path/'policy.json'; policy.write_text(json.dumps({'root':str(tmp_path)}))
    requests=[{'jsonrpc':'2.0','id':1,'method':'tools/call','params':None},
              {'jsonrpc':'2.0','id':2,'method':'ping'}]
    p=subprocess.run([sys.executable,str(HERE/'server.py'),'--policy',str(policy)],input=''.join(json.dumps(x)+'\n' for x in requests),text=True,capture_output=True)
    assert p.returncode==0
    result=[json.loads(x) for x in p.stdout.splitlines()]
    assert result[0]['error']['code']==-32600 and result[1]['result']=={}


def test_stdio_malformed_link_does_not_lose_saved_state(tmp_path):
    policy=tmp_path/'policy.json';policy.write_text(json.dumps({'root':str(tmp_path),'create_roots':['docs/loom/research']}))
    request={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'save_record','arguments':{'path':'docs/loom/research/q.md','content':'[x](http://[)'}}}
    p=subprocess.run([sys.executable,str(HERE/'server.py'),'--policy',str(policy)],input=json.dumps(request)+'\n',text=True,capture_output=True,check=True)
    response=json.loads(p.stdout)
    assert 'result' in response
    body=json.loads(response['result']['content'][0]['text'])
    assert body['written'] and body['persisted_content']=='[x](http://[)'
