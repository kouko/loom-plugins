#!/bin/sh
# Wait until a new completed "loom-pr-floor / PR floor" run appears on commit $1
# beyond the $2 runs already counted; print every run as id|status|conclusion.
i=0
while [ $i -lt 30 ]; do
  out=$(gh api "repos/kouko/loom-floor-test/commits/$1/check-runs?per_page=50" \
    --jq '[.check_runs[] | "\(.id)|\(.name)|\(.status)|\(.conclusion)|\(.started_at)"]')
  n=$(printf '%s' "$out" | python3 -c "import json,sys;print(len(json.load(sys.stdin)))")
  done_n=$(printf '%s' "$out" | python3 -c "import json,sys;print(sum(1 for r in json.load(sys.stdin) if '|completed|' in r))")
  if [ "$n" -gt "$2" ] && [ "$done_n" -eq "$n" ]; then
    printf '%s\n' "$out"
    exit 0
  fi
  i=$((i+1))
  sleep 8
done
echo "timeout; last: $out"
