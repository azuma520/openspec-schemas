## MODIFIED Requirements

### Requirement: REQ-3 executing-plans exclusion rationale rests on review structure

The rationale SHALL rest on verified structural facts about `superpowers:executing-plans` itself
everywhere the bridge explains why it is not supported as an apply fallback: it runs without a
reviewer per task and reviews the whole branch once at the end, and on a platform without a
subagent tool — the situation a fallback would serve — that final review is performed by the
author. The bridge's apply relies on independent review during execution (after each task, or
after each batch of small same-shape tasks, rather than only at the end). The rationale SHALL NOT
rest on what upstream recommends choosing between executors, and SHALL NOT state that
executing-plans dispatches no independent reviewer at all — with a subagent tool it dispatches
one for the final review.

The rationale SHALL NOT use TDD as a differentiator between the two executors. TDD is not a
differentiator because the bridge's TDD requirement does not depend on either executor carrying
it: applicability is declared per task in tasks.md and evidenced by the RED/GREEN records the
tdd-evidence-contract capability defines, so the requirement reaches an executor through the
task list it is given, whichever executor that is. Surfaces SHALL NOT describe plan.md task
content as the carrier of that requirement — under the Plan Contract plan.md holds contract
entries and no task list.

#### Scenario: REQ-3-S1 Old TDD-based comparison is gone

- **WHEN** the fallback rationale segments (schema.yaml, both bridge READMEs, CLAUDE.md
  red-flag list) are read after the change
- **THEN** none argues "it does not bring TDD while we do"; each states the
  review-structure rationale, with the code-review comparison scoped honestly (review during
  execution, which may batch small same-shape tasks — not one-reviewer-per-task)

#### Scenario: REQ-3-S2 Carrier named consistently across the spec

- **WHEN** this capability's own requirements are read together
- **THEN** every statement of where a TDD requirement reaches an executor names the tasks.md
  annotation and evidence contract, and none names plan.md task content, so the spec presents
  a single answer rather than two conflicting ones

#### Scenario: REQ-3-S3 Superseded executing-plans claims are gone

- **WHEN** the same fallback rationale segments are read after the change
- **THEN** none states that executing-plans dispatches no independent reviewer without
  qualification, none states that upstream directs users to subagent-driven-development
  whenever subagents exist, and none rests the exclusion on any upstream recommendation;
  each states that executing-plans has no reviewer per task and that its final review is
  author-performed on a platform without a subagent tool
