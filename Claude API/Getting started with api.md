---
tags: []
created: 2026-05-29
---

# Getting Started with API

Install globaly the dependencies. change <py> per your python executable name

```
uv pip install anthropic python-dotenv --python py --system
```

or to create a virtual environment run:
`uv venv`

> [!NOTE]
> Claude API is stateless — there is no built-in conversation history. Each request must include the full message history to give Claude context.
