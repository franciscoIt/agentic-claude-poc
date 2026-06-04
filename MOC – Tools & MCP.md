---
tags: [moc]
created: 2026-06-04
---

# MOC – Tools & MCP

Giving Claude external capabilities — from the Anthropic API tool use lifecycle through the MCP protocol and its three primitives.

## API Tool Use

[[Tool use]] — Full lifecycle: write a JSON schema → call Claude → run the tool → return the `ToolResult` block. Includes the complete Anthropic built-in tool reference (Text Edit, Web Search, Fine-Grained Tool Calls) and all Claude Code Agent Tools.

## MCP Protocol

[[MCP Architecture]] — How MCP works: the three primitives (Tools / Resources / Prompts), their control model (model-controlled / app-controlled / user-controlled), and the full Client ↔ Server ↔ Claude sequence diagram.

### MCP Primitives

[[Resources]] — App-controlled data exposure via `@mcp.resource`. Covers direct resources (static URI) and templated resources (parameterised URI that receives args as function parameters).

[[FastMCP Prompt Definitions]] — User-triggered prompt templates via `@mcp.prompt`. Define reusable, high-quality instructions inside a FastMCP server instead of asking callers to write their own.

---

*See also: [[MOC – Claude API]] · [[MOC – Claude Code]]*
