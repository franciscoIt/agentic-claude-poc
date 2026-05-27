---
name: obsidian-formater
description: Format and structure notes for Obsidian — apply consistent Markdown conventions, add frontmatter, fix headings, linkify wiki-links, and clean up whitespace. Trigger when the user asks to format, clean, or prepare notes for Obsidian.
usage: /obsidian-formater [file or content]
---

# Obsidian Formatter Skill

You are executing the `obsidian-formater` skill. Your job is to take raw or messy notes and reformat them to be clean, consistent, and Obsidian-ready.

## What to do

1. **Read the target** — if the user gave a file path, read it; if they pasted content, use that directly.
2. **Apply formatting rules** (see below).
3. **Write the result** — overwrite the file in place, or output the formatted content if no file was given.
4. **Report** — one sentence: what changed.

## Formatting rules

### Frontmatter
- If no YAML frontmatter exists, add a minimal block at the top:
  ```yaml
  ---
  tags: []
  created: <today's date in YYYY-MM-DD>
  ---
  ```
- If frontmatter exists, preserve existing keys; only add `created` if missing.

### Headings
- Ensure there is exactly one `# Title` at the top (after frontmatter).
- Promote headings if the document starts at `##` with no `#`.
- Never skip heading levels (e.g., `##` → `####`); insert intermediate levels if needed.

### Wiki-links
- Convert bare URLs that point to internal notes (`[[Note Name]]`) if the user has already indicated a pattern.
- Leave external URLs (`https://...`) as standard Markdown links `[text](url)`.

### Lists
- Normalize unordered list markers to `-`.
- Remove trailing spaces from list items.

### Whitespace
- One blank line between sections.
- No trailing whitespace on any line.
- File ends with a single newline.

### Callouts (Obsidian syntax)
- Preserve existing `> [!NOTE]` / `> [!WARNING]` callout blocks as-is.

## Constraints
- Do not rewrite prose or change meaning — only fix structure and syntax.
- Do not remove any content.
- Preserve code blocks exactly.
