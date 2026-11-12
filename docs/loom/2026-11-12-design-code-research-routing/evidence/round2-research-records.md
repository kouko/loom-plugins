# Round 2 actual trial snapshots

These are direct Markdown snapshots of inspected external trial artifacts and newly saved/read-back clean-copy research. External originals were not repository artifacts. Code is fenced evidence, not a new executable harness. Cold actor initial execution provenance is supplied by the parent; witness independently inspected substantive content and reran the bounded operation.

## /private/tmp/loom-initial-choice-_azq987_/request.md

```text
# Local text export request

We need to export receipt.txt as a ZIP archive containing one member named
receipt.txt, with the text bytes preserved and the source file untouched.
Compare practical implementations available on this machine and recommend an
approach supported by the evidence. Bounded local checks in temporary files
are permitted. Do not install software or change a real project implementation.
Keep an inspectable research record with the recommendation and its limits.

```

## /private/tmp/loom-initial-choice-_azq987_/docs/loom/research/2026-11-12-receipt-zip-choice.md

```text
---
title: "Choose a local receipt ZIP export implementation"
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags:
  - loom/research
---

# Choose a local receipt ZIP export implementation

## Question and scope

Which implementation available on this machine can export the supplied receipt.txt as a ZIP with exactly one member named receipt.txt, preserving its bytes and leaving the source untouched? This is standalone research; no implementation change or installation is authorized. The intended caller/runtime and output-collision policy are unspecified.

## Method and rationale

A lightweight trade study with a bounded local experiment fits this small capability question. Mandatory criteria are exact member list, equal extracted bytes, and unchanged source contents; also inspect modification time and mode. Compare available Python standard-library zipfile and the system zip command under the same source and fresh temporary destinations. Stop when both have directly inspected results. No external search is needed for this installed-machine question. No performance ranking is required or measured.

## Findings

Observed on macOS 26.7 arm64: Python 3.15.2 is available at /opt/homebrew/bin/python3; /usr/bin/zip reports Info-ZIP 3.0 with Apple modifications. Both tested implementations produced exactly ['receipt.txt'], reproduced all 11 source bytes including the non-ASCII character, and had no CRC error reported by Python's ZIP reader. Source bytes, modification time and mode matched before and after each operation.

| Candidate | Tested operation | Practical tradeoff |
|---|---|---|
| Python zipfile | ZipFile(destination, 'x', compression=ZIP_DEFLATED), then write(source, arcname='receipt.txt') | Explicit member name; used without invoking a separate archiver process. Fits a Python caller. |
| System zip | /usr/bin/zip -j fresh-destination.zip /absolute/path/receipt.txt | A short shell command; fits a terminal or shell caller. Requires a fresh output to avoid retaining unrelated existing members. |

The caller context is missing, so these observations establish feasibility, not a universal winner. The simplicity judgments in the table are inference from the tested operations, not timing measurements.

## Evidence

- [Request](../../../request.md) and [source receipt](../../../receipt.txt) were read directly. The source SHA-256 observed was 50e6cdc2df5a6604eb1c12a9acd030293fe2b9d5d42c83f7b572e0c9b780d0e7.
- Installed availability/version commands: `command -v python3 zip ditto node`, `python3 --version`, and `zip -v`. These also found ditto and node, but those were not evaluated; this is a comparison of two credible options, not an exhaustive inventory.
- [Executable probe](../../../probe.py) preserves the actual operations and validation logic. Command: `python3 /private/tmp/loom-initial-choice-_azq987_/probe.py > /private/tmp/loom-initial-choice-_azq987_/probe-results.json`.
- [Saved observed results](../../../probe-results.json) were read in full: both exit codes 0, one exact member each, payload equality true, bad_crc_member null, and all three source-preservation checks true. Temporary archives were deleted when the probe finished. This is runtime evidence, not historical deployment evidence or upstream implementation verification.

## Decision impact

For a one-off terminal export to a new archive, recommend `/usr/bin/zip -j NEW-ARCHIVE.zip /absolute/path/receipt.txt`: the bounded experiment supports the exact required contents with a short available command. If this export belongs inside a Python workflow, prefer the tested zipfile operation with explicit arcname and exclusive creation instead. Neither choice is shown superior across unknown caller contexts. Confirm the target caller and existing-output handling before selecting an application integration; do not reuse an arbitrary existing ZIP and assume it will contain only this member.

## Limitations and open questions

Only this 11-byte input, ordinary local paths, and fresh writable destinations were tested. Access time was not asserted unchanged; reading can affect it. The experiment does not establish all metadata preservation, crash safety, concurrency behavior, large-file performance, permissions-error handling, compatibility with external extractors, or how an existing output should be handled. The system-zip archives were validated with Python's reader, so the checks are not independent implementations for every candidate. No real export was retained or production implementation changed. Revalidate for a different caller, environment or collision policy.

```

## /private/tmp/loom-initial-choice-_azq987_/probe.py

```text
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile

source = Path(__file__).parent / 'receipt.txt'
before = source.read_bytes()
stat = source.stat()
results = []
with tempfile.TemporaryDirectory(prefix='receipt-zip-check-') as temporary:
    root = Path(temporary)
    for candidate in ('python-zipfile', 'system-zip'):
        archive = root / (candidate + '.zip')
        if candidate == 'python-zipfile':
            command = 'ZipFile(archive, "x", compression=ZIP_DEFLATED).write(source, arcname="receipt.txt")'
            with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as output:
                output.write(source, arcname='receipt.txt')
            exit_code = 0
        else:
            command = [shutil.which('zip'), '-j', str(archive), str(source)]
            process = subprocess.run(command, capture_output=True, text=True)
            exit_code = process.returncode
        with zipfile.ZipFile(archive) as output:
            members = output.namelist()
            same = output.read('receipt.txt') == before
            integrity = output.testzip()
        after_stat = source.stat()
        results.append(dict(candidate=candidate, command=command, exit_code=exit_code,
                            members=members, payload_equal=same, bad_crc_member=integrity,
                            source_bytes_unchanged=source.read_bytes() == before,
                            source_mtime_unchanged=stat.st_mtime_ns == after_stat.st_mtime_ns,
                            source_mode_unchanged=stat.st_mode == after_stat.st_mode))
print(json.dumps(dict(python=sys.version, platform=platform.platform(),
                     source_bytes=len(before), source_sha256=hashlib.sha256(before).hexdigest(),
                     results=results), indent=2))

```

## /private/tmp/loom-initial-choice-_azq987_/probe-results.json

```text
{
  "python": "3.15.2 (main, Oct 25 2026, 16:57:51) [Clang 21.0.0 (clang-2100.3.34.2)]",
  "platform": "macOS-26.7-arm64-arm-64bit-Mach-O",
  "source_bytes": 11,
  "source_sha256": "50e6cdc2df5a6604eb1c12a9acd030293fe2b9d5d42c83f7b572e0c9b780d0e7",
  "results": [
    {
      "candidate": "python-zipfile",
      "command": "ZipFile(archive, \"x\", compression=ZIP_DEFLATED).write(source, arcname=\"receipt.txt\")",
      "exit_code": 0,
      "members": [
        "receipt.txt"
      ],
      "payload_equal": true,
      "bad_crc_member": null,
      "source_bytes_unchanged": true,
      "source_mtime_unchanged": true,
      "source_mode_unchanged": true
    },
    {
      "candidate": "system-zip",
      "command": [
        "/usr/bin/zip",
        "-j",
        "/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/receipt-zip-check-rmk9godm/system-zip.zip",
        "/private/tmp/loom-initial-choice-_azq987_/receipt.txt"
      ],
      "exit_code": 0,
      "members": [
        "receipt.txt"
      ],
      "payload_equal": true,
      "bad_crc_member": null,
      "source_bytes_unchanged": true,
      "source_mtime_unchanged": true,
      "source_mode_unchanged": true
    }
  ]
}

```

## docs/loom/research/2026-11-12-witness-round2-design-choice.md

```text
---
title: Recovery behavior comparison with unknown accessibility context
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

## Question and scope
Re-run original D1 synthetic design decision: prevent accidental removal while
preserving keyboard work. Compare modal confirmation, reversible inline undo,
and immediate removal. No implementation, interview or confirmation authorized.
Unknown decision-critical context: screen-reader announcement and focus recovery
of the candidate implementations. A conditional design conclusion is required.

## Method and rationale
Read original fixture observation and interview; compare common recovery,
focus continuity and accessibility criteria. Necessary: pointer-free recovery.
Preference: perceived safety. Reported preference is not observed success.
Stop with uncertainty because no authorized prototype observation settles it.

## Findings
Synthetic three-operator observation reports modal focus loss and draft loss;
one interviewee reports preferring modal safety. Neither proves all modal
implementations fail or that untested inline undo announces correctly.
Immediate removal lacks the required recovery. For a verified keyboard workflow
with discoverable focused undo, inline undo could preserve recovery and flow.
If announcement/focus recovery is unreliable, inline undo is not established
adequate; an accessible confirmation or redesigned recovery needs evaluation.
No unconditional winner is supported for the unspecified accessibility context.

## Evidence
[Original synthetic input](../2026-11-12-design-code-research-routing/evidence/fixture-sources.md)
read in full. Context is synthetic operators, 2026-11-12; no real users observed,
no prototype operated. Separate facts, interview claims and conditional inference.

## Decision impact
Return conditional alternatives and missing accessibility evidence to original
design task. Preserve confirmed goal and user decisions, do not ratify or advance
confirmation. Overall recovery architecture does not establish nested component
quality; neither tool used for research nor interview preference settles it.

## Limitations and open questions
Screen-reader/focus behavior remains unknown. D2's separately fixed undo choice
is not reopened. No population-wide or cross-model quality claim follows.

```

## docs/loom/research/2026-11-12-witness-round2-engineering-choice.md

```text
---
title: Receipt ZIP comparison without assuming caller context
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

## Question and scope
Choose installed local receipt ZIP implementation; exact one receipt.txt member,
same bytes, unchanged source. Caller/runtime and collision policy unspecified;
do not infer caller from Python used by this investigation. No implementation,
installation or external action authorized. This is a separate re-run record,
not replacement of the first trial's unsupported assumption and withdrawal.

## Method and rationale
Matched bounded experiment for two credible material nested writer choices:
Python zipfile versus system zip. Common mandatory checks: exact member list,
payload, CRC reader outcome, source bytes/mtime/mode unchanged. No speed score
or feature-count ranking. Stop when bounded feasibility established.

## Findings
Witness reran the inspected cold actor's probe: Python 3.15.2, macOS 26.7 arm64,
11 source bytes, both exit 0, exact ['receipt.txt'], payload equality true,
CRC bad member null, source bytes/mtime/mode checks all true. This is a real
fresh local execution, not proof of deployment or every input.

## Evidence
Inspected /private/tmp/loom-initial-choice-_azq987_/request.md, receipt.txt,
probe.py, probe-results.json and saved research record in full. Executed
`python3 /private/tmp/loom-initial-choice-_azq987_/probe.py` from clean copy.
Output source hash 50e6cdc2df5a6604eb1c12a9acd030293fe2b9d5d42c83f7b572e0c9b780d0e7.
Archives used fresh temporary names and were deleted by the existing probe.
These external files are inspected trial artifacts, not committed repo files;
direct Markdown snapshots retained with acceptance evidence preserve their data.

## Decision impact
If terminal/shell one-off to a new output, use installed zip -j with the source
absolute path. If integrated into existing Python workflow, use zipfile explicit
arcname and exclusive creation. Caller context can reverse preference, so no
unconditional integration recommendation is supported. Both meet bounded
requirements; overall local-export integration does not prove nested winner.
Return conditional choices and unknown caller/collision policy to task without
changing confirmed goal, scope, authorization or any human decision point.

## Limitations and open questions
Only one 11-byte input and fresh writable outputs tested. No access-time,
concurrency, existing-output, large-file, external-reader, speed or crash claim.
Cold actor provenance is supplied by station; witness independently inspected
its retained content and reran operations, not its original host execution trace.

```


