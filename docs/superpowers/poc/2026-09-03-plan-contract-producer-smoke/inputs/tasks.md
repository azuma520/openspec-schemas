## 1. Policy model

- [ ] 1.1 Define the rate-limit policy config shape: a named policy carries a window (seconds), a burst allowance, and an optional per-identity key selector. Policies are declared in `config/rate-limits.yaml` and loaded once at boot; an unknown policy name referenced anywhere is a boot-time failure, not a request-time one
  - TDD: applicable
- [ ] 1.2 Implement the token-bucket limiter against the policy shape from 1.1: `check(policyName, identity) -> {allowed, remaining, resetAt}`. Buckets are per (policy, identity) and expire after two windows of inactivity. No storage backend beyond process memory in this change
  - TDD: applicable

## 2. Request path

- [ ] 2.1 Wire the limiter into the HTTP middleware chain so every request resolves a policy before the handler runs. A request whose policy denies it returns 429 and never reaches the handler
  - TDD: applicable
- [ ] 2.2 Support per-route policy overrides: a route may name a policy that replaces the global default for that route only. Overrides are resolved at route-registration time, not per request
  - TDD: applicable

## 3. Surfaces

- [ ] 3.1 Emit `X-RateLimit-Remaining` and `X-RateLimit-Reset` on every response that passed through the limiter, including the 429 responses
  - TDD: applicable
- [ ] 3.2 Add a CI job that fails the build when any file under `config/` does not parse as YAML. It checks syntax only — it does not know or validate what any particular file is supposed to contain
  - TDD: n/a — configuration
