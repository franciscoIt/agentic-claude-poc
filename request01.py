import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "claude-sonnet-4-6"
MAX_TOKENS = 4096

messages_history:list= []

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def send_msg(msg: str = "Hi") -> anthropic.types.Message:
    client = _get_client()
    response: anthropic.types.Message | None = None
    try:
        messages_history.append({"role":"user","content":msg})
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=MAX_TOKENS,
            messages= messages_history
        )
        messages_history.append({"role": "assistant", "content": response.content[0].text})    
    except anthropic.AuthenticationError:
        print("Invalid API key. Check ANTHROPIC_API_KEY.")
    except anthropic.RateLimitError as e:
        retry_after = int(e.response.headers.get("retry-after", "60"))
        print(f"Rate limited. Retry after {retry_after}s.")
    except anthropic.APIConnectionError:
        print("Network error. Check your internet connection.")
    except anthropic.APIStatusError as e:
        print(f"API error ({e.status_code}): {e.message}")
        #     print(response.content[0].text)
    return response






if __name__ == "__main__":
        response = send_msg(msg="say my name")
        print(response.content[0].text)


