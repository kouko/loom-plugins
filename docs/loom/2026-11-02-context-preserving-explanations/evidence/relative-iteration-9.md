# Relative iteration 9 — released baseline repeated

## Outcome

This round reran the released baseline (`41211a0b`) on the same eight
synthetic cases. On incomplete CSV it explicitly noted both missing product
answers, called them weak, and asked for confirmation anyway. Its reply added a
claim that CSV record counts match the list, unsupported by the case. The
unknown-date case created an open draft, asked for confirmation, and offered
the choice of guessing a date, while also saying guessing was not recommended.
In the preceding candidate rounds the unknown-date cases did not invent or
propose a date; the missing-answer case was handled inconsistently.

The explicitly held invoice case preserved the ongoing hold but its flow lacked
the newer titled outer frames. It stated that amounts would not change,
despite the request allowing amounts to differ. The natural-default invoice
disclosed push and PR after review and publication checks, plus a separate
merge decision, but described opting out at answer time rather than any time
before publication. The prior candidate samples generally disclosed the later
opt-out. The other capture-only wrappers have ambiguous publication duration;
their interpretation is not scored as a definite consent error. The two
ready code-only cases both wrote drafts before confirmation in this run.

The baseline and candidate each have factual and workflow failures. These
concrete observations support improvement on specific unknown-date and consent
details, not a universal quality claim. The same small fixed cases have been
reused throughout, results are author-reviewed, and this baseline run was not
contemporaneously randomized with candidate runs. A final candidate repeat is
planned before judging the evidence.

## Test

Eight fresh isolated native Claude Code sessions used the same synthetic
requests and first-party `claude-sonnet-5-5` at requested medium effort.
All receipts matched; isolation and original hook preflight passed, with no
permission denials or fixture commits observed. The CLI estimated cost was
USD 0.9482214. Source hashes, cases, replies, drafts and receipts are retained
in `relative-iteration-9-data.json`, with email-shaped strings redacted. Every
baseline resource path is within the previously listed candidate path set;
the content is from the prior released commit.
