---
tags: []
created: 2026-05-27
---

# Skills

Personal skills go in `~/.claude/skills` (your home directory). These follow you across all your projects — your commit message style, your documentation format, how you like code explained.

Project skills go in `.claude/skills` inside the root directory of your repository. Anyone who clones the repo gets these skills automatically. This is where team standards live, like your company's brand guidelines, preferred fonts, and colors for web design.

On Windows, personal skills live in `C:/Users/<your-user>/.claude/skills`.

## Priority Order

1. Enterprise — managed settings, highest priority
2. Personal — your home directory (`~/.claude/skills`)
3. Project — the `.claude/skills` directory inside a repository
4. Plugins — installed plugins, lowest priority

## Folder Structure

- scripts/ — Executable code
- references/ — Additional documentation
- assets/ — Images, templates, or other data files

## Writing Descriptions

- **Less that 500 lines.**
- Semantic with the prompt that will call it
- Answer:
  - What does?
  - When is it needed?
