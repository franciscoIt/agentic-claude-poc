---
tags: []
created: 2026-05-29
---

# Structure Data (Force It)

Solution recommended is to use an strategy of

## Message Prefilling + Stop Sequences

``` python
response = client.messages.create(
    model="claude-sonnet-4-5",  # prefill works here
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract the name, age, and city from: 'Maria is 34 years old and lives in Madrid.'"
        },
        {
            "role": "assistant",
            "content": "```json"   # <-- PREFILL: forces Claude to open a JSON block
        }
    ],
    stop_sequences=["```"]        # <-- STOP: halts generation at closing ```
)
```
