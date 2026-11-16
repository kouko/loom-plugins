# Build integration observations

- Base origin/main: 9bbab926b5224456a467fdfd7d8f1306b9cb54b9.
- Initial sync-trunk returned WARN because sandbox denied FETCH_HEAD; authorized
  retry of the same installed command confirmed up to date at 0ceed532.
- Initial package launch failed before tests because sandbox denied uv cache
  lock creation. Authorized identical retry ran the package inventory.
- First executed group: 2855 passed, 2 failed in 116.12s; runner exited1 before
  subsequent groups. Full log is package-first-run.log, not a full-suite pass.
- Both failures are stale active mechanism census records: missing roadmap
  registration and deleted decision-map eval path. Repair stays in Build;
  checker/test assertions are not weakened. Re-run full suite after repair.
- Adversary found five attack points, no successful attack, reused
  loom-code/tests/test_loom_checker_intent.py (65 cases) with a concern marker.
  Its semantic temptation run is separate from the executable finalizer probe.
