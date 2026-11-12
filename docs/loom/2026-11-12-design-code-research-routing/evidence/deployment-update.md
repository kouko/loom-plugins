# Synthetic acceptance condition update

This is a controlled test input, not a claim about the user's real deployment.

The next evaluation targets a different deployment from the original local
machine: an existing shell script exports an existing UTF-8 text file on disk
as one ZIP member. The output directory is writable. The target provides
`/usr/bin/zip`; a Python runtime is absent, and adding a runtime is outside the
confirmed fixture scope. Original local round-trip observations remain valid
for their original environment; no remote deployment has been executed.

Use these as the new target's fixed conditions. Preserve the original research
basis and distinguish these supplied conditions from locally measured results.
