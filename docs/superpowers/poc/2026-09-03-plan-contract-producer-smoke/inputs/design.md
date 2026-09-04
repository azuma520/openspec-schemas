# Design — add-rate-limit

## Context

The public API has no rate limiting. A single misbehaving client can exhaust the request budget for everyone, and the only current mitigation is manual IP blocking at the edge, which is slow and coarse. This change adds an in-process limiter with declarative policies.

## Goals / Non-Goals

**Goals**

1. Policies are declared, not coded — an operator changes a limit by editing config, not by shipping.
2. A denied request costs the handler nothing: the limiter decides before the handler runs.
3. Clients can see their own budget without guessing, via response headers.

**Non-Goals** (closed set): distributed/shared state across instances; persistence of buckets across restarts; per-user quota accounting or billing; dynamic policy reload without restart; any admin UI.

## Decisions

### D1 — Policy is a named record, referenced by name

A policy is `{ window, burst, keySelector? }` declared under a name in `config/rate-limits.yaml`. Everything else refers to policies **by name**. Rationale: the same limit is usually shared by several routes, and inlining it at each route makes a limit change a multi-file edit. Consequence: an unknown name is a configuration error, and it is caught **at boot**, not on the request that happens to hit it — a limit that silently does not apply is worse than a service that refuses to start.

### D2 — Token bucket, per (policy, identity), in process memory

Token bucket over fixed windows, because it permits a short burst while holding the average — the behaviour operators actually expect from "60 per minute". Identity comes from the policy's `keySelector` (default: client IP). Buckets expire after two idle windows so memory does not grow without bound. In-process only: distributed state is a Non-Goal, so two instances enforce independently and the effective global limit is the per-instance limit times the instance count. That is a deliberate, documented under-enforcement, not an oversight.

### D3 — Resolution happens at registration, enforcement at request

Route overrides are resolved when routes are registered, so the request path does a map lookup rather than a config walk. This is what makes D1's boot-time failure possible: by the time the first request arrives, every route already holds a resolved policy or the process never started.

### D4 — Headers are informational, and always present when the limiter ran

`X-RateLimit-Remaining` and `X-RateLimit-Reset` are emitted on every response the limiter saw, including 429s — a client that has just been denied is exactly the client that needs to know when to retry. They are not emitted on paths the limiter never touched, because a header claiming a budget that was never checked would be a lie.

## Risks / Trade-offs

- [Per-instance enforcement under-counts] → documented in the API reference; revisit if the fleet grows past a handful of instances.
- [In-memory buckets reset on deploy] → accepted; a deploy briefly forgives limits rather than briefly over-denying.
- [Clock skew affects `resetAt` across instances] → clients are told to treat `X-RateLimit-Reset` as advisory.

## Migration Plan

None — this is additive. Rolling out with an empty policy set changes no behaviour; limits begin applying as policies are declared.
