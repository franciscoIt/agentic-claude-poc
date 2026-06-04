---
tags: []
created: 2026-05-29
---

# System Prompt

- System prompts provide Claude guidance on how to respond
- Claude will try to respond in the same way someone in the specified role would respond
- Helps keep Claude on task
- It's like a gem, a description or a SKILL.md

```python
system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
client.messages.create(
    model=model,
    messages=messages,
    max_tokens=1000,
    **[[system]]=system_prompt**
    
)
```

![[Pasted image 20260602123952.png]]
