---
tags: []
created: 2026-06-02
---

# Tool Use

[Documentationf](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)

![[Pasted image 20260601122816.png]]

![[Pasted image 20260601123544.png]]

![[Pasted image 20260601124104.png]]

![[Pasted image 20260601151752.png]]

- [[Fine grained tool call (bypass claude json validation)]]
- [[text edit tool]]
- [[Web search tool]]

## Anthropic API Built-In Tools

| Approach                      | When to use it                                                | What to expect                                                                        | Learn more                                                                                     |
| ----------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| User-defined client tools     | Custom business logic, internal APIs, proprietary data        | You handle execution and the agentic loop                                             | [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)     |
| Anthropic-schema client tools | Standard dev operations (bash, file editing, browser control) | You handle execution; Claude calls the tool reliably because the schema is trained-in | [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference) |
| Server-executed tools         | Web search, code sandbox, web fetch                           | Anthropic handles execution; you get results directly                                 | [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools)     |

### Client Tools (Executed by your application)

- **Bash** (`bash_20250124`, `bash_20241022`): Executes persistent shell commands.
- **Text Editor** (`text_editor_20250728`, `text_editor_20250124`, `text_editor_20241022`): Views and modifies files.
- **Computer Use** (`computer_20251124`, `computer_20250124`, `computer_20241022`): Automates desktop UI (mouse/keyboard/screen).
- **Memory** (`memory_20250818`): Stores persistent cross-conversation data.

### Server Tools (Executed on Anthropic's infrastructure)

- **Web Search** (`web_search_20250305`): Performs open web searches.
- **Web Fetch** (`web_fetch_20250910`): Extracts raw page/PDF content.
- **Code Execution** (`code_execution_20250825`): Runs code in a secure sandbox.
- **Tool Search (Regex)** (`tool_search_tool_regex_20251119`): Discovers tools via regex.
- **Tool Search (BM25)** (`tool_search_tool_bm25_20251119`): Discovers tools via natural language.
- **MCP Toolset** (`mcp_toolset_20251120`): Connects to remote MCP servers.

---

## Claude Code Agent Tools

These tools are injected into the agent's context using the standard `"type": "custom"` JSON Schema definition.

### File & Code Navigation

- **Read**: Reads file contents (up to 2000 lines) with line numbers.
- **Glob**: Finds files based on pattern matching.
- **Grep**: Searches code patterns/strings via regex (`ripgrep`).
- **LS**: Lists directory contents.
- **LSP**: Language Server Protocol integration for code intelligence.

### File Editing

- **Write**: Creates or completely overwrites files.
- **Edit**: Makes targeted string replacements in specific file locations.
- **MultiEdit**: Modifies multiple file sections simultaneously.
- **NotebookRead**: Parses and reads Jupyter Notebooks natively.
- **NotebookEdit**: Modifies Jupyter Notebook cells safely.

### Execution & System

- **Monitor**: Runs commands in the background and streams output.
- **EnterWorktree** / **ExitWorktree**: Creates and manages isolated Git worktrees.

### Agent & Orchestration

- **Agent**: Spawns sub-agents for concurrent or specialized tasks.
- **TaskCreate** / **TaskList** / **TaskUpdate** / **TaskStop**: Manages asynchronous background tasks.
- **SendMessage**: Allows communication between sub-agents.
- **TodoRead** / **TodoWrite**: Reads and updates project task lists.

### Planning & Interaction

- **EnterPlanMode** / **exit_plan_mode**: Toggles planning state and requests user approval for actions.
- **AskUserQuestion**: Halts execution to ask multiple-choice or clarifying questions.
- **PushNotification**: Sends desktop/mobile alerts for completed background tasks.

### Extensibility & Network

- **WebFetch**: Pulls raw content from specific URLs.
- **WebSearch**: Performs external web searches for context.
- **ListMcpResourcesTool** / **ReadMcpResourceTool**: Interfaces with local MCP servers.
- **Skill**: Executes user-defined, reusable project workflows.
