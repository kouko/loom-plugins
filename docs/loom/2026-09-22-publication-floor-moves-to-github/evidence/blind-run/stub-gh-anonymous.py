#!/usr/bin/env python3
"""Stand-in for `gh api <path> [--hostname h] [-H hdr]` that calls GitHub
anonymously, to see what a caller without write access is shown."""
import sys, urllib.request, urllib.error

args = sys.argv[1:]
if not args or args[0] != "api":
    sys.exit("anon gh: only `api` is supported")
path = args[1]
headers = {"User-Agent": "loom-blind-run"}
if "-H" in args:
    k, v = args[args.index("-H") + 1].split(": ", 1)
    headers[k] = v
req = urllib.request.Request("https://api.github.com/" + path, headers=headers)
try:
    with urllib.request.urlopen(req) as r:
        sys.stdout.write(r.read().decode())
except urllib.error.HTTPError as e:
    body = e.read().decode()
    sys.stderr.write(f"gh: {body} (HTTP {e.code})\n")
    sys.exit(1)
