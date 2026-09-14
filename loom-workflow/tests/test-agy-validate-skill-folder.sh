#!/usr/bin/env bash
# test-agy-validate-skill-folder.sh
#
# Pins the Antigravity CLI (agy) PreToolUse adapter for the flat-skill-folder
# rule: loom-workflow/hooks.json registers scripts/agy-validate-skill-folder.sh,
# which reads agy's camelCase payload and prints {"decision":"allow"|"deny"}.
#
# Usage:
#   bash loom-workflow/tests/test-agy-validate-skill-folder.sh

set -u

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ADAPTER="$PLUGIN_DIR/scripts/agy-validate-skill-folder.sh"
HOOKS_JSON="$PLUGIN_DIR/hooks.json"

PASS_COUNT=0
FAIL_COUNT=0
pass() { echo "PASS — $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "FAIL — $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/agy-skill-folder-test.XXXXXX")"
cleanup() { rm -rf "$TMP_ROOT"; }
trap cleanup EXIT

# Fixture: a flat skill inside a git repo that also ships the repo-level
# .claude hook copy, so the original validator's dedup short-circuit would fire.
REPO="$TMP_ROOT/repo"
mkdir -p "$REPO/.claude/hooks" "$REPO/plugin/skills/foo/assets"
printf '#!/bin/sh\nexit 0\n' > "$REPO/.claude/hooks/validate-skill-folder-structure.sh"
chmod +x "$REPO/.claude/hooks/validate-skill-folder-structure.sh"
printf -- '---\nname: foo\n---\n' > "$REPO/plugin/skills/foo/SKILL.md"
git -C "$REPO" init -q

# run_hook <stdin> — runs the adapter the way agy does (sh -c, cwd = plugin
# root); sets OUT and CODE.
run_hook() {
  OUT=$(cd "$PLUGIN_DIR" && printf '%s' "$1" | sh -c 'bash ./scripts/agy-validate-skill-folder.sh' 2>/dev/null)
  CODE=$?
}
decision() { printf '%s' "$OUT" | jq -r '.decision // empty' 2>/dev/null; }
reason() { printf '%s' "$OUT" | jq -r '.reason // empty' 2>/dev/null; }
payload() { jq -cn --arg k "$1" --arg p "$2" \
  '{toolCall:{name:"write_to_file",args:{($k):$p}},stepIdx:1,conversationId:"c",workspacePaths:[],transcriptPath:""}'; }

# --- hooks.json registration -------------------------------------------------
if [ -f "$HOOKS_JSON" ] && jq -e '
    .["loom-workflow-skill-folder"].PreToolUse[0]
    | (.matcher | test("write_to_file")) and (.matcher | test("replace_file_content"))
      and (.hooks[0].type == "command")
      and (.hooks[0].command | test("\\./scripts/agy-validate-skill-folder\\.sh"))
  ' "$HOOKS_JSON" >/dev/null 2>&1; then
  pass "hooks.json registers the adapter on agy file-write tools (PreToolUse)"
else
  fail "hooks.json missing or does not register ./scripts/agy-validate-skill-folder.sh on PreToolUse"
fi

# --- A7 positive: nested-skill-subfolder-write-denied ------------------------
# Cwd of the run is the plugin root (no .claude copy there), but the target is
# inside a repo that has one: the adapter must still enforce.
NESTED="$REPO/plugin/skills/foo/assets/sub/x.md"
run_hook "$(payload TargetFile "$NESTED")"
if [ "$CODE" -eq 0 ] && [ "$(decision)" = "deny" ] && reason | grep -q "assets/sub"; then
  pass "nested-skill-subfolder-write-denied (deny, reason names assets/sub)"
else
  fail "nested-skill-subfolder-write-denied: code=$CODE out=$OUT"
fi
if [ ! -e "$REPO/plugin/skills/foo/assets/sub" ]; then
  pass "adapter does not create the nested directory it checks"
else
  fail "adapter created $REPO/plugin/skills/foo/assets/sub"
fi

# Same nested target through each accepted path-arg key.
for key in AbsolutePath FilePath file_path path; do
  run_hook "$(payload "$key" "$NESTED")"
  if [ "$(decision)" = "deny" ]; then
    pass "nested write denied via args.$key"
  else
    fail "nested write via args.$key: out=$OUT"
  fi
done

# --- negative: flat-skill-file-write-allowed ---------------------------------
run_hook "$(payload TargetFile "$REPO/plugin/skills/foo/assets/x.md")"
if [ "$CODE" -eq 0 ] && [ "$(decision)" = "allow" ]; then
  pass "flat-skill-file-write-allowed"
else
  fail "flat-skill-file-write-allowed: code=$CODE out=$OUT"
fi

# A new file one level down in a brand-new subfolder is still flat.
run_hook "$(payload TargetFile "$REPO/plugin/skills/foo/references/y.md")"
if [ "$(decision)" = "allow" ]; then
  pass "new single-level subfolder write allowed"
else
  fail "new single-level subfolder write: out=$OUT"
fi

# --- non-skill path ----------------------------------------------------------
run_hook "$(payload TargetFile "$REPO/src/deep/nested/dir/file.py")"
if [ "$CODE" -eq 0 ] && [ "$(decision)" = "allow" ]; then
  pass "non-skill path allowed"
else
  fail "non-skill path: code=$CODE out=$OUT"
fi

# --- malformed / unrecognised stdin ------------------------------------------
for input in 'not json at all' '' '{"toolCall":{"name":"write_to_file","args":{"Other":"x"}}}'; do
  run_hook "$input"
  if [ "$CODE" -eq 0 ] && [ "$(decision)" = "allow" ]; then
    pass "unrecognised stdin allowed: '${input:0:30}'"
  else
    fail "unrecognised stdin '${input:0:30}': code=$CODE out=$OUT"
  fi
done

echo ""
echo "================================================================"
echo "Summary: ${PASS_COUNT} PASS / ${FAIL_COUNT} FAIL"
echo "================================================================"
[ "$FAIL_COUNT" -eq 0 ]
