"""One permitted command-construction experiment; never execute returned argv."""
import os
import sys
import tempfile
from pathlib import Path

scratch = Path(__file__).resolve().parent
project = scratch.parent
# Keep Git probes inside the empty fixture and away from user configuration.
os.environ["GIT_CONFIG_NOSYSTEM"] = "1"
os.environ["GIT_CONFIG_GLOBAL"] = "/dev/null"
os.environ["GIT_CEILING_DIRECTORIES"] = str(scratch)
sys.path.insert(0, str(project / "src" / "scripts"))
from run_package_tests import loom_family_commands

with tempfile.TemporaryDirectory(prefix="empty-preview-", dir=scratch) as directory:
    print(loom_family_commands(Path(directory), only="workflow-mermaid"))
