# Grounded state prototype — local preflight only

Six fixed synthetic cases and a two-stage extraction/writing experiment were
prepared in `/private/tmp/loom-grounded-state-pilot-20261105/`. No actor model
call ran. Two automatic approval reviews rejected launching the native model
with workspace rule contents, including after the nine paths and their hashes
were compared with the earlier candidate resource manifest. The reviewer
distinguished permission for Claude Code to read the resources from explicit
authorization to transmit their full contents to the external provider.

The proposed model inputs are the nine current Loom intake skill/reference
files named in `run.py`, plus synthetic fixture requests and fixture documents.
All nine paths occur in `/private/tmp/loom-option-guidance-iterations/r5/candidate-manifest.json`,
and their current SHA-256 hashes match that manifest's source hashes. The
proposed model is native `claude-sonnet-5-5`; effort medium is requested.
No private instructions, memory, credentials or unrelated repository content
are intended to be included. The prototype is not connected to Loom hooks and
does not prove output interception.

The standalone local `gate.py` was exercised with five synthetic controls:
missing product value case, missing factual value, nonexistent quote, complete
flags with an explicit hold, and engineering exemption for product value
fields. These checks establish only how the supplied inputs affect this small
function. A deliberately invalid semantic mapping — the same real quote placed
in all fields — still passes. Literal quotation and field presence cannot prove
the contents support the assigned meanings, or that the model chose the right
change kind, missing-fact list or hold. The prototype has not been exercised
by a real model and is not a complete implementation of the Loom contract.

No package suite was run: no Loom production skill, rule or checker changed.
No publication, merge, installed-plugin change or confirmation was performed.
