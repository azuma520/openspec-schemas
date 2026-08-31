# Proposal: claude-md-phase-boundary

## Why

The bridge-guarantee direction document (2026-08-27) confirmed Orca as the
bridge's future execution runtime, so CLAUDE.md's "phase two has not started"
framing is no longer factual. This change restates the boundary as an event
gate — updating the reason schema work is forbidden, not lifting the
prohibition. It is also the Phase 2 specimen of the traceability-gate concept
PoC (routing exception recorded in the PoC spec §6).

## What Changes

- Rewrite the CLAUDE.md「分兩階段」section as an event-gated work boundary
  (concept PoC PASS + approved formal design, instead of time phases).

## Impact

CLAUDE.md guidance only. No schema.yaml change, no new formal artifact type.
