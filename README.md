# openspec-schemas

[English](./README.md) · [繁體中文](./README.zh-TW.md)

Community-contributed [OpenSpec](https://github.com/Fission-AI/OpenSpec) schemas. Each schema is a self-contained bundle that you copy into your project's `openspec/schemas/` directory and select per-change with `--schema <name>`.

## Bridges in this repository

| Bridge | Purpose | Status |
|--------|---------|--------|
| [`superpowers-bridge`](./superpowers-bridge/) | Bridges OpenSpec's artifact governance with [obra/superpowers](https://github.com/obra/superpowers) execution skills (brainstorming, subagent execution with structural code review, finishing). Each task carries a TDD applicability annotation and RED/GREEN evidence; verify's deterministic checks read the presence and structure of that evidence before archive, instruction-mediated rather than a mechanically enforced, non-bypassable gate. Adds an evidence-first `retrospective` artifact filling a gap Superpowers does not natively cover. | v2 |

## Why a separate repository?

[OpenSpec PR #970](https://github.com/Fission-AI/OpenSpec/pull/970) originally proposed `sdd-plus-superpowers` as a built-in schema. After maintainer review, the integration moved to a community repository — same pattern as [github/spec-kit's community extension catalog](https://speckit-community.github.io/extensions/), which keeps third-party tool integrations out of core.

Benefits:
- OpenSpec core does not take on Superpowers' release cadence
- Bridge can iterate independently
- Other community schemas can join this repository as siblings

## Install

Each bridge directory has its own `README.md` with a copy-paste Claude Code prompt for one-shot installation, plus a manual bash alternative. See e.g. [`superpowers-bridge/README.md#install`](./superpowers-bridge/README.md#install).

## Roadmap

See [`docs/roadmap.md`](./docs/roadmap.md) for what's planned.

## License

MIT — see [LICENSE](./LICENSE).
