# Changelog

All notable changes to acplint are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-10

ACP v1 spec-conformance alignment for the runner and schema. These are general
ACP v1 fixes applicable to any ACP v1 agent, verified end-to-end against a live
ACP server bridge reaching Full Conformance (all 14 categories pass).

### Fixed

- **`protocolVersion` is an integer, not a string.** ACP v1 defines
  `ProtocolVersion` as `integer (uint16)` (`PROTOCOL_VERSION = 1`). acplint sent
  and compared the string `"1"`, which SDK-based agents reject with
  `-32602 "expected number, received string"`, failing the mandatory
  `initialization` category. The `ProtocolVersion` enum, all `initialize` send
  sites, the `protocol_version_returned` comparison, and `schema_validation`
  params now use integer `1`.
- **Permission request/response shape aligned to ACP v1.**
  - `RequestPermissionRequest` is now `{ sessionId, toolCall, options }` — the
    stale required `description` field was dropped and `toolCall` is required.
  - `PermissionOptionChoice` is now `{ optionId, name, kind }` with a
    `PermissionOptionKind` enum (`allow_once` / `allow_always` / `reject_once` /
    `reject_always`).
  - Auto-allow handlers now emit the v1 `RequestPermissionOutcome`
    discriminated union: `{ outcome: "selected", optionId }` /
    `{ outcome: "cancelled" }`.
  - `select_allow_option()` prefers an allow-kind option so a reject-first
    ordering cannot produce a false negative; no options / no allow option now
    responds `cancelled` (ACP v1 has no `minItems` on `options`) instead of a
    JSON-RPC error.
- **`PromptRequest` field, `sessionUpdate` casing, and streaming timeout.**
  - `PromptRequest` uses `prompt` (not the non-v1 `content`); renamed at the
    schema and all runner send sites.
  - `sessionUpdate` discriminator values are snake_case per the ACP SDK
    (`agent_message_chunk`, `tool_call`, `tool_call_update`, `usage_update`,
    etc.); previously camelCase constants were compared against snake_case wire
    values, causing the required `agent_message_chunk_received` check to
    false-fail.
  - `_test_streaming` now honors `--timeout` instead of a hardcoded 20s wait.

### Added

- `StopReason` gains `max_tokens`, `max_turn_requests`, and `cancelled` for ACP
  v1 alignment.

## [0.1.0] - 2026-07-10

### Added

- Initial release of acplint — the linter for the Agent Client Protocol (ACP).

[0.2.0]: https://github.com/rinadelph/acplint/releases/tag/v0.2.0
[0.1.0]: https://github.com/rinadelph/acplint/releases/tag/v0.1.0
