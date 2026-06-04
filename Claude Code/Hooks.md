---
tags: []
created: 2026-06-04
---

# Hooks

## Types

There are more hooks beyond the `PreToolUse` and `PostToolUse` hooks discussed in this course. There are also:

- `Notification` - Runs when Claude Code sends a notification, which occurs when Claude needs permission to use a tool, or after Claude Code has been idle for 60 seconds
- `Stop` - Runs when Claude Code has finished responding
- `SubagentStop` - Runs when a subagent (these are displayed as a "Task" in the UI) has finished
- `PreCompact` - Runs before a compact operation occurs, either manual or automatic
- `UserPromptSubmit` - Runs when the user submits a prompt, before Claude processes it
- `SessionStart` - Runs when starting or resuming a session
- `SessionEnd` - Runs when a session ends

![[Pasted image 20260604073508.png]]

Useful hooks

- linters
- similar existing file checker

![[Pasted image 20260604075911.png]]
