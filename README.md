<h1 align="center">acplint</h1>

<p align="center"><strong>The linter for the Agent Client Protocol (ACP)</strong></p>

<p align="center">
Validate your AI agent implementation against the ACP specification.<br>
Catch missing hooks, broken streaming, schema violations, and more.
</p>

<p align="center">
<a href="https://pypi.org/project/acplint/"><img src="https://img.shields.io/pypi/v/acplint.svg" alt="PyPI" /></a>
<a href="https://pypi.org/project/acplint/"><img src="https://img.shields.io/pypi/pyversions/acplint.svg" alt="Python Versions" /></a>
<img src="https://img.shields.io/pypi/l/acplint.svg" alt="License" />
</p>

---

## What is ACP?

The **Agent Client Protocol (ACP)** is a JSON-RPC 2.0 protocol for communication between AI coding agents and their clients (IDEs, CLIs, editors). It's used by [Zed](https://zed.dev) and other tools that integrate AI agents. If you're building an ACP-compatible agent, `acplint` makes sure you're doing it right.

## What does acplint do?

Like `eslint` for JavaScript or `pylint` for Python, **acplint** checks your agent implementation against the ACP specification and reports what's missing, broken, or non-conformant.

It catches:

- **Missing capabilities** — agent doesn't advertise hooks, sub-agent support, skills
- **Broken streaming** — missing `agentMessageChunk` / `agentThoughtChunk` notifications
- **Schema violations** — wrong field names, missing required fields, invalid types (with exact field paths)
- **Tool call issues** — missing raw output, broken status transitions, missing content
- **Protocol errors** — wrong JSON-RPC responses, missing session updates, bad initialization

## Install

```bash
pip install acplint
```

## Quick Start

Test any ACP agent via stdio:

```bash
# Test Claude Code
acplint --agent claude-code --agent-args "--acp"

# Test a custom agent
acplint --agent "my-agent" --agent-args "--stdio --model=gpt-4"
```

## 14 Test Categories

| Category | What it validates |
|---|---|
| `initialization` | Protocol handshake, version negotiation, capabilities |
| `authentication` | Auth method discovery, authenticate, logout |
| `session_lifecycle` | new/load/resume/close/list/delete/fork sessions |
| `streaming` | All 11 `session/update` notification types |
| `tool_calls` | Full lifecycle: raw input/output, content, status, sub-agent/skills meta |
| `permissions` | `request_permission` flow, auto-approve detection |
| `file_operations` | `fs/read_text_file`, `fs/write_text_file` |
| `terminals` | `terminal/create`, output, release, kill, wait_for_exit |
| `plans` | `plan` notification detection and validation |
| `session_modes` | `session/set_mode` |
| `config_options` | `session/set_config_option` |
| `cancel` | `session/cancel` notification handling |
| `stress` | Rapid prompts, concurrent sessions, large content |
| `schema_validation` | Strict Pydantic validation on every method response |

## Conformance Levels

| Level | Meaning |
|---|---|
| ✅ **Full Conformance** | All mandatory tests pass |
| ⚠️ **Partial Conformance** | Core tests pass, some optional capability tests fail |
| ❌ **Non-Conformant** | Core protocol tests fail |

## Python API

```python
from acplint import ConformanceRunner

runner = ConformanceRunner(agent_command=["my-agent", "--stdio"])
report = runner.run_all()
report.print_summary()

# Programmatic access
print(report.conformance_level)
print(report.passed_tests)
print(report.findings)
```

## CI Integration

```bash
# JSON output for pipelines
acplint --agent "my-agent" --output json --output-file results.json

# Exit codes: 0=full, 1=partial, 2=non-conformant
acplint --agent "my-agent" && echo "Agent is ACP-conformant!"
```

## Why "acplint"?

Because every protocol deserves a linter. `acplint` checks your agent against the ACP spec the same way `eslint` checks your JS against a style guide. If it passes `acplint`, your agent speaks ACP correctly.

## License

Apache-2.0
