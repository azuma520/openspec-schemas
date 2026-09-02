# tdd-claim-accuracy

## MODIFIED Requirements

### Requirement: Honest statement of the TDD carrier

The apply instruction in `schema.yaml` SHALL state where TDD actually comes from under the evidence contract: TDD applicability is declared per task in tasks.md (`TDD: applicable` / `TDD: n/a — <reason>`); applicable tasks must record RED/GREEN evidence under the task in tasks.md per the tdd-evidence-contract capability; the verify instruction requires deterministic checks of the presence and structure of annotations and evidence before archive, executed by the verify agent (instruction-mediated, not a Harness-enforced gate); and the schema does not verify evidence semantics or authenticity — those rest on the review layer and degrade with it. The instruction SHALL NOT claim TDD executes automatically or unconditionally, SHALL NOT claim the schema verifies more than presence and structure, SHALL NOT claim a non-bypassable mechanical gate, and SHALL NOT retain the superseded statements that the schema "neither enforces nor verifies TDD" or that TDD arrives via `writing-plans`' micro-step task content.

#### Scenario: Agent reading the apply instruction learns the evidence condition

- **WHEN** an agent reads the apply instruction's TDD passage after the change
- **THEN** it is told that applicability is annotation-driven from tasks.md, that applicable tasks owe RED/GREEN evidence in tasks.md checked by verify's deterministic checks (agent-executed), and that semantic and authenticity assurance belong to review — and it is not told that any skill or layer executes or fully verifies TDD on its behalf

#### Scenario: Superseded carrier statements are gone

- **WHEN** bridge-owned normative surfaces are read after the change
- **THEN** none states that the schema "neither enforces nor verifies TDD" or that TDD arrives via writing-plans micro-steps; each describes the annotation + evidence carrier at its actual capability
