### `context: fork` in Claude Code

It's a frontmatter field you can add to a `SKILL.md` file (or a slash-command file) that controls **where** the skill runs.

**The problem it solves**: when a skill produces verbose output — scanning hundreds of files, generating long reports — that output consumes your conversation's context. Next time you ask Claude a question, it has less room to think because the skill's output is taking up space. [Panaversity](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/claude-code-teams-cicd/custom-skills-with-frontmatter)

**How it works**: adding `context: fork` to a skill's frontmatter runs that skill in an isolated sub-agent context with its own independent conversation history and tool access, instead of executing inline in the main conversation. The subagent does all the heavy work, then returns just a summary to your main conversation. [ClaudeLog](https://claudelog.com/faqs/what-is-context-fork-in-claude-code/)[Panaversity](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/claude-code-teams-cicd/custom-skills-with-frontmatter)