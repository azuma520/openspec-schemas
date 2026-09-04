# add-rate-limit — Plan Contract

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task. Each entry states what "done"
> means for one task, not how to get there — two executors may satisfy
> the same entry by different paths and both conform.

**Goal:** Add an in-process, declaratively-configured rate limiter that rejects over-budget requests before they reach the handler, and tells clients their remaining budget via response headers.

**Pointers:** This change has no `specs/` directory. The source used for the header, global constraints, and per-entry acceptance criteria below is `design.md` (Context, Goals/Non-Goals, Decisions D1–D4, Risks/Trade-offs). Architecture and rationale live there — see D1 (named policy config), D2 (token bucket, per-instance, in-memory), D3 (registration-time resolution), D4 (header semantics) — and are not repeated here beyond what each entry needs to state its acceptance criteria.

**Global constraints (verbatim from design.md; every entry below is bound by them):**

- "an unknown policy name referenced anywhere is a boot-time failure, not a request-time one" (D1)
- Non-Goals (closed set): "distributed/shared state across instances; persistence of buckets across restarts; per-user quota accounting or billing; dynamic policy reload without restart; any admin UI"
- "A denied request costs the handler nothing: the limiter decides before the handler runs" (Goals)
- "X-RateLimit-Remaining` and `X-RateLimit-Reset` are emitted on every response the limiter saw, including 429s ... They are not emitted on paths the limiter never touched" (D4)

---

## 1.1 — Rate-limit policy config shape

- **Delivers:** A loadable policy configuration: named policies (window, burst, optional per-identity key selector) declared in `config/rate-limits.yaml`, loaded once at process boot.
- **Acceptance:**
  - A policy declared in `config/rate-limits.yaml` with `window`, `burst`, and optionally `keySelector` loads successfully at boot.
  - Any reference to a policy name that does not exist in the loaded config causes the process to fail at boot, before it accepts requests — not on the first request that hits it.
  - Omitting `keySelector` on a policy is valid; a default resolution behaviour (e.g. client IP) is defined for that case.
- **Blocked by:** none

## 1.2 — Token-bucket limiter

- **Delivers:** A limiter function `check(policyName, identity) -> {allowed, remaining, resetAt}` implementing token-bucket accounting per (policy, identity), against the policy shape defined in 1.1.
- **Acceptance:**
  - `check(policyName, identity)` returns `{allowed, remaining, resetAt}` for a known policy and identity.
  - Calls within a policy's `burst` allowance inside one `window` return `allowed: true`; a call that would exceed the bucket returns `allowed: false`.
  - Buckets are keyed by the (policy, identity) pair — two different identities under the same policy are accounted independently.
  - A bucket with no activity for two full windows is expired (no longer retained), verifiable by absence of residual state after the idle period.
  - No storage backend beyond process memory is used (no external/distributed store).
- **Blocked by:** 1.1
- **Interfaces:** Consumes the policy shape (`window`, `burst`, `keySelector`) declared and loaded in 1.1; produces the `check(policyName, identity) -> {allowed, remaining, resetAt}` contract consumed by 2.1 and 3.1.

## 2.1 — Middleware wiring on the request path

- **Delivers:** Every incoming HTTP request resolves a rate-limit policy and is checked via the 1.2 limiter before the route handler runs; a denied request short-circuits with a 429 and never reaches the handler.
- **Acceptance:**
  - A request under a route with an applicable policy invokes `check()` before the handler executes.
  - A request for which `check()` returns `allowed: false` receives a 429 response and the handler is not invoked (verifiable — e.g. handler-side side effect does not occur).
  - A request for which `check()` returns `allowed: true` reaches the handler normally.
- **Blocked by:** 1.2
- **Interfaces:** Calls the `check(policyName, identity) -> {allowed, remaining, resetAt}` contract produced by 1.2. Produces the "limiter ran on this response" signal that 3.1 depends on to decide whether to emit headers.

## 2.2 — Per-route policy overrides

- **Delivers:** A route may declare a policy name that replaces the global default policy for that route only; the override is resolved once, when the route is registered, not on each request.
- **Acceptance:**
  - A route registered with an explicit policy name uses that policy for every request it handles, in place of the global default.
  - A route registered without an override continues to use the global default policy.
  - The resolution of which policy applies to a route is fixed at route-registration time: changing what "the global default" points to after registration does not change an already-registered route's resolved policy without re-registration.
  - An override naming an unknown policy fails at boot (per the global constraint from D1), not per-request.
- **Blocked by:** 2.1
- **Interfaces:** Reads policy names from the set declared in 1.1 and resolves them at the same route-registration point 2.1 wires the limiter into; the resolved policy name is what 2.1's per-request `check()` call receives for that route.

## 3.1 — Rate-limit response headers

- **Delivers:** `X-RateLimit-Remaining` and `X-RateLimit-Reset` are present on every response that passed through the limiter, including 429 responses, and absent on responses the limiter never saw.
- **Acceptance:**
  - Any response on a route where the limiter ran (allowed or denied) carries both `X-RateLimit-Remaining` and `X-RateLimit-Reset`, with values derived from the corresponding `check()` result (`remaining`, `resetAt`).
  - A 429 response carries both headers.
  - A response on a route the limiter did not run against (no policy applied) carries neither header.
- **Blocked by:** 2.1
- **Interfaces:** Consumes `remaining` and `resetAt` from the `check()` result shape produced by 1.2, and relies on 2.1 having actually invoked the limiter on the request/response pair being headered.

## 3.2 — Config YAML syntax CI check

- **Delivers:** A CI job that fails the build when any file under `config/` is not syntactically valid YAML.
- **Acceptance:**
  - CI fails when a file under `config/` contains invalid YAML syntax.
  - CI passes when every file under `config/` is syntactically valid YAML, regardless of its semantic content (the job checks syntax only — it does not validate what any particular file is supposed to contain, e.g. it does not itself catch an unknown policy name from D1).
- **Blocked by:** none
