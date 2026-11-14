"""The plugin checker runtime is separate from a project's Python runtime."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


LAUNCHER = Path(__file__).resolve().parents[1] / "scripts" / "loom-python"


def fake_uv(tmp_path: Path) -> Path:
    tool_dir = tmp_path / "tools"
    tool_dir.mkdir()
    uv = tool_dir / "uv"
    uv.write_text(
        f"""#!{sys.executable}
import os, pathlib, sys, time
args = sys.argv[1:]
with open(os.environ['FAKE_UV_LOG'], 'a') as log:
    log.write(' '.join(args) + '\\n')
if args[:2] == ['python', 'install']:
    sys.exit(0)
if args[0] == 'venv':
    if os.environ.get('FAKE_UV_SLOW'):
        time.sleep(1)
    target = pathlib.Path(args[-1])
    (target / 'bin').mkdir(parents=True)
    (target / 'bin' / 'python').symlink_to(sys.executable)
    sys.exit(0)
if args[:2] == ['pip', 'install']:
    sys.exit(0)
sys.exit(9)
""",
        encoding="utf-8",
    )
    uv.chmod(0o755)
    return tool_dir


def run_launcher(tmp_path: Path, *args: str, tools: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["XDG_CACHE_HOME"] = str(tmp_path / "cache")
    env["FAKE_UV_LOG"] = str(tmp_path / "uv.log")
    env["PATH"] = f"{tools}:/usr/bin:/bin" if tools else "/usr/bin:/bin"
    return subprocess.run(["/bin/sh", str(LAUNCHER), *args], env=env, cwd=tmp_path,
                          text=True, capture_output=True)


def test_repair_then_ready_offline_uses_cached_interpreter(tmp_path: Path) -> None:
    tools = fake_uv(tmp_path)
    repaired = run_launcher(tmp_path, "--repair", "--list-rules", tools=tools)
    assert repaired.returncode == 0, repaired.stderr
    assert "contract.requires\t" in repaired.stdout
    log = (tmp_path / "uv.log").read_text()
    assert "python install 3.11" in log
    assert "PyYAML==6.0.2" in log

    offline = run_launcher(tmp_path, "--ready", "--list-rules")
    assert (offline.returncode, offline.stdout, offline.stderr) == (
        repaired.returncode, repaired.stdout, repaired.stderr
    )
    assert (tmp_path / "uv.log").read_text() == log


def test_ready_accepts_importable_newer_yaml_but_rejects_missing_yaml(tmp_path: Path) -> None:
    runtime = tmp_path / "cache" / "loom-code" / "python-3.11-pyyaml-6.0.2-v1"
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(runtime)], check=True)
    interpreter = runtime / "bin" / "python"
    site_packages = Path(subprocess.run(
        [str(interpreter), "-E", "-s", "-c", "import site; print(site.getsitepackages()[0])"],
        check=True, text=True, capture_output=True,
    ).stdout.strip())
    yaml_package = site_packages / "yaml"
    yaml_package.mkdir()
    (yaml_package / "__init__.py").write_text("__version__ = '6.0.3'\n")
    script = tmp_path / "yaml_version.py"
    script.write_text("import yaml; print(yaml.__version__)\n")

    usable = run_launcher(tmp_path, "--ready", "--script", str(script))
    assert (usable.returncode, usable.stdout, usable.stderr) == (0, "6.0.3\n", "")

    shutil.rmtree(yaml_package)
    missing = run_launcher(tmp_path, "--ready", "--script", str(script))
    assert missing.returncode == 86
    assert "runtime is missing or invalid" in missing.stderr


def test_missing_installer_and_corrupt_cache_are_bootstrap_errors(tmp_path: Path) -> None:
    missing = run_launcher(tmp_path, "--repair", "--list-rules")
    assert missing.returncode == 2
    assert "uv" in missing.stderr and "install" in missing.stderr.lower()
    assert "BLOCK " not in missing.stderr and "contract" not in missing.stderr.lower()

    runtime = tmp_path / "cache" / "loom-code" / "python-3.11-pyyaml-6.0.2-v1"
    (runtime / "bin").mkdir(parents=True)
    (runtime / "bin" / "python").write_text("broken")
    corrupt = run_launcher(tmp_path, "--ready", "--list-rules")
    assert corrupt.returncode == 86
    assert "--repair" in corrupt.stderr
    assert "BLOCK " not in corrupt.stderr

    no_home = subprocess.run(["/bin/sh", str(LAUNCHER), "--ready", "--list-rules"],
                             env={"PATH": "/bin"}, text=True, capture_output=True)
    assert no_home.returncode == 86
    assert "HOME or XDG_CACHE_HOME" in no_home.stderr


def test_script_mode_uses_runtime_and_preserves_script_exit(tmp_path: Path) -> None:
    script = tmp_path / "probe.py"
    script.write_text("import sys, yaml, tomllib; print(sys.executable); print(sys.argv[1:]); sys.exit(7)\n")
    result = run_launcher(tmp_path, "--repair", "--script", str(script), "--help", "space argument", tools=fake_uv(tmp_path))
    assert result.returncode == 7, result.stderr
    assert "/loom-code/python-3.11-pyyaml-6.0.2-v1/bin/python" in result.stdout
    assert "['--help', 'space argument']" in result.stdout


def test_launcher_help_and_invalid_calls_need_no_runtime(tmp_path: Path) -> None:
    for args in [("--help",), ("-h",), (), ("plan", "plan.md"),
                 (str(LAUNCHER.with_name("loom_checker.py")), "plan", "plan.md"),
                 ("--ready", "loom_checker.py", "plan", "plan.md"),
                 ("--repair", str(LAUNCHER.with_name("loom_checker.py")), "plan", "plan.md"),
                 ("--ready",), ("--help", "plan", "plan.md")]:
        result = run_launcher(tmp_path, *args)
        help_only = args in [("--help",), ("-h",)]
        assert result.returncode == (0 if help_only else 2), (args, result)
        output = result.stdout if help_only else result.stderr
        assert '"<loom-code>/scripts/loom-python" --repair plan "<path-to-plan.md>"' in output
        assert "Replace <loom-code>" in output
        assert "checker is selected automatically" in output
        assert "No validation" in output
        if args and args[0] in ("--ready", "--repair") and len(args) > 1:
            assert "omit" in output and "loom_checker.py" in output
    assert not (tmp_path / "cache").exists()


def test_checker_help_recovers_to_plan_validation(tmp_path: Path) -> None:
    tools = fake_uv(tmp_path)
    help_result = run_launcher(tmp_path, "--repair", "--help", tools=tools)
    assert help_result.returncode == 0, help_result.stderr
    assert "plan <path-to-plan.md>" in help_result.stdout
    assert "charter [--manifest" in help_result.stdout
    plan = tmp_path / "plan with spaces.md"
    plan.write_text("charter: 1.0\n## Task DAG\n**T1 Example** after: none\n- Files: src/a.py\n- Test: works\n- Risk: agent-decided — low\n")
    assert run_launcher(tmp_path, "--ready", "plan", str(plan)).returncode == 0
    plan.write_text(plan.read_text().replace("- Test: works\n", ""))
    invalid = run_launcher(tmp_path, "--ready", "plan", str(plan))
    assert invalid.returncode == 1 and "BLOCK plan.field-caps" in invalid.stderr
    assert run_launcher(tmp_path, "--ready", "plan", str(plan), "extra").returncode == 2


def test_all_command_help_uses_ready_runtime_without_repair(tmp_path: Path) -> None:
    tools = fake_uv(tmp_path)
    assert run_launcher(tmp_path, "--repair", "--list-rules", tools=tools).returncode == 0
    log = (tmp_path / "uv.log").read_text()
    commands = ("intent", "intents", "intake", "push", "publish", "delivery", "land",
                "sync-trunk", "github-rules", "pr-floor", "standing", "contract",
                "charter", "plan", "reviewer-count", "finalize-review")
    for command in commands:
        for flag in ("--help", "-h"):
            result = run_launcher(tmp_path, "--ready", command, flag)
            assert (result.returncode, result.stderr) == (0, ""), (command, flag, result)
            assert result.stdout.startswith(command + " — ")
    checked_help = run_launcher(tmp_path, "--ready", "--script", "checked_readonly.py", "--help")
    assert (checked_help.returncode, checked_help.stderr) == (0, "")
    assert checked_help.stdout.startswith("checked-readonly — ")
    assert (tmp_path / "uv.log").read_text() == log
    shutil.rmtree(tmp_path / "cache")
    result = run_launcher(tmp_path, "--ready", "push", "--help")
    assert result.returncode == 86 and not (tmp_path / "cache").exists()
    checked_missing = run_launcher(tmp_path, "--ready", "--script", "checked_readonly.py", "--help")
    assert checked_missing.returncode == 86 and not (tmp_path / "cache").exists()


def test_launcher_resolves_its_directory_when_called_by_path_name(tmp_path: Path) -> None:
    assert run_launcher(tmp_path, "--repair", "--list-rules", tools=fake_uv(tmp_path)).returncode == 0
    env = {**os.environ, "PATH": str(LAUNCHER.parent), "XDG_CACHE_HOME": str(tmp_path / "cache")}
    result = subprocess.run(["/bin/sh", "-c", "loom-python --ready --list-rules"],
                            env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert "contract.requires\t" in result.stdout


def test_checked_help_and_local_advice_need_only_standard_library(tmp_path: Path) -> None:
    consumer = LAUNCHER.with_name("checked_readonly.py")
    for args, code in ((["--help"], 0), (["plan"], 2)):
        result = subprocess.run([sys.executable, "-E", "-s", "-S", str(consumer), *args],
                                cwd=tmp_path, text=True, capture_output=True)
        assert result.returncode == code
        assert "No module named" not in result.stderr
        assert ("Suggested next step:" in result.stderr) == (code == 2)


def test_script_keeps_project_environment_without_importing_project_modules(tmp_path: Path) -> None:
    tools = fake_uv(tmp_path)
    assert run_launcher(tmp_path, "--repair", "--list-rules", tools=tools).returncode == 0
    project_path = tmp_path / "project-modules"
    project_path.mkdir()
    (project_path / "project_only.py").write_text("value = 1\n")
    script = tmp_path / "environment_probe.py"
    script.write_text(
        "import importlib.util, os, yaml\n"
        "assert os.environ['PYTHONPATH'] == os.environ['EXPECTED_PROJECT_PATH']\n"
        "assert os.environ['PYTHONHOME'] == 'project-python-home'\n"
        "assert os.environ['VIRTUAL_ENV'] == 'project-venv'\n"
        "assert importlib.util.find_spec('project_only') is None\n"
        "print('isolated with project environment intact')\n"
    )
    env = os.environ.copy()
    env.update(
        XDG_CACHE_HOME=str(tmp_path / "cache"), PATH="/usr/bin:/bin",
        PYTHONPATH=str(project_path), EXPECTED_PROJECT_PATH=str(project_path),
        PYTHONHOME="project-python-home", VIRTUAL_ENV="project-venv",
    )
    result = subprocess.run(
        ["/bin/sh", str(LAUNCHER), "--ready", "--script", str(script)],
        env=env, text=True, capture_output=True,
    )
    assert (result.returncode, result.stdout) == (0, "isolated with project environment intact\n"), result.stderr
    checked = subprocess.run(
        ["/bin/sh", str(LAUNCHER), "--ready", "--script", "checked_readonly.py",
         "contract", "--require", "2.0"],
        env=env, text=True, capture_output=True,
    )
    assert (checked.returncode, checked.stderr) == (0, ""), checked.stderr


def test_concurrent_repair_publishes_one_complete_runtime(tmp_path: Path) -> None:
    tools = fake_uv(tmp_path)
    env = os.environ.copy()
    env.update(
        XDG_CACHE_HOME=str(tmp_path / "cache"), FAKE_UV_LOG=str(tmp_path / "uv.log"),
        FAKE_UV_SLOW="1", PATH=f"{tools}:/usr/bin:/bin",
    )
    command = ["/bin/sh", str(LAUNCHER), "--repair", "--list-rules"]
    first = subprocess.Popen(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.1)
    second = subprocess.Popen(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for process in (first, second):
        out, err = process.communicate(timeout=10)
        assert process.returncode == 0, err
        assert "contract.requires\t" in out
    assert (tmp_path / "uv.log").read_text().count("pip install") == 1
