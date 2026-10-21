"""The plugin checker runtime is separate from a project's Python runtime."""
from __future__ import annotations

import os
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
    return subprocess.run(["/bin/sh", str(LAUNCHER), *args], env=env, text=True, capture_output=True)


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
    script.write_text("import sys, yaml, tomllib; print(sys.executable); sys.exit(7)\n")
    result = run_launcher(tmp_path, "--repair", "--script", str(script), tools=fake_uv(tmp_path))
    assert result.returncode == 7, result.stderr
    assert "/loom-code/python-3.11-pyyaml-6.0.2-v1/bin/python" in result.stdout


def test_launcher_resolves_its_directory_when_called_by_path_name(tmp_path: Path) -> None:
    assert run_launcher(tmp_path, "--repair", "--list-rules", tools=fake_uv(tmp_path)).returncode == 0
    env = {**os.environ, "PATH": str(LAUNCHER.parent), "XDG_CACHE_HOME": str(tmp_path / "cache")}
    result = subprocess.run(["/bin/sh", "-c", "loom-python --ready --list-rules"],
                            env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert "contract.requires\t" in result.stdout


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
