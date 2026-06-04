---
tags: []
created: 2026-05-27
---

# Claude ? Types

| Concept         | When it loads                         | Best for                                              | Key distinction from Skills                                                 |
| --------------- | ------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------- |
| **CLAUDE.md**   | Every conversation, always-on         | Project-wide standards, conventions, persistent rules | Skills load on demand; CLAUDE.md is always present                          |
| **Skills**      | On demand, request-driven             | Task-specific expertise, specialized workflows        |                                                                             |
| **Subagents**   | Triggered by orchestrator tool calls  | Delegated work in isolated execution contexts         | Skills add knowledge to your conversation; subagents run separately         |
| **Hooks**       | Event-driven (file saves, tool calls) | Oversight, guardrails, reacting to Claude's actions   | Skills activate based on what you're asking; hooks fire on lifecycle events |
| **MCP Servers** | Connected per session                 | External tools, APIs, third-party integrations        | A different category entirely — provide tools, not knowledge                |
