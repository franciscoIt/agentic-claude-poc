![[Pasted image 20260601122816.png]]

![[Pasted image 20260601123544.png]]

![[Pasted image 20260601124104.png]]

![[Pasted image 20260601151752.png]]

- [[Fine grained tool call (bypass claude json validation)]]
- [[text edit tool]]
- [[Web search tool]]


"- `web_search`
- `web_fetch`
- `code_execution`
- `tool_search`"
  

[](https://gemini.google.com/library)

[](https://gemini.google.com/gems/view)

[](https://gemini.google.com/videos)

[](https://gemini.google.com/library)

[](https://gemini.google.com/gems/view)

[

](https://accounts.google.com/SignOutOptions?continue=https://gemini.google.com)

# Conversation with Gemini

according to claude code api interaction, what is a textBlock

In the Anthropic Claude API (and by extension, Claude Code interactions), a **`TextBlock`** is a specific object used to represent a chunk of text within a message.

Claude Console

Because Claude's Messages API supports complex, multi-step, and multimodal interactions, the `content` of a message isn't always just a single string. Instead, it is formatted as an array of distinct "blocks." A `TextBlock` is simply the block designated for standard text, co-existing alongside other types of blocks like images or tool calls.

### Structure of a `TextBlock`

When interacting with the API, a `TextBlock` contains the following core fields:

- **`type`**: Always strictly set to `"text"` to identify the block's format.
    
- **`text`**: The actual string of text content being sent to or received from Claude.
    
- **`citations`** _(Optional)_: An array of citation objects. If Claude is referencing uploaded files (like PDFs) or web search results, it will populate this field with the exact locations (e.g., page numbers or character indexes) that support the generated text.
    
    Claude Console
    

### Code Examples

**JSON Representation (API payload):** If you are sending a message with a `TextBlock`, it looks like this:

JSON

```
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "Can you review this specific Python script?"
    }
  ]
}
```

_(Note: Passing a simple string like `"content": "Hello"` is allowed in the API as a shorthand, but under the hood, the API automatically converts it into an array containing a single `TextBlock`.)_

Claude Console

**Python SDK Representation (Response):** When you receive a generated response using the Anthropic Python SDK, the text is returned as a specific `TextBlock` Python object:

Python

```
[TextBlock(text='Here is the review of your script...', type='text', citations=None)]
```

### Why use Blocks instead of simple strings?

Structuring message content into discrete blocks is essential for advanced AI interactions. It allows you to seamlessly mix and match different types of data within a single conversational turn:

- **Multimodal Input:** Sending an image next to a prompt (combining an `ImageBlock` with a `TextBlock`).
    
- **Tool Use (Agents):** Allowing Claude to output its thought process (`TextBlock`), followed immediately by a command to execute a function or code (`ToolUseBlock`), all in the same response.
    
- **Extended Thinking:** When using advanced reasoning models, Claude can return a `ThinkingBlock` (exposing its internal, step-by-step logic) followed by a final `TextBlock` (the polished answer presented to the user).
    

type of tools in claude code

In Claude Code, tools give the AI agent the ability to interact with your local environment, codebase, and external services. Rather than relying on a single monolithic toolset, Claude Code categorizes its built-in tools into several distinct types based on their function.

Claude Code by Anthropic | AI Coding Agent, Terminal, IDE+ 1

Here is a breakdown of the primary types of tools available in Claude Code:

### 1. File & Code Navigation Tools

These tools allow Claude to read, search, and understand your project structure without executing code.

- **`Read`**: Reads the contents of specific files (preferred over bash commands like `cat`).
    
- **`Glob`**: Finds files based on pattern matching, useful for exploring directories.
    
    vtrivedy
    
- **`Grep`**: Searches for specific code patterns, strings, or regex within file contents.
    
    GitHub Gist
    
- **`LSP`**: Provides deep code intelligence via Language Servers (e.g., jump to definitions, find references, and check for type errors).
    
    Claude Code by Anthropic | AI Coding Agent, Terminal, IDE
    

### 2. File Editing Tools

When Claude needs to write or modify code, it uses specialized editing tools rather than attempting to rewrite whole files via standard shell commands.

vtrivedy

- **`Edit`**: Makes targeted, precise edits to specific lines or blocks within a file.
    
    vtrivedy
    
- **`NotebookEdit`**: Specifically designed to modify and manage Jupyter notebook cells.
    
    vtrivedy
    

### 3. Execution & System Tools

These tools grant Claude the ability to run commands directly in your terminal environment. Because these can modify your system, they usually require user permission.

Claude Code by Anthropic | AI Coding Agent, Terminal, IDE

- **`Bash` / `PowerShell`**: Executes standard shell commands in your environment to run builds, tests, or git commands.
    
    Claude Code by Anthropic | AI Coding Agent, Terminal, IDE
    
- **`Monitor`**: Runs a command in the background and streams the output line-by-line back to Claude. This allows the agent to react to server logs, file changes, or polling statuses in real time.
    
    Claude Code by Anthropic | AI Coding Agent, Terminal, IDE
    
- **`EnterWorktree` / `ExitWorktree`**: Creates and manages isolated Git worktrees, allowing Claude to work on a task in a clean environment without disrupting your current branch.
    

### 4. Agent & Orchestration Tools

Claude Code can act as a manager, spinning up sub-agents to handle complex workflows or parallel tasks.

vtrivedy

- **`Agent`**: Spawns a dedicated sub-agent with its own context window to tackle a specific sub-task autonomously.
    
    Claude Code by Anthropic | AI Coding Agent, Terminal, IDE
    
- **Task Management (`TaskCreate`, `TaskList`, `TaskUpdate`, `TaskStop`)**: A suite of tools to create, monitor, and kill background tasks or asynchronous jobs.
    
    GitHub Gist
    
- **`SendMessage`**: Allows communication between different agents in an agent team.
    

### 5. Planning & Interaction Tools

These tools dictate how Claude interacts with you, the user, to ensure it understands the requirements before acting.

- **`EnterPlanMode` / `ExitPlanMode`**: Switches the agent into a planning state to outline an approach. It uses `ExitPlanMode` to present the final plan for your approval before writing any code.
    
- **`AskUserQuestion`**: Halts execution to ask you multiple-choice or clarifying questions to resolve ambiguity.
    
- **`PushNotification`**: Sends a desktop or mobile notification to alert you when a long-running task is complete.
    

### 6. Extensibility Tools (MCP & Skills)

Claude Code is highly extensible, allowing it to connect to external databases, APIs, or company-specific workflows.

Claude Code by Anthropic | AI Coding Agent, Terminal, IDE

- **`ListMcpResourcesTool` / `ReadMcpResourceTool`**: Interfaces with Model Context Protocol (MCP) servers to pull in external context (like Jira tickets, Slack messages, or database schemas).
    
- **`Skill`**: Executes a predefined, reusable workflow or "skill" that you have installed in your project.
    

Are there any specific tools or workflows from this list that you'd like to explore in more detail?

according to the type in json schema

When you look at how tools are actually defined under the hood in the Anthropic Claude API's JSON payload, the logical categories from Claude Code are mapped using a specific **`type`** property.

According to the API specification, there are two distinct ways the `type` field handles tools:

### 1. Custom Tools (`"type": "custom"`)

This is the default tool type. Most of the specialized tools in Claude Code (like `Read`, `Glob`, `Grep`, or `Agent`) are sent to the API as `"custom"` tools.

- **How it works:** When the type is `"custom"`, you **must** provide an `input_schema` object.
    
- **The Schema Structure:** This block uses standard JSON Schema definitions. You dictate the exact parameters your tool accepts by mapping them to JSON Schema data types (`string`, `number`, `integer`, `boolean`, `object`, `array`, `null`).
    
    Claude Console
    

**API Payload Example:**

JSON

```
{
  "name": "glob",
  "description": "Find files based on pattern matching.",
  "type": "custom",
  "input_schema": {
    "type": "object",
    "properties": {
      "pattern": { 
        "type": "string",
        "description": "The file pattern to search for."
      }
    },
    "required": ["pattern"]
  }
}
```

### 2. Built-In System Tools

Anthropic natively hosts several system-level tools (introduced alongside their Computer Use beta). For these, the `type` field maps directly to Anthropic's versioned identifier rather than `"custom"`.

Go Packages

- **How it works:** Because Anthropic's backend already strictly understands the input requirements for these tools, you **do not** provide an `input_schema` in your JSON request.
    
- **Built-in Types Include:**
    
    - `"bash_20241022"` or `"bash_20250124"` (Claude Code uses this to execute terminal shell commands).
        
    - `"text_editor_20241022"` or `"text_editor_20250124"` (Claude Code uses this for precise file modification).
        
    - `"computer_20241022"` or `"computer_20251124"` (Used for visual screen interaction and mouse control).
        

**API Payload Example:**

JSON

```
{
  "name": "bash",
  "type": "bash_20250124"
}
```

### Bonus Context: Structured Outputs

If you meant how to force Claude to return a JSON Schema _without_ executing a tool, the API uses a feature called Structured Outputs. In this context, you set the `type` inside the `output_config.format` parameter to `"json_schema"`, passing the exact JSON Schema you want Claude's text response to conform to.

list the build in tools

According to the Anthropic API documentation, there are several "built-in" tools. These tools are predefined by Anthropic, meaning their underlying schemas are already understood by the model. When sending them in the API payload, you omit the `input_schema` and instead use a specific, version-dated string for the `type` property.

Claude Console

Anthropic divides these into **Client tools** (where your application, like Claude Code, executes the action) and **Server tools** (where the execution happens directly on Anthropic's infrastructure).

Claude Console

Here is the definitive list of built-in tools and their JSON schema `type` identifiers:

### Built-In Client Tools

These tools require the host application to run the commands and return the results to Claude.

Claude Console

|Tool Name|JSON `type` Identifiers|Functionality|
|---|---|---|
|**Bash**|`"bash_20250124"`, `"bash_20241022"`|Executes standard shell commands within your environment (used heavily by Claude Code for terminal interaction).|
|**Text Editor**|`"text_editor_20250728"`, `"text_editor_20250124"`, `"text_editor_20241022"`|Makes targeted edits, modifications, and reads to specific files or file blocks without needing standard shell utilities.|
|**Computer Use**|`"computer_20251124"`, `"computer_20250124"`, `"computer_20241022"`|Interacts with a visual desktop environment, allowing Claude to simulate mouse clicks, keystrokes, and read screen pixels.|
|**Memory**|`"memory_20250818"`|Allows Claude to store, update, and consult persistent information across different sessions and conversations.|

### Built-In Server Tools

These tools execute remotely on Anthropic's end, and the results are injected directly back into the context window.

|Tool Name|JSON `type` Identifiers|Functionality|
|---|---|---|
|**Web Search**|`"web_search_20260209"`, `"web_search_20250305"`|Searches the open web for up-to-date information, automatically returning data alongside natural citations.|
|**Web Fetch**|`"web_fetch_20260209"`, `"web_fetch_20250910"`|Fetches and parses the raw content of specific URLs.|
|**Code Execution**|`"code_execution_20260120"`, `"code_execution_20250825"`, `"code_execution_20250522"`|Runs Python or Bash code directly inside a secure Anthropic sandbox to solve math, process data, or debug logic.|
|**Tool Search**|`"tool_search_tool_regex_20251119"`, `"tool_search_tool_bm25_20251119"`|Dynamically discovers and loads tools on-demand from large internal tool catalogs or databases.|
|**Advisor**|`"advisor_20260301"`|A specialized server tool intended for guidance and review.|
|**MCP Connector**|`"mcp_toolset"`|Connects to external systems (Model Context Protocol), allowing integration with databases, enterprise APIs, or browsers.|

> **Note on Versioning:** Anthropic appends a `_YYYYMMDD` suffix to built-in tools. They release new versions when the tool's behavior, schema, or model support changes (e.g., `"code_execution_20260120"` adds programmatic tool-calling capabilities over older versions). Multiple versions often remain active simultaneously to prevent breaking older integrations.
> 
> Claude Console

list them all ```markdown

Here is the complete list of Anthropic's built-in tools and their JSON schema `type` identifiers, organized by execution environment.

### 🖥️ Client Tools (Dynamic Execution)

These tools require your application (the client) to execute the commands and pass the results back to Claude.

LangChain Reference Docs

|Tool Name|JSON `type` Identifiers|Core Functionality|
|---|---|---|
|**Bash**|`bash_20250124`<br><br>  <br><br>`bash_20241022`|Executes standard shell commands in a persistent bash session (includes session restart support).|
|**Text Editor**|`text_editor_20250728`<br><br>  <br><br>`text_editor_20250124`<br><br>  <br><br>`text_editor_20241022`|Views and modifies text files natively without shell utilities. Commands include `view`, `str_replace`, `create`, and `insert`.|
|**Computer Use**|`computer_20251124`<br><br>  <br><br>`computer_20250124`<br><br>  <br><br>`computer_20241022`|Provides desktop automation by simulating mouse movements, keystrokes, zooming, and reading screen pixels via screenshots.|
|**Memory**|`memory_20250818`|Stores and retrieves information across multiple conversations via a persistent memory file directory.|

### ☁️ Server Tools (Managed Execution)