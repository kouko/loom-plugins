"""Offline launch/isolation controls; model requests are never run by these tests."""
from pathlib import Path
import importlib.util
import pytest

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('save_probe_public',HERE/'public_runner.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


def test_public_command_has_only_explicit_mcp_and_confined_file_tools(tmp_path):
    cmd=p.command(tmp_path,'public prompt')
    assert '--safe-mode' not in cmd and '--restricted' in cmd
    assert cmd[cmd.index('--tools')+1]=='Read,Grep,Glob'
    assert cmd[cmd.index('--allowedTools')+1]=='Read,Grep,Glob,mcp__save_probe__save_record'
    assert '--strict-mcp-config' in cmd and '--disable-slash-commands' in cmd
    assert cmd[cmd.index('--model')+1]=='claude-sonnet-5-5'
    assert cmd[cmd.index('--effort')+1]=='medium'
    assert cmd[cmd.index('--setting-sources')+1]==''
    assert not any(x in ','.join(cmd) for x in ['Bash','Write,','Edit,','Agent,','Skill,'])


def test_environment_omits_provider_proxy_and_credential_vars():
    env=p.environment({'PATH':'path','HOME':'other','HTTPS_PROXY':'bad','ANTHROPIC_API_KEY':'credential','ANTHROPIC_BASE_URL':'proxy','SECURITYSESSIONID':'normal'})
    assert env=={'PATH':'path','HOME':'/Users/kouko','SECURITYSESSIONID':'normal','PYTHONDONTWRITEBYTECODE':'1'}


def test_public_overwrite_prevention(tmp_path):
    (tmp_path/'started.json').write_text('{}')
    with pytest.raises(RuntimeError,match='overwrite'):p.require_fresh(tmp_path)


def paired():
    s=importlib.util.spec_from_file_location('save_probe_pair',HERE/'paired_experiment.py')
    module=importlib.util.module_from_spec(s);s.loader.exec_module(module)
    return module


def test_case_write_policies_keep_originals_and_instance_copy_boundary():
    q=paired()
    assert q.policy_for('F03','full','/project')=={'root':'/project','result_mode':'full'}
    assert q.policy_for('F06','full','/project')['create_files']==['fixtureVault/research/2026-11-08-package-test-roots.md']
    assert 'create_roots' not in q.policy_for('F06','full','/project')
    assert q.policy_for('F01','confirmation','/project')['update_files']==['docs/loom/research/2026-11-08-package-test-roots.md']
    assert 'update_files' not in q.policy_for('F04','full','/project')


def test_common_actor_adapter_has_no_mode_labels_or_readback_coaching():
    q=paired();text=q.actor_prompt('COMMON','CASE')
    assert text.startswith('COMMON\nCASE\n')
    assert not any(x in text.lower() for x in ['confirmation','full-result','baseline','treatment','rubric','read back'])
    assert 'save_record' in text


def test_pair_run_refuses_changed_frozen_dependency(tmp_path,monkeypatch):
    q=paired();run=tmp_path/'run';run.mkdir();dependency=tmp_path/'source.py';dependency.write_text('changed')
    import json
    (run/'freeze.json').write_text(json.dumps({'dependencies':{str(dependency):'not-the-hash'}}))
    monkeypatch.setattr(q,'RUN',run)
    with pytest.raises(RuntimeError,match='dependency drift'):q.validate_freeze()
