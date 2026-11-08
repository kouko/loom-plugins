"""Single permitted experiment: build Mermaid commands without executing them."""
import importlib.util
import os
from pathlib import Path
from tempfile import TemporaryDirectory

workspace = Path(__file__).resolve().parents[1]
# Keep the builder's read-only Git probes inside the empty scratch directory;
# disable system/global settings and inherited Git repository overrides.
os.environ.clear()
os.environ.update({
    "PATH": "/usr/bin:/bin",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CEILING_DIRECTORIES": str(workspace / "scratch"),
    "GIT_TERMINAL_PROMPT": "0",
})
spec = importlib.util.spec_from_file_location(
    "package_runner_preview", workspace / "src/scripts/run_package_tests.py"
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
with TemporaryDirectory(prefix="empty-preview-", dir=workspace / "scratch") as empty:
    print(runner.loom_family_commands(Path(empty), only="workflow-mermaid"))
