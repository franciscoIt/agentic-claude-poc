---
tags: [moc]
created: 2026-06-04
---

# MOC – Claude Code

Claude Code is Anthropic's CLI and IDE integration for AI-assisted development. This hub covers how to configure a project, what components exist at runtime, and how to operate them effectively.

## Overview

[[Claude Resource Types]] — Comparison table of all Claude Code components: CLAUDE.md, Skills, Subagents, Hooks, and MCP Servers — when each loads and what it's best for.

## Setup

[[Setting up a project]] — Run `/init` to generate CLAUDE.md and understand the three-level config hierarchy (project / local / global).

## Components

[[Skills]] — Reusable task-specific workflows. Covers personal vs project skill locations, priority order (Enterprise → Personal → Project → Plugins), folder structure, and description guidelines.

[[Hooks]] — Event-driven shell commands that react to Claude's lifecycle: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `UserPromptSubmit`, and more.

## Workflow

[[When to Use Planning vs Effort]] — Choose between Planning Mode (breadth, multi-file changes) and higher effort levels (depth, complex logic and debugging).

[[Claude Code Custom Commands]] — Define reusable slash commands in `.claude/commands/` and use `/compact` to summarise and compress context.

## Reference

[[Models]] — Available Claude models.

---

*See also: [[MOC – Claude API]] · [[MOC – Tools & MCP]]*
