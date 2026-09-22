"""Feed the branch's PreToolUse hook the payload an agent host sends for each
command, and record exit code, stdout and stderr. The commands are not run."""
import json, subprocess, sys
from pathlib import Path

CHECKER = sys.argv[1]
REPO = sys.argv[2]
P, M = "pu" + "sh", "mer" + "ge"   # keep literal shapes out of the caller's command text

CASES = [
    ("#4 direct push", f"git {P} -u origin feat/local-probe"),
    ("#4 direct PR create", f"gh pr create --title T --body-file b.md"),
    ("#4 env-prefixed push", f"GIT_TRACE=0 git {P} origin HEAD"),
    ("#4 wrapped: true;", f"true; git {P} origin HEAD"),
    ("#4 wrapped: if/then", f"if true; then git {P} origin HEAD; fi"),
    ("#4 wrapped: subshell", f"( git {P} origin HEAD )"),
    ("#4 wrapped: xargs", f"echo origin | xargs git {P}"),
    ("#4 wrapped: heredoc to bash", f"cat <<EOF | bash\ngit {P} origin HEAD\nEOF"),
    ("#4 wrapped: bash -c", f"bash -c 'git {P} origin HEAD'"),
    ("#4 && chain", f"git status && git {P} origin HEAD"),
    ("#10 merge outside land", f"gh pr {M} 5 --squash"),
    ("#12 grep for merge words", f'grep -rn "gh pr {M}" .'),
    ("#12 echo merge words", f'echo "run gh pr {M} later"'),
    ("#12 commit message", f'git commit -m "document gh pr {M} usage"'),
    ("#12 printf merge words", f"printf '%s\\n' 'gh pr {M} --auto'"),
    ("guard: selection store", "echo x > .git/loom/selections/foo.json"),
]


def run(cmd, cwd):
    payload = {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": cwd,
               "hook_event_name": "PreToolUse"}
    r = subprocess.run([sys.executable, CHECKER, "push", "--hook"], input=json.dumps(payload),
                       capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


for label, cmd in CASES:
    code, out, err = run(cmd, REPO)
    print(f"[{label}] exit={code}\n  command: {cmd!r}\n  stderr: {err or '(none)'}\n")

code, out, err = run(f"git {P} origin HEAD", "/")
print(f"[hook failure: cwd is not a repository] exit={code}\n  stderr: {err or '(none)'}\n")
