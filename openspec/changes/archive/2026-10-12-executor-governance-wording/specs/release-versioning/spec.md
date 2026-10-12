## MODIFIED Requirements

### Requirement: REQ-3 A Compatibility baseline date records a full cycle against the row's listed versions

A "Baseline as of" date written into the bridge README's Compatibility table by this change or any later change SHALL be the date a maintainer re-ran a full cycle against the versions listed in that same row and confirmed nothing degraded. Until such a run exists the cell SHALL hold `pending` as plain text, and a run against versions other than those listed in the row SHALL NOT be grounds to fill it. The v4 row SHALL list the Superpowers version `v5.1.0` as an unrevalidated historical declaration, explained below the table rather than inside the cell, and that explanation SHALL state that it is not a compatibility guarantee.

The existing v2 and v3 row dates are outside this requirement: they are CLI-level attestations, already documented as such, and this change does not rewrite them.

#### Scenario: REQ-3-S1 Dogfood on another Superpowers version does not fill the date

- **WHEN** the v4 row lists Superpowers `v5.1.0` and this change's dogfood runs on a different loaded Superpowers version
- **THEN** the v4 row's "Baseline as of" stays `pending`

#### Scenario: REQ-3-S2 Weekly version check reads the row of the released schema major

- **WHEN** `superpowers-bridge/schema.yaml` declares schema major N, the Compatibility table holds a `vN` row whose date cell may read `pending` with its explanation below the table, and a schema-major bump is released
- **THEN** the row the weekly version check reads is the `vN` row — the check's row target is updated together with the bump, by whatever means — and running that step yields the OpenSpec and Superpowers versions listed in that row; this scenario does not require the check to detect the newest row on its own
