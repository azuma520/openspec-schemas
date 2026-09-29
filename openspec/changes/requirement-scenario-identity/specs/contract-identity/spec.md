# contract-identity

## ADDED Requirements

### Requirement: REQ-1 Requirement and Scenario headings carry a stable identity

Every requirement heading in a `superpowers-bridge` spec SHALL have the form `### Requirement: <REQ-ID> <description>`, where `<REQ-ID>` is `REQ-` followed by one or more uppercase letters or digits (`[A-Z0-9]+`), and `<description>` is non-empty text separated from the ID by whitespace. Every scenario heading SHALL have the form `#### Scenario: <REQ-ID>-S<m> <description>`, where `<REQ-ID>` is exactly the local ID of the requirement the scenario sits under, `<m>` is a positive integer written without leading zeros, and `<description>` is non-empty.

The ID is the identity of the contract; the description is not. A local ID is unique within its capability, not across the repository; a formal cross-artifact reference to a contract therefore carries the capability as well (`capability / local-ID`), while prose MAY use the bare local ID. Requirement IDs that already exist are legal as they are, whether numeric or not; the numeric form is a constraint on newly allocated IDs only (REQ-4).

#### Scenario: REQ-1-S1 Conforming headings

- **WHEN** a capability contains `### Requirement: REQ-3 Token expiry` with scenarios `#### Scenario: REQ-3-S1 expired token` and `#### Scenario: REQ-3-S2 valid token`
- **THEN** every heading carries a legal identity

#### Scenario: REQ-1-S2 Heading without an ID blocks

- **WHEN** a requirement heading reads `### Requirement: Token expiry`, or a scenario heading reads `#### Scenario: expired token`
- **THEN** the identity check reports a violation naming the heading

#### Scenario: REQ-1-S3 ID without a description blocks

- **WHEN** a requirement heading reads `### Requirement: REQ-3` with nothing after the ID
- **THEN** the identity check reports a violation

#### Scenario: REQ-1-S4 Scenario prefix must name its own requirement

- **WHEN** a scenario headed `#### Scenario: REQ-7-S1 …` sits under the requirement `REQ-3`
- **THEN** the identity check reports a violation, even if a requirement `REQ-7` exists elsewhere in the capability

#### Scenario: REQ-1-S5 Existing non-numeric ID stays legal

- **WHEN** a capability contains the pre-existing requirement `REQ-PB` with scenarios `REQ-PB-S1` and `REQ-PB-S2`
- **THEN** the headings carry a legal identity and no rename is required

### Requirement: REQ-2 Identity survives rewording and renaming

A contract's ID SHALL NOT change once the contract exists. Rewording a requirement's body while keeping its heading is a MODIFIED operation and leaves the ID unchanged. Changing a requirement heading's description is a RENAMED operation, and the local ID in the RENAMED `FROM` heading SHALL equal the local ID in its `TO` heading. The one exception is a `FROM` heading that carries no ID at all: that rename assigns an ID to a pre-existing unnumbered requirement (migration), and its `TO` ID is a newly allocated ID under REQ-4. Giving a contract a different ID is a change of contract identity: the old ID is retired and a new one is born, and it SHALL NOT be expressed as a rename.

#### Scenario: REQ-2-S1 Reworded body keeps the ID

- **WHEN** a change MODIFIES `REQ-3` with new body text under the same heading
- **THEN** the contract is still `REQ-3` and the identity check raises nothing for it

#### Scenario: REQ-2-S2 Rename that keeps the ID passes

- **WHEN** a change RENAMES `### Requirement: REQ-3 Token expiry` to `### Requirement: REQ-3 Access token expiry`
- **THEN** the identity check raises nothing for it

#### Scenario: REQ-2-S3 Rename that changes the ID blocks

- **WHEN** a change RENAMES `### Requirement: REQ-3 Token expiry` to `### Requirement: REQ-9 Token expiry`
- **THEN** the identity check reports a violation naming both IDs

#### Scenario: REQ-2-S4 Migration rename assigns a new ID under the allocation rules

- **WHEN** a change RENAMES the unnumbered `### Requirement: Token expiry` to `### Requirement: REQ-FOO Token expiry`
- **THEN** the rename is an ID assignment, `REQ-FOO` is a new ID, and the identity check reports a violation under REQ-4; renaming it to `REQ-1 Token expiry` in a capability with no numeric ID raises nothing

### Requirement: REQ-3 One local ID denotes one contract

Within one capability, a local ID SHALL NOT denote two different contracts. Whether two occurrences denote the same contract SHALL be decided from artifact structure and the OpenSpec operation role, never from reading the text: a main-spec requirement and a delta MODIFIED or RENAMED entry carrying the same ID are the same contract; an ADDED entry carrying an ID that the main spec already holds, two ADDED entries carrying the same ID, and two separate blocks in one spec file carrying the same ID each denote two contracts under one ID. A RENAMED entry maps its `FROM` requirement in the main spec to its `TO` heading; a MODIFIED entry whose heading equals a RENAMED `TO` heading in the same delta file resolves through that mapping to the `FROM` requirement, and is the same contract as it — including when the `FROM` heading carries no ID (migration), where the main spec does not yet hold the `TO` heading. Scenario IDs follow the same rule within their requirement. The same contract appearing in several places is not a violation.

#### Scenario: REQ-3-S1 MODIFIED entry is the same contract

- **WHEN** the main spec holds `REQ-3` and the change's delta MODIFIES `REQ-3`
- **THEN** the two occurrences are one contract and the identity check raises nothing

#### Scenario: REQ-3-S2 ADDED entry that takes an existing ID blocks

- **WHEN** the main spec holds `REQ-3` and the change's delta ADDS a requirement with ID `REQ-3`
- **THEN** the identity check reports a violation

#### Scenario: REQ-3-S3 Two blocks in one file with one ID block

- **WHEN** one spec file contains two separate requirement blocks both headed with `REQ-3`
- **THEN** the identity check reports a violation

#### Scenario: REQ-3-S4 Two ADDED entries with one ID block

- **WHEN** a change's delta ADDS two requirements both carrying `REQ-11`
- **THEN** the identity check reports a violation

#### Scenario: REQ-3-S5 Two scenarios with one ID under a requirement block

- **WHEN** requirement `REQ-3` contains two scenarios both headed `REQ-3-S2`
- **THEN** the identity check reports a violation

#### Scenario: REQ-3-S6 MODIFIED after a migration RENAMED resolves to the FROM requirement

- **WHEN** the main spec holds the unnumbered `### Requirement: Token expiry` with two unnumbered scenarios, and the delta RENAMES it to `### Requirement: REQ-1 Token expiry` and MODIFIES `### Requirement: REQ-1 Token expiry` with scenarios `REQ-1-S1` and `REQ-1-S2`
- **THEN** the MODIFIED entry is the same contract as the `FROM` requirement, its two scenarios are new with an empty current set, and the identity check raises nothing

### Requirement: REQ-4 New identities are allocated by fixed rules

Newly allocated IDs SHALL follow the rules below, which first fix what counts as new. A requirement ID is new when its requirement appears under ADDED, or when it is the `TO` ID of a RENAMED entry whose `FROM` heading carries no ID (REQ-2); every scenario under an ADDED requirement is new. A scenario is also new when it appears in a MODIFIED requirement and its ID is not among that requirement's scenarios in the main spec; "that requirement" is the main-spec requirement the MODIFIED entry resolves to under REQ-3, so for a MODIFIED entry that follows a migration RENAMED it is the `FROM` requirement, whose unnumbered scenarios hold no ID and leave the current set empty.

The identity check SHALL enforce: a new requirement's ID is `REQ-<n>` with `<n>` a positive integer greater than every numeric requirement ID currently in that capability's main spec; a new scenario's number is greater than every scenario number currently under the same requirement in the main spec, compared within that requirement only. When the relevant current set is empty, any positive integer satisfies the check.

The author allocating an ID SHALL additionally take history into account: the base is the largest number ever used for that capability (or, for scenarios, that requirement), including the delta specs of archived changes, and the new number is taken above it. Only when no number has ever been used does allocation start at 1. The identity check does not read history and does not verify this obligation (REQ-8).

#### Scenario: REQ-4-S1 New numeric ID above the current maximum passes

- **WHEN** the main spec's largest numeric requirement ID is `REQ-9` and the change ADDS `REQ-10`
- **THEN** the identity check raises nothing for the allocation

#### Scenario: REQ-4-S2 New non-numeric ID blocks

- **WHEN** a change ADDS a requirement with ID `REQ-FOO`
- **THEN** the identity check reports a violation, although `REQ-FOO` matches the heading grammar of REQ-1

#### Scenario: REQ-4-S3 New ID not above the current maximum blocks

- **WHEN** the main spec's largest numeric requirement ID is `REQ-9` and the change ADDS `REQ-4` (an ID not held by any current requirement)
- **THEN** the identity check reports a violation

#### Scenario: REQ-4-S4 New scenario number is compared within its requirement

- **WHEN** requirement `REQ-3` currently has scenarios up to `REQ-3-S2`, requirement `REQ-5` has scenarios up to `REQ-5-S6`, and a change MODIFIES `REQ-3` adding `REQ-3-S3`
- **THEN** the identity check raises nothing for the allocation

#### Scenario: REQ-4-S5 Empty current set accepts any positive integer

- **WHEN** a capability's main spec holds no numeric requirement ID and a change ADDS `REQ-4`
- **THEN** the identity check raises nothing for the allocation

#### Scenario: REQ-4-S6 Author allocates above the historical maximum

- **WHEN** an archived change once held `REQ-10` for a capability, `REQ-10` has since been removed, and the main spec's largest ID is `REQ-9`
- **THEN** the author allocating a new requirement ID SHALL take `REQ-11` or above, and the identity check, which does not read history, would also accept `REQ-10`

### Requirement: REQ-5 The identity check judges the candidate state

The identity check SHALL read two states in two roles. The current state — the main specs together with the change's delta specs — is the context: it decides whether an entry is new, what the current maxima are, and what each RENAMED `FROM` denotes. It SHALL NOT be required to satisfy REQ-1 as a whole, because before archive it may still be in the unnumbered form a migrating change is replacing. The candidate state — the main specs produced by running `openspec archive <change> -y` on a temporary copy of the repository's `openspec/` directory, without `--skip-specs` — is the object under judgement: every heading in it SHALL satisfy REQ-1 and REQ-3. The check SHALL NOT re-implement OpenSpec's merge.

#### Scenario: REQ-5-S1 A migrating change is judged by its result

- **WHEN** a change RENAMES every unnumbered requirement of every capability in the repository to a numbered heading and MODIFIES each with numbered scenario headings, while those main specs are still unnumbered
- **THEN** the identity check judges the candidate state, finds every heading numbered, and raises nothing

#### Scenario: REQ-5-S2 Failed archive preview is undeterminable

- **WHEN** the archive preview on the temporary copy fails (for example, a MODIFIED heading matches no requirement in the main spec)
- **THEN** no candidate state exists, and the identity check reports the outcome as undeterminable and blocks

### Requirement: REQ-6 Extracted counts are cross-checked against the CLI

Counts the identity check extracts from text SHALL be compared with the OpenSpec CLI's JSON, and any disagreement SHALL block without presuming which side is right. Each comparison SHALL read the CLI against the state it judges. For each candidate-state main spec, the CLI SHALL be run inside the temporary copy produced under REQ-5, after the archive preview — run against the repository's own `openspec/` it would read the pre-archive main spec and compare the wrong state: the number of requirement headings SHALL equal `requirementCount` from `openspec show <spec> --type spec --json`, and the number of scenario headings under the k-th requirement SHALL equal the length of `requirements[k].scenarios`. For the change, the CLI SHALL be run against the current state, where the change is not yet archived: the number of requirements under each operation in each delta file — counted as `### Requirement:` headings under ADDED, MODIFIED and REMOVED, and as `FROM` / `TO` pairs under RENAMED, one pair being one rename — SHALL equal the number of entries of that spec and operation in `openspec show <change> --json --deltas-only`; for each ADDED or MODIFIED entry, the number of scenario headings under the k-th requirement of that operation in the delta file SHALL equal the length of the scenarios array of the k-th such entry in the CLI output; and the IDs in each RENAMED pair SHALL also be compared as given by the CLI's `rename.from` and `rename.to`.

Pairing scenarios by requirement position is an assumption about OpenSpec 1.3.1, whose JSON carries no scenario identity. When the pairing cannot be made reliably — for instance the requirement counts already disagree — the cross-check is undeterminable and SHALL block; the check SHALL NOT guess a pairing.

#### Scenario: REQ-6-S1 Agreeing counts pass

- **WHEN** a candidate-state spec has three requirement headings with two, one and one scenario headings, and the CLI reports `requirementCount` 3 with scenario arrays of lengths 2, 1 and 1
- **THEN** the cross-check raises nothing

#### Scenario: REQ-6-S2 A heading the CLI does not see blocks

- **WHEN** a malformed line makes the text extraction count four requirement headings while the CLI reports `requirementCount` 3
- **THEN** the identity check blocks, reporting the mismatch

#### Scenario: REQ-6-S3 Scenario count mismatch at a position blocks

- **WHEN** requirement counts agree but the text extraction finds two scenario headings under the second requirement while the CLI's second requirement has one scenario
- **THEN** the identity check blocks, reporting the position and both counts

#### Scenario: REQ-6-S4 Delta scenario counts are cross-checked

- **WHEN** a delta file's MODIFIED requirement has three scenario headings while the CLI's matching MODIFIED entry has two scenarios
- **THEN** the identity check blocks, reporting the delta entry and both counts

### Requirement: REQ-7 Blocking outcomes are distinguished and never degraded

A blocking outcome of the identity check SHALL be recorded as one of two kinds: a violation, when the check completed and found a breach of REQ-1 to REQ-4, or completed a reliably paired REQ-6 comparison and found the counts disagree; or undeterminable, when the check could not complete reliably (failed archive preview, CLI output lacking the data needed or no longer mappable, unreliable cross-check pairing). An undeterminable outcome SHALL NOT be recorded as an identity violation. Neither kind SHALL have a degraded pass: identity integrity is a Core Integrity Invariant, which no change may switch off or override.

#### Scenario: REQ-7-S1 Undeterminable is not reported as a violation

- **WHEN** the archive preview fails
- **THEN** verify.md records the identity check as undeterminable and blocking, not as an ID violation

#### Scenario: REQ-7-S2 No degraded pass

- **WHEN** a change's proposal asks to relax or skip the identity check
- **THEN** the identity check still applies, and an undeterminable or violating outcome still blocks

#### Scenario: REQ-7-S3 A completed comparison that disagrees is a violation

- **WHEN** requirement counts agree, pairing is reliable, and the scenario counts at one position disagree
- **THEN** verify.md records an identity violation, not an undeterminable outcome

### Requirement: REQ-8 Claim boundaries of the identity check

The identity check is a set of deterministic, machine-evaluable rules executed by the verify agent as part of verify; it is not a non-bypassable executable gate, and no surface SHALL describe it as one. It establishes, for the candidate state and the change, only what REQ-1 to REQ-7 state. It SHALL NOT be described as establishing that: a retired ID is never reassigned (the check reads no history); no scenario ID disappears silently through a MODIFIED full-text replacement or through archive; the meaning under an unchanged ID has not been weakened; or an ID survives a capability rename.

Mutation fixtures exercising the check establish that its rules are explicit enough for an agent following them to reach the expected verdict on known defects. They do not establish that the harness enforces these invariants. They are conformance and acceptance evidence: each fixture carries an expected outcome (pass, or block recorded as a violation or as undeterminable), and the evidence is that the verdict reached by following the rules matches it. Where a fixture is re-run with the same method before and after the identity check's rules are added, and the verdict under the earlier rules contradicts this contract while the verdict under the new rules matches it, that before/after pair MAY also serve as TDD evidence for the task that adds the rules. A fixture whose verdict does not change — a positive control, or one already blocked by an earlier check — is conformance evidence only. TDD evidence obtained this way shows a reproducible contract gap and its closure; it does not raise the assurance claims of this requirement, since the verdicts are still reached by an agent following the rules. No surface SHALL present the fixtures as establishing more than this requirement states.

#### Scenario: REQ-8-S1 No non-bypassable claim

- **WHEN** a bridge surface (schema instruction, template, README) describes the identity check
- **THEN** it describes deterministic rules executed by the verify agent and does not claim the harness enforces them

#### Scenario: REQ-8-S2 Reuse of a retired ID is outside the guarantee

- **WHEN** a change ADDS `REQ-10` to a capability whose `REQ-10` was retired in an archived change, and the current maximum is `REQ-9`
- **THEN** the identity check raises nothing, and no surface claims that the check prevents this

#### Scenario: REQ-8-S3 Fixtures are conformance evidence

- **WHEN** a fixture expected to block as a violation is judged by an agent following the identity check's rules
- **THEN** the evidence records the fixture, the expected outcome and the verdict reached, and is cited as conformance evidence that the rules decide this case, not as showing that the harness enforces them

#### Scenario: REQ-8-S4 A changed verdict is TDD evidence without raising assurance

- **WHEN** a fixture whose requirement heading carries no ID passes under the verify rules in force before the identity check is added, and blocks as a violation when the same fixture is re-run the same way after it is added
- **THEN** the pair may be recorded as RED and GREEN TDD evidence for the task that added the rules, and no surface cites it as showing that the harness enforces the identity check

#### Scenario: REQ-8-S5 An unchanged verdict is conformance evidence only

- **WHEN** a positive-control fixture passes both before and after the identity check is added
- **THEN** it is recorded as conformance evidence only, and no RED is recorded for it
