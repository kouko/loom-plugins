import importlib.util
import json
import tempfile
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'src/scripts/run_package_tests.py'
spec = importlib.util.spec_from_file_location('package_runner_preview', source)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
with tempfile.TemporaryDirectory(dir=Path(__file__).parent, prefix='empty-') as root:
    print(json.dumps(runner.loom_family_commands(Path(root), only='workflow-mermaid'), ensure_ascii=False, indent=2))
