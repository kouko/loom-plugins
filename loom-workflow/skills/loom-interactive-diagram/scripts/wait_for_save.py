"""Wait within one active turn for a stable content change to one diagram."""

import argparse
import hashlib
import math
import sys
import time
from pathlib import Path


def digest(path):
    try:
        return hashlib.sha256(path.read_bytes()).digest()
    except OSError as error:
        raise OSError(f"{path}: {error.strerror or error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diagram", type=Path, help="one existing diagram file")
    parser.add_argument("--timeout", type=float, default=120, help="maximum wait in seconds (default: 120)")
    parser.add_argument("--interval", type=float, default=0.2, help="poll interval in seconds (default: 0.2)")
    args = parser.parse_args()
    if not all(math.isfinite(value) and value > 0 for value in (args.timeout, args.interval)):
        parser.error("--timeout and --interval must be finite positive numbers")

    try:
        baseline = digest(args.diagram)
        print("READY", flush=True)
        deadline = time.monotonic() + args.timeout
        pending = None
        while time.monotonic() < deadline:
            time.sleep(min(args.interval, max(0, deadline - time.monotonic())))
            current = digest(args.diagram)
            if current == baseline:
                pending = None
            elif current == pending:
                print("CHANGED", flush=True)
                return 0
            else:
                pending = current
    except OSError as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    print("TIMEOUT", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
