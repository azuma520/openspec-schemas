## ADDED Requirements

### Requirement: REQ-1 Each bundle release from 4.0.0 is marked by a same-version tag on its release commit

Every `superpowers-bridge` bundle release from `4.0.0` onward SHALL be marked by an annotated Git tag named `v` followed by the exact `VERSION` value (`v4.0.0` for bundle `4.0.0`). The tag SHALL point at the release commit: the final commit, published to `main`, made after the change carrying the release has been archived, finally verified, and every release-coupled document updated — which is not necessarily the archive commit. A release SHALL count as complete only when the remote tag, peeled to the commit it points at, is confirmed equal to the recorded release commit SHA; a lookup that returns the annotated tag object's own SHA SHALL NOT count as that confirmation. Pushing the tag is a controlled git operation and SHALL be authorised by the user for that push.

Releases before `4.0.0` are out of scope: they carry no tags, and none SHALL be created for them retroactively, because which commit was each such release is not established by evidence.

Tagging happens after archive, so the completion condition SHALL be carried outside the change's tasks.md — on the change's work-map record, which SHALL NOT be marked done until the remote tag is confirmed.

#### Scenario: REQ-1-S1 Release completes on a confirmed remote tag

- **WHEN** bundle `4.0.0` is released, the annotated tag `v4.0.0` is pushed, and the remote ref `refs/tags/v4.0.0^{}` resolves to the recorded release commit SHA
- **THEN** the release is complete and its work-map record may be marked done

#### Scenario: REQ-1-S2 Unpeeled tag SHA is not confirmation

- **WHEN** the remote lookup returns the SHA of the tag object itself rather than of the commit it points at
- **THEN** that lookup is not accepted as confirming the release, and the work-map record stays not done

#### Scenario: REQ-1-S3 Earlier releases are not back-tagged

- **WHEN** the repository has no tag for bundle `3.0.0` or any earlier release
- **THEN** no tag is created for those releases as part of releasing `4.0.0`

### Requirement: REQ-2 Release documentation states the tag rule, not a tag event

The bridge README (en and zh-TW) SHALL describe bundle release tagging as a rule — each bundle release is marked by a same-version Git tag `vX.Y.Z`, a discipline actually practised from bundle `4.0.0` — and SHALL NOT state that a particular tag has been created, because the commit that carries the statement exists before its own tag can. Statements that a tag exists which the repository does not hold SHALL be removed where this change edits them, including the existing claims about `v3.0.0`.

#### Scenario: REQ-2-S1 README makes no claim about a tag that does not exist

- **WHEN** the README describes the current bundle release and the Versioning table describes bundle releases
- **THEN** neither states that a specific tag was created, and both read true both before and after that release's tag is pushed

### Requirement: REQ-3 A Compatibility baseline date records a full cycle against the row's listed versions

A "Baseline as of" date written into the bridge README's Compatibility table by this change or any later change SHALL be the date a maintainer re-ran a full cycle against the versions listed in that same row and confirmed nothing degraded. Until such a run exists the cell SHALL hold `pending` as plain text, and a run against versions other than those listed in the row SHALL NOT be grounds to fill it. The v4 row SHALL list the Superpowers version `v5.1.0` as an unrevalidated historical declaration, explained below the table rather than inside the cell, and that explanation SHALL state that it is not a compatibility guarantee.

The existing v2 and v3 row dates are outside this requirement: they are CLI-level attestations, already documented as such, and this change does not rewrite them.

#### Scenario: REQ-3-S1 Dogfood on another Superpowers version does not fill the date

- **WHEN** the v4 row lists Superpowers `v5.1.0` and this change's dogfood runs on a different loaded Superpowers version
- **THEN** the v4 row's "Baseline as of" stays `pending`

#### Scenario: REQ-3-S2 Weekly version check still reads the row

- **WHEN** the v4 row's date cell holds `pending` and its explanation sits below the table
- **THEN** the weekly version check reads the v4 row's OpenSpec and Superpowers versions correctly

### Requirement: REQ-4 Rollback instructions point only at refs that exist

Rollback instructions written by this change or any later change SHALL reference only a tag or commit that exists in the repository. The v3 → v4 rollback SHALL name the full SHA of the parent of the first commit that sets `schema.yaml` to `version: 4`, and that SHA SHALL be checked out once to confirm it yields the v3 bundle before verify passes; no placeholder SHALL remain.

The existing v1 → v2 and v2 → v3 rollback instructions, which name bundle versions that have no tags, are outside this requirement and are recorded as an observation rather than rewritten here.

#### Scenario: REQ-4-S1 v3 rollback SHA is real and checked

- **WHEN** the v3 → v4 rollback instruction is finalised
- **THEN** it names a full commit SHA, checking that SHA out yields `superpowers-bridge/schema.yaml` with `version: 3`, and no placeholder text remains

#### Scenario: REQ-4-S2 No rollback to an absent tag

- **WHEN** the v3 → v4 rollback instruction is written and the repository holds no `v3.x.y` tag
- **THEN** the instruction does not tell the reader to pin a `3.x.y` bundle by tag
