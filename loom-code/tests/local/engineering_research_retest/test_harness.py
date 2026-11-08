"""Offline safety/protocol checks for the optional local comparison harness."""
from pathlib import Path
import importlib.util
import subprocess
from unittest.mock import Mock
import pytest

spec = importlib.util.spec_from_file_location('paired_retest_harness', Path(__file__).with_name('harness.py'))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def test_only_confined_native_file_tools_and_no_write_for_f03():
    normal = h.command('ordinary', 'prompt')
    readonly = h.command('F03', 'prompt')
    assert normal[normal.index('--tools') + 1] == 'Read,Write,Edit,Grep,Glob'
    assert readonly[readonly.index('--tools') + 1] == 'Read,Grep,Glob'
    assert '--restricted' in normal and '--safe-mode' in normal
    assert '--strict-mcp-config' in normal and '--mcp-config' not in normal
    assert normal[normal.index('--model') + 1] == 'claude-sonnet-5-5'
    assert normal[normal.index('--effort') + 1] == 'medium'
    assert normal[normal.index('--setting-sources') + 1] == ''
    assert 'Bash' not in ','.join(normal) and 'Skill' not in ','.join(normal) and 'Agent' not in ','.join(normal)


def test_environment_does_not_inherit_proxy_tokens_or_provider_aliases():
    env = h.environment({'HOME':'x','PATH':'y','ANTHROPIC_API_KEY':'secret','HTTPS_PROXY':'proxy','ANTHROPIC_BASE_URL':'alias','SECURITYSESSIONID':'ok'})
    assert env == {'HOME':'/Users/kouko','PATH':'y','SECURITYSESSIONID':'ok'}


def test_no_overwrite_or_refreeze(tmp_path):
    h.require_fresh(tmp_path / 'new')
    (tmp_path / 'freeze.json').write_text('{}')
    with pytest.raises(RuntimeError): h.require_fresh(tmp_path)
    out = tmp_path / 'actor'; out.mkdir(); (out / 'answer.txt').write_text('prior')
    with pytest.raises(RuntimeError): h.require_unrun(out)


def test_actor_prompt_has_no_labels_rubric_or_verification_coaching():
    p = h.actor_prompt('COMMON', 'CASE')
    assert p.startswith('COMMON\nCASE\n')
    assert 'fixture-observations.json' in p
    assert not any(x in p.lower() for x in ['old_skill','new_skill','baseline','criteria','rubric','read back'])


def test_protected_mutation_detected_and_no_write_assertion():
    before={'src/a.py':'a','skill/SKILL.md':'b','docs/old.md':'c'}
    good=h.inventory_checks('F03',before,before)
    assert good['protected_unchanged'] and good['case_boundary_satisfied']
    bad=h.inventory_checks('F03',before,{**before,'src/a.py':'evil','scratch/a.md':'d'})
    assert not bad['protected_unchanged'] and not bad['case_boundary_satisfied']
    denied=h.inventory_checks('F05',before,{**before,'fixtureVault/research/x.md':'x'})
    assert not denied['case_boundary_satisfied']
    extra=h.inventory_checks('F06',before,{**before,'fixtureVault/research/2026-11-08-package-test-roots.md':'x','scratch/extra.md':'y'})
    assert not extra['case_boundary_satisfied']


def test_timeout_terminates_process_group_then_kills_if_needed(monkeypatch):
    proc=Mock(pid=123,returncode=-9)
    proc.communicate.side_effect=[subprocess.TimeoutExpired('x',300), subprocess.TimeoutExpired('x',10), ('partial','err')]
    killed=[];monkeypatch.setattr(h.os,'killpg',lambda pid,sig:killed.append((pid,sig)))
    out,err,timed=h.communicate(proc,'prompt')
    assert timed and (out,err)==('partial','err')
    assert killed==[(123,h.signal.SIGTERM),(123,h.signal.SIGKILL)]


def test_sanitizer_preserves_denials_and_removes_only_thinking():
    events=h.sanitize('{"type":"assistant","message":{"content":[{"type":"thinking","thinking":"private"},{"type":"tool_use","name":"Read","id":"x"}]}}\n{"type":"user","message":{"content":[{"type":"tool_result","is_error":true,"content":"denied"}]}}')
    assert events[0]['message']['content']==[{'type':'tool_use','name':'Read','id':'x'}]
    assert events[1]['message']['content'][0]['content']=='denied'


def test_audit_packager_refuses_incomplete_runs_before_creating_packet(tmp_path, monkeypatch):
    module_spec = importlib.util.spec_from_file_location('comparison_audit_packager', Path(__file__).with_name('prepare_audits.py'))
    packager = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(packager)
    run = tmp_path / 'run'; run.mkdir(); (run / 'receipts.json').write_text('[]')
    monkeypatch.setattr(packager, 'RUN', run)
    monkeypatch.setattr(packager, 'AUDITS', tmp_path / 'audits')
    with pytest.raises(RuntimeError, match='twelve'):
        packager.prepare()
    assert not (tmp_path / 'audits').exists()


def test_revision_blinding_removes_only_runtime_read_results(tmp_path):
    import json
    module_spec = importlib.util.spec_from_file_location('comparison_audit_blinding', Path(__file__).with_name('prepare_audits.py'))
    packager = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(packager)
    work=tmp_path/'project'; skill=work/'skill/engineering-research';skill.mkdir(parents=True)
    secret='DISTINCTIVE_NEW_REVISION_WORDING'
    (skill/'SKILL.md').write_text(secret)
    events=[
      {'type':'assistant','message':{'content':[{'type':'tool_use','id':'s','name':'Read','input':{'file_path':str(skill/'SKILL.md')}}]}},
      {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':'s','content':'1→'+secret,'is_error':False}]},'tool_use_result':{'type':'text','file':{'filePath':str(skill/'SKILL.md'),'content':secret,'numLines':1}}},
      {'type':'assistant','message':{'content':[{'type':'tool_use','id':'u','name':'Read','input':{'file_path':str(work/'saved.md')}}]}},
      {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':'u','content':'ACTUAL_SAVED_FINDING','is_error':False}]},'tool_use_result':{'file':{'content':'ACTUAL_SAVED_FINDING'}}},
      {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':'denied','content':'outside path denied','is_error':True}]}}
    ]
    raw=''.join(json.dumps(e)+'\n' for e in events)
    redacted,receipt=packager.mask_skill_reads(raw,work)
    assert secret not in redacted and 'ACTUAL_SAVED_FINDING' in redacted and 'outside path denied' in redacted
    actual=[json.loads(l) for l in redacted.splitlines()]
    assert len(actual)==len(events)
    assert actual[0]==events[0] and actual[2:]==events[2:]
    assert actual[1]['message']['content'][0]['tool_use_id']=='s'
    assert actual[1]['message']['content'][0]['is_error'] is False
    assert 'sha256' in actual[1]['message']['content'][0]['content']
    assert receipt['redacted_event_lines']==[2]
    assert redacted.splitlines()[2:]==raw.splitlines()[2:]
