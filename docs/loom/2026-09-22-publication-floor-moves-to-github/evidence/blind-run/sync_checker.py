"""Update the test repository's copied checker files to a newer loom-plugins
HEAD, on a branch, through the GitHub contents API (gh api)."""
import base64, json, subprocess, sys

WT, BRANCH, REPO = sys.argv[1], sys.argv[2], "repos/kouko/loom-floor-test"
FILES = [
    "loom-code/scripts/loom_checker/command_handlers/github_rules.py",
    "loom-code/scripts/loom_checker/command_handlers/land.py",
    "loom-code/scripts/loom_checker/command_handlers/pr_floor.py",
]


def gh(*args, data=None):
    r = subprocess.run(["gh", "api", *args], input=data, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"gh api {args[:3]} failed: {r.stderr or r.stdout}")
    return json.loads(r.stdout) if r.stdout.strip() else None


main_sha = gh(f"{REPO}/git/ref/heads/main")["object"]["sha"]
gh("-X", "POST", f"{REPO}/git/refs", "-f", f"ref=refs/heads/{BRANCH}", "-f", f"sha={main_sha}")
for path in FILES:
    blob = gh(f"{REPO}/contents/{path}?ref={BRANCH}")["sha"]
    content = base64.b64encode(open(f"{WT}/{path}", "rb").read()).decode()
    body = json.dumps({"message": f"Update {path.rsplit('/', 1)[1]} to loom-plugins fc0019b9",
                       "content": content, "sha": blob, "branch": BRANCH})
    res = gh("-X", "PUT", f"{REPO}/contents/{path}", "--input", "-", data=body)
    print(path, "->", res["commit"]["sha"][:10])
print("branch head:", gh(f"{REPO}/git/ref/heads/{BRANCH}")["object"]["sha"])
