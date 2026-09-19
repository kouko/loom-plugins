# Adversarial — spec

The attack recipe for a spec. Read it together with the shared protocol in
[`adversarial.md`](adversarial.md).

## Spec

Red-team it: for each `REQ-<n>`, name a behaviour the requirement permits
that the author clearly did not want. Then look for the states the spec
never mentions — the second user, the interrupted run, the empty account,
the migration from what exists today. Each one is a finding with the
requirement as its anchor.
