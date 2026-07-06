# Claude API — `/v1/messages` Cheatsheet

Endpoint: `POST /v1/messages` · SDK: `client.messages.create(...)`

## Required parameters

|Parameter|Type|Description|
|---|---|---|
|`model`|string|Model ID, e.g. `claude-opus-4-8`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`|
|`messages`|array|Conversation turns: `[{"role": "user"/"assistant", "content": ...}]`. Content can be a string or an array of content blocks (text, image, document, tool_use, tool_result, thinking).|
|`max_tokens`|integer|Maximum tokens to generate. Anthropic requires this explicitly (unlike some other providers, which can auto-determine it).|

## Common optional parameters

|Parameter|Type|Description|
|---|---|---|
|`system`|string or array|System prompt, kept separate from the `messages` array. Can be a string or an array of text blocks (e.g. for cache_control).|
|`temperature`|float (0–1)|Controls randomness. Lower = more deterministic. ⚠️ Not supported on Claude Opus 4.7+ (including Opus 4.8) — omit it or you'll get a 400 error.|
|`top_p`|float|Nucleus sampling — considers tokens within a cumulative probability mass. Same Opus 4.7+ restriction as `temperature`.|
|`top_k`|integer|Limits sampling to the top K most likely tokens. Anthropic-specific (not in OpenAI's API). Same Opus 4.7+ restriction.|
|`stop_sequences`|array of strings|Custom strings that halt generation when produced.|
|`stream`|boolean|Enables server-sent event (SSE) streaming of the response.|
|`metadata`|object|Arbitrary tagging, e.g. `{"user_id": "..."}` — useful for analytics/debugging, not sent to the model.|
|`tools`|array|Tool/function definitions Claude may call. Each has `name`, `description`, `input_schema` (or is a built-in server tool like `web_search`, `code_execution`, `bash`, `text_editor`).|
|`tool_choice`|object|Controls tool invocation: `{"type": "auto"}` (default), `{"type": "any"}`, `{"type": "tool", "name": "..."}`, or `{"type": "none"}`. Add `"disable_parallel_tool_use": true` to cap at one tool call.|
|`thinking`|object|Enables extended thinking, e.g. `{"type": "enabled", "budget_tokens": N}` (or `"adaptive"` on newer models). Only compatible with `tool_choice: auto` or `none`.|
|`service_tier`|string|Priority/routing tier, e.g. `"auto"` or `"standard_only"`.|

## Less-common / newer parameters

| Parameter                          | Type   | Description                                                                                                     |
| ---------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------- |
| `output_format` / `output_config`  | object | Structured outputs — constrain the response to a JSON schema.                                                   |
| `speed`                            | string | `"standard"` or `"fast"` — trades latency for throughput on supported models.                                   |
| `mcp_servers`                      | array  | Connect remote MCP servers directly from the Messages API without a separate MCP client.                        |
| `container`                        | object | Reference/reuse a code execution container across requests.                                                     |
| `betas` (header: `anthropic-beta`) | list   | Opt into beta features (e.g. `interleaved-thinking-2025-05-14`, structured outputs, programmatic tool calling). |

## Required headers

|Header|Description|
|---|---|
|`x-api-key`|Your API key (handled automatically by SDKs).|
|`anthropic-version`|API version string, e.g. `2023-06-01`.|
|`content-type`|`application/json`|
|`anthropic-beta`|Comma-separated beta feature flags, only when using beta features.|

## Context management

These control how conversation history/context is handled as it grows. Mostly beta features, set via `context_management` (plus the relevant `betas` header flag) rather than a plain top-level parameter.

|Feature|How it's set|Description|
|---|---|---|
|`cache_control`|Field on a content block (in `system`, `messages`, or `tools`), or top-level for automatic caching|Marks a prefix for prompt caching so repeated context isn't reprocessed. Cache order: tools → system → messages. Default TTL 5 min (1 hr available at 2x price).|
|Compaction|`context_management={"edits": [{"type": "compact_20260112"}]}` + `betas=["compact-2026-01-12"]`|Server-side: once nearing the context window limit, automatically summarizes older history into a compact block and continues. Recommended over manual/SDK compaction.|
|Context editing|`context_management={"edits": [{"type": "clear_tool_uses_20250919"}]}` + `betas=["context-management-2025-06-27"]`|Selectively clears stale content (e.g. old tool results, thinking blocks) rather than summarizing — prunes instead of compresses.|
|`container`|Top-level object|Reuse a code-execution container/context across multiple requests.|

There's no single `context` request parameter — "context" here is a family of features (caching, compaction, editing) layered on top of the plain `messages` array, since the API itself is stateless and you always resend full history.

## Response fields (for reference)

|Field|Description|
|---|---|
|`id`|Unique message ID.|
|`type`|Always `"message"`.|
|`role`|Always `"assistant"`.|
|`content`|Array of content blocks: text, tool_use, thinking, etc.|
|`model`|Model that generated the response.|
|`stop_reason`|`end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, or `refusal`.|
|`stop_sequence`|Which stop sequence was hit, if any.|
|`usage`|`input_tokens`, `output_tokens`, plus cache-related counts (`cache_creation_input_tokens`, `cache_read_input_tokens`) when prompt caching is used.|

## Quick minimal example

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    system="You are a concise assistant.",
    messages=[{"role": "user", "content": "Hello, Claude"}],
)

print(message.content[0].text)
```

## Notes & gotchas

- The Messages API is **stateless** — you must resend the full conversation history on every call.
- `temperature`, `top_p`, and `top_k` are **not supported on Claude Opus 4.7 and later** (including Opus 4.8). Omit them entirely on those models and steer behavior via prompting instead.
- `tool_choice: any` or `tool_choice: {"type": "tool", ...}` **cannot** be combined with extended thinking — only `auto` or `none` work there.
- You can prefill part of Claude's response by ending your `messages` array with an `assistant`-role message; Claude will continue from where you left off.

---

_Compiled from Anthropic's Claude API documentation, July 2026. Parameters and model availability change — check [docs.claude.com](https://docs.claude.com/) for the latest._