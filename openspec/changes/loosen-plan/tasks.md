## 1. schema.yaml — plan artifact (Plan Contract, producer, PRECHECK)

- [x] 1.1 Rewrite the `plan` artifact instruction: remove the `superpowers:writing-plans` invocation, its PRECHECK, and the micro-step description (2-5 min steps, exact paths, commit points); define the Plan Contract (header + one entry per tasks.md task keyed by task number; delivers / acceptance criteria / blocked by / conditional interfaces; right-sizing rule; decision-rich snippet allowed; no step prescription) and a generation-time self-review list (entry keys = task numbers, no vague acceptance language, interfaces present where coupled)
  - TDD: n/a — schema.yaml has real behaviour (the CLI parses it; agents act on the prose), but that behaviour has no unit-testable subject; the fitting verification is `openspec schema validate` (structure) + `openspec instructions plan` render (integration) + text review against specs/plan-contract. Not n/a because it is YAML
- [x] 1.2 Update the `plan` artifact `description:` line (currently "Micro-task implementation plan using Superpowers writing-plans") to the contract wording
  - TDD: n/a — one-line metadata

## 2. schema.yaml — tasks artifact (TDD applicability annotation + evidence carrier)

- [x] 2.1 Extend the `tasks` artifact instruction: every task carries `TDD: applicable` or `TDD: n/a — <reason>` indented under the checkbox; tasks.md is the SSOT for applicability; seed the `n/a` reason vocabulary (throwaway prototype, generated code, configuration, prose/doc-only); define the RED/GREEN record shape that applicable tasks write under the same checkbox at completion (subject `test-file::test-name`, outcome, failure excerpt; GREEN same subject, PASS; invocation optional); state it is the v1 carrier, not an invariant
  - TDD: n/a — instruction prose; verified by validate + text review against specs/tdd-evidence-contract
- [x] 2.2 Add a tasks self-review line: no task without an annotation; `n/a` must carry a reason
  - TDD: n/a — instruction prose

## 3. schema.yaml — apply instruction (TDD passage, writing-plans references)

- [x] 3.1 Rewrite the apply step-2 TDD passage per specs/tdd-claim-accuracy: applicability is annotation-driven from tasks.md; applicable tasks owe RED/GREEN records under the task, checked by verify's deterministic checks (agent-executed, instruction-mediated — not a non-bypassable gate); semantics and authenticity rest on review; remove "this schema itself neither enforces nor verifies TDD" and "writing-plans' standard task format contains TDD micro-steps"
  - TDD: n/a — instruction prose; verified by grep for the two superseded strings (expect 0 hits in bridge-owned surfaces) + text review
- [x] 3.2 Update the apply pre-flight / executor wording that reads plan.md as "micro-tasks" (reads contract entries instead); keep the subagent-driven-development dispatch, the no-`executing-plans` rule, and every other PRECHECK unchanged
  - TDD: n/a — instruction prose; red-flag table in CLAUDE.md re-read before editing

## 4. schema.yaml — verify instruction + templates/verify.md (deterministic checks)

- [x] 4.1 Append numbered deterministic checks to the verify instruction's existing list without restructuring it (guardrail 8): (a) every tasks.md task has a well-formed `TDD:` annotation; (b) every `applicable` task has RED and GREEN records with the required fields; (c) RED outcome marker is non-pass and GREEN outcome marker is pass; (d) RED subject == GREEN subject; (e) tasks.md task-number set == plan.md entry-key set, both differences empty; any failure → BLOCK. Separately list the **review judgements** that are not deterministic: whether the RED excerpt is a behavioural failure rather than SyntaxError/import/dependency/harness error, whether the subject actually tests the claimed behaviour, whether an `n/a` reason holds. State in the instruction that the deterministic checks are agent-executed (instruction-mediated) and that skipping one is not intercepted by v1
  - TDD: n/a — this is instruction prose whose behaviour is "what the verify agent does when reading it"; the fitting verification is a mutation-style run, not a unit test: on a fixture change, violate each deterministic check once (missing annotation / missing GREEN / outcome marker PASS on RED / subject mismatch / plan `{1,2,9}` vs tasks `{1,2,3}`) and confirm BLOCK; plus one SyntaxError-RED fixture to confirm it surfaces as a review finding — recorded in verify.md of this change
- [x] 4.2 Update `templates/verify.md` §4 TDD rows to report per-task annotation + evidence outcome (which tasks applicable, which passed the checks) instead of "task list required TDD or not"
  - TDD: n/a — Markdown template

## 5. schema.yaml — top-level description, skill list, version

- [x] 5.1 Update the top-level `description:` — remove `writing-plans` from the required-skill list (currently 5 named; 4 remain — not to be confused with the README's "Seven touchpoints" table, a different list), replace "TDD arrives via plan.md task content" with the annotation + evidence contract sentence at its actual capability
  - TDD: n/a — metadata prose
- [x] 5.2 Bump `version: 1` → `version: 2` in schema.yaml and `superpowers-bridge/VERSION` 1.0.1 → 2.0.0
  - TDD: n/a — version literals; verified by `openspec schema validate` + `openspec schemas` on a fresh copy

## 6. templates/plan.md and templates/tasks.md

- [x] 6.1 Rewrite `templates/plan.md` (17-line shell) to the Plan Contract shape: header block (goal, pointers to specs/ and design.md, global constraints) + entry skeleton keyed by task number with delivers / acceptance criteria / blocked by / interfaces (marked conditional); `<!-- -->` fill-in guidance may stay zh-TW per repo convention
  - TDD: n/a — Markdown template
- [x] 6.2 Rewrite `templates/tasks.md` to show the `TDD:` annotation and the RED/GREEN record shape under a sample task
  - TDD: n/a — Markdown template

## 7. Bridge README (en + zh-TW) — claims, touchpoints, versioning, migration

- [x] 7.1 Update every writing-plans / "TDD micro-steps" / "TDD per task content" claim in `superpowers-bridge/README.md`: problem statement (§ task fragmentation), comparison table (Plan layer, apply method rows), Mermaid DAG node for plan.md, apply description, "Seven Superpowers touchpoints" table (row 2 → no longer invoked; row 5 → annotation + evidence contract), integration runbook bullets, the "How TDD and code review actually arrive" touchpoint, and the "Open drift — TDD is conditional upstream" paragraph (mark the deeper fix as landed in v2, brainstorming drift stays open)
  - TDD: n/a — documentation; verified by grep of the superseded phrases (0 hits) + text review at the claim boundary in specs/tdd-evidence-contract "Claim boundaries"
- [x] 7.2 Add the v2 row to the Compatibility table and a v1→v2 migration guide section (the four steps from design.md § Migration Plan; rollback = pin bundle 1.0.1); keep the v1 row intact
  - TDD: n/a — documentation
- [x] 7.3 Mirror 7.1–7.2 into `superpowers-bridge/README.zh-TW.md`
  - TDD: n/a — translation
- [x] 7.4 Update the CLI cheat sheet / install expectations if they list `writing-plans` as required
  - TDD: n/a — documentation

## 8. Adopter fragments, top-level README, roadmap

- [x] 8.1 Update `templates/adopters/CLAUDE.md.fragment.md` and `.zh-TW.md`: remove the "letting writing-plans write to docs/superpowers/plans/" red-flag row or reword it for the optional-aid case; add the tasks.md `TDD:` annotation expectation
  - TDD: n/a — documentation; both locales edited in the same commit
- [x] 8.2 Update top-level `README.md` + `README.zh-TW.md` bridges table: schema major column v1 → v2, description no longer says "writing-plans with TDD micro-steps"
  - TDD: n/a — documentation
- [x] 8.3 Update `docs/roadmap.md` + `.zh-TW.md`: mark the plan-loosening / TDD-evidence item landed in v2; leave unrelated backlog items as they are
  - TDD: n/a — documentation
- [x] 8.4 Root `CLAUDE.md` (a bridge-owned normative surface named by `openspec/specs/tdd-claim-accuracy` requirement 3): confirm the executing-plans red-flag row's TDD clause reads the v2 carrier ("TDD 由 tasks.md 的 applicability 標註 + 證據契約承載,與執行器無關" — landed in the doc-gate round of this change) and that no other CLAUDE.md sentence still describes TDD as arriving via plan.md / writing-plans micro-steps. **Scope boundary:** only the clauses this change makes stale; the full §5 capability / evidence / degradation rewrite of that red flag stays with the registered work-map item and is not folded in
  - TDD: n/a — governance prose; verified by the 10.2 sweep now covering CLAUDE.md

## 9. CI coupling

- [x] 9.1 Update `.github/workflows/version-check.yml` `Read pinned versions` step: the grep currently keys on `^\| v1 \| \`` — point it at the v2 row (or the newest row) so the pinned OpenSpec / Superpowers baselines are read from the current schema major; keep the backtick-column shape the awk relies on
  - TDD: n/a — the workflow has real behaviour (grep/awk extraction, npm/GitHub lookups) but no local test harness; the fitting verification is integration-style: run the extraction lines locally against the edited README (both versions print non-empty; also confirm the old `v1` pattern would now read the wrong row, to prove the change matters) and watch the next scheduled/dispatched run

## 10. Dogfood sync and end-to-end check

- [ ] 10.1 Re-sync the dogfood copy (`rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/`) and run `openspec schema validate superpowers-bridge` + `openspec schemas` from a clean test project per CLAUDE.md
  - TDD: n/a — verification step; output pasted into verify.md
- [ ] 10.2 Grep all bridge-owned surfaces (schema.yaml, templates/, both bridge READMEs, adopter fragments, top-level READMEs, **and root CLAUDE.md** — spec-named normative surface) in two classes. **Exact superseded sentences — expect 0 hits**: "neither enforces nor verifies TDD", "TDD micro-steps", "TDD arrives via plan.md task content", "writing-plans' standard task format". **Boundary vocabulary — grep then review every hit, 0 is not the criterion**: "mechanical", "guarantee", "bypass", "gate", "fail-closed" — each hit must either be a negation ("not a mechanically enforced gate") or a claim within the tdd-evidence-contract "Claim boundaries" requirement; any positive claim of a Harness-enforced archive gate is a finding
  - TDD: n/a — verification step; both grep outputs and the per-hit disposition recorded in verify.md
- [ ] 10.3 Run one `openspec new change --schema superpowers-bridge` on the v2 copy and confirm `openspec instructions plan` / `instructions tasks` render the new contract text (no writing-plans PRECHECK)
  - TDD: n/a — verification step
- [ ] 10.4 Bounded fresh-context v2 plan-generation smoke test: one fixture change (≥ 5 tasks, ≥ 2 coupled), one fresh subagent given only the v2 `plan` instruction + tasks.md + design.md, one generation; score the result against the Plan Contract (key-set equality, no vague acceptance, interfaces on coupled tasks, no step prescription) and against the D3 trigger list; record in verify.md as one sample and hand the Q4-A recommendation to the user (this change's own plan.md was hand-written under v1 and does not count as direct-producer evidence)
  - TDD: n/a — an evaluation run, not code; the fitting verification is the scored sample itself
