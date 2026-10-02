## 1. Align the §4 inventory with REQ-5

- [ ] 1.1 Retrospective template §4 presents exactly the six REQ-5 rows, with no `superpowers:writing-plans` row, and its note states the two-class definition without a second, conflicting one
  - TDD: n/a — template prose; no executable behaviour, checked by reading against REQ-5-S1..S4
- [ ] 1.2 Retrospective instruction §4 in `schema.yaml` states the two-class criterion (required invocations + required disciplines, optional aids excluded) in place of "apply phase"
  - TDD: n/a — instruction prose passed verbatim to the agent; no executable behaviour, checked by reading against REQ-5-S4

## 2. Consistency and delivery

- [ ] 2.1 Bridge README (en and zh-TW) checked for statements about what retrospective §4 lists; any conflict with REQ-5 is reported, and no edit is made where none conflicts
  - TDD: n/a — doc consistency review; the outcome is a recorded finding, not behaviour
- [ ] 2.2 The dogfood schema copy matches `superpowers-bridge/`, the bridge and the change validate, and the retrospective instructions the CLI hands an agent carry the new §4 text
  - TDD: n/a — delivery check of existing CLI behaviour; no new behaviour is introduced
