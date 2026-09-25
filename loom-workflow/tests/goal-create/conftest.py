"""Put the goal-create skill's scripts directory on sys.path.

The tests live in loom-workflow/tests/goal-create/, apart from the scripts they
import by bare module name, which stay in loom-workflow/skills/goal-create/scripts/.
"""

import sys
from pathlib import Path

# Importing the scripts must not leave __pycache__/ inside the skill folder,
# which the skill-folder structure hook forbids.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skills" / "goal-create" / "scripts"))
