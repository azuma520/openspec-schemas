## ADDED Requirements

### Requirement: REQ-PB event-gated schema work boundary
CLAUDE.md SHALL state the schema-work boundary as an event gate: Orca is
confirmed as the bridge's future execution runtime, with architecture
direction owned by the bridge-guarantee direction document; and until the
concept PoC passes AND the formal design is approved, `schema.yaml` MUST NOT
be modified and no formal artifact type may be added. The restatement SHALL
replace the outdated "phase two has not started" framing — it updates the
reason for the prohibition, it does not authorize early Orca implementation.

#### Scenario: boundary reads as yes/no events
- **WHEN** a reader consults CLAUDE.md before touching schema.yaml
- **THEN** the gate is expressed as answerable events (concept PoC passed? formal design approved?) rather than a time phase

#### Scenario: prohibition force unchanged
- **WHEN** the restated section lands
- **THEN** modifying schema.yaml or adding a formal artifact type is still forbidden until both gate events are YES
