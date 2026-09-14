# PRE-EDIT RED WALK (recorded BEFORE any edit to schema.yaml)

Baseline text: `git show 22c15cf:superpowers-bridge/schema.yaml` checks 9-11
(byte-identical to the on-disk text at walk time; task 2.1 touched check 12 only).

Sentences applied:
- c9: "the lines belonging to it must include one `- RED:` line and one `- GREEN:` line"
- c9: "`- RED:` requires the fields `subject:`, `outcome:` and `failure:`. `- GREEN:` requires
  `subject:` and `outcome:`." / "A missing record, a missing required field, or a required
  field whose value is empty after trimming -> BLOCK."
- c10: "GREEN's `outcome:` value must be exactly the token `PASS`. RED's must be a single token
  of uppercase letters A-Z ... and must not be `PASS`"
- c11: "within one task, the RED record's `subject:` value and the GREEN record's `subject:`
  value must be identical character for character after ... trimmed. Any difference -> BLOCK."

## f10-subject-without-separator  (subject = `rejects empty email`, no `::`, same both sides)
c9  -> no finding: one RED, one GREEN; subject/outcome/failure all present and non-empty after
       trimming. The pre-edit text constrains a field VALUE only by "empty after trimming";
       no sentence in checks 9-11 mentions `::`, a separator, or any format.
c10 -> no finding: RED FAIL, GREEN PASS.
c11 -> no finding: the two subjects are identical character for character.
VERDICT: PASS.  EXPECTED: BLOCK naming the malformed subject.  WRONG.

## f11-duplicate-subject-one-side  (two REDs, identical subjects; one GREEN, same subject)
c9  -> no finding under the reading the fixtures were authored to ("must include one RED and one
       GREEN" = at least one): both present, every field present and non-empty.
c10 -> no finding: both REDs FAIL, GREEN PASS.
c11 -> no finding: whichever RED "the RED record" designates, its subject equals the GREEN's.
VERDICT: PASS.  EXPECTED: BLOCK naming the duplicated subject.  WRONG - no sentence in checks
9-11 mentions uniqueness or per-subject cardinality at all.
(Under a strict "exactly one" reading of c9 this would BLOCK, but for the wrong reason - record
count, not the duplicated subject - and the same reading would also block f12, the positive
control. That is why the ambiguity is settled in terms of subjects, not raw record counts.)

## f12-two-subjects-paired  (POSITIVE CONTROL: two distinct subjects, each fully paired)
c9  -> no finding (at-least-one reading). Under "exactly one" it would BLOCK - wrong for a
       positive control.
c10 -> no finding.
c11 -> INDETERMINATE. The sentence "the RED record's `subject:` value and the GREEN record's
       `subject:` value" uses the definite singular over a task holding two RED records and two
       GREEN records. Pairing RED#1 with GREEN#1 and RED#2 with GREEN#2 yields no difference;
       pairing RED#1 with GREEN#2 yields a difference and therefore BLOCK. The pre-edit text
       supplies no rule for choosing, so two executors reading it can reach opposite verdicts.
VERDICT: indeterminate (not PASS, not BLOCK).  EXPECTED: no finding from checks 9-11.  WRONG -
the check cannot decide the case at all.
