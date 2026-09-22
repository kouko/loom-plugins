#!/usr/bin/env python3
"""Stand-in gh: a GitHub repository whose trunk has no loom-pr-floor.yml."""
import json, sys

path = sys.argv[2] if len(sys.argv) > 2 else ""
if "/contents/" in path:
    sys.stderr.write("gh: Not Found (HTTP 404)\n")
    sys.exit(1)
if path.count("/") == 2:
    print(json.dumps({"default_branch": "main"}))
    sys.exit(0)
sys.stderr.write(f"stand-in gh: unexpected call {sys.argv[1:]}\n")
sys.exit(1)
