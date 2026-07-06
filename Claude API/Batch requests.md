[docs](https://docs.claude.com/en/docs/build-with-claude/batch-processing)
The **Message Batches API** lets you send large volumes of `/v1/messages` requests asynchronously at a discount. Here's the rundown:

**How it works**

- You submit a list of requests (each with a unique `custom_id` and a normal Messages API `params` object) via `POST /v1/messages/batches`.
- Each request is processed independently, and you poll the batch or check status until it's done.
- Most batches complete within 1 hour, and you can access results once all messages have completed or after 24 hours, whichever comes first. [Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- Batches expire if processing doesn't complete within 24 hours, and results remain available for 29 days after creation. [Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

**Cost & scale**

- You can send batches of up to 10,000 queries per batch. [Claude](https://claude.com/blog/message-batches-api)
- All usage is charged at 50% of standard API prices — for both input and output tokens.
```python
import anthropic
client = anthropic.Anthropic()

# Create a batch
response = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Hello!"}]
            }
        },
        # ... more requests
    ]
)

# Poll for status
batch = client.messages.batches.retrieve(response.id)
print(batch.processing_status)  # "in_progress" -> "ended"

# Get results once ended
if batch.processing_status == "ended":
    for result in client.messages.batches.results(response.id):
        print(result.custom_id, result.result.type)
```