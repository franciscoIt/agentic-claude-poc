---
tags: [moc]
created: 2026-06-04
---

# MOC – Claude API

Core concepts for building applications with the Claude API — from client setup through behaviour control and advanced performance features.

## Setup

[[Getting started with api]] — Install the SDK (`anthropic`, `python-dotenv`), create a virtual environment, and understand the stateless request model.

## Behaviour Control

[[System prompt]] — Define Claude's role, persona, and constraints before the conversation begins.

[[temperature]] — Low (0–0.3) for factual and code tasks; medium (0.4–0.7) for balanced output; high (0.8–1.0) for creative work.

[[Force Structured JSON Output]] — Use message prefilling + stop sequences to guarantee JSON-shaped output without an external schema validator.

## Advanced Features

[[Extended thinking]] — Enable deeper reasoning with `thinking: true` and `budget_tokens`. Returns encrypted `redacted_thinking` blocks alongside the response.

[[Caching]] — Attach `cache_control` to content blocks to reduce latency and cost on repeated large contexts.

---

*See also: [[MOC – Data & Inputs]] · [[MOC – Tools & MCP]] · [[MOC – Prompt Engineering & RAG]]*
