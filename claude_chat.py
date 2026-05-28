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


def send_msg(msg: str = "Hi", system: str | None = None, temperature: float | None = None) -> anthropic.types.Message | None:
    client = _get_client()
    response: anthropic.types.Message | None = None
    try:
        messages_history.append({"role": "user", "content": msg})
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=MAX_TOKENS,
            messages=messages_history,
            **({"temperature": temperature} if temperature else {}),
            **({"system": system} if system else {}),
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

def chat(system: str | None = None, temperature: float | None = None):
    print("Chat with Claude  |  type 'exit' or 'quit' to stop\n")
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not msg:
            continue
        if msg.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = send_msg(msg, system, temperature)
        if response:
            text = "\n".join(
                block.text for block in response.content if block.type == "text"
            )
            print(f"Claude: {text}\n")


_JSON_STOP ="```"
# Prefilling is not supported on claude-sonnet-4-6 / claude-opus-4-6+.
# claude-haiku-4-5 is the default here because it supports the technique.
_JSON_MODEL_ID = "claude-haiku-4-5"


def ask_json(prompt: str, system: str | None = None) -> str | None:
    """Ask Claude for a JSON response using message prefilling + stop sequences.

    Prefills the assistant turn with '{' to force a JSON object, then stops
    generation at _JSON_STOP so the returned string is a complete JSON object.
    """
    client = _get_client()
    json_system = (
        f"Respond only with valid JSON. "
        f"After the closing brace write {_JSON_STOP} on its own line."
    )
    if system:
        json_system = f"{json_system}\n\n{system}"

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "```json"},  # prefill — forces JSON object start
    ]
    try:
        response = client.messages.create(
            model=_JSON_MODEL_ID,
            max_tokens=MAX_TOKENS,
            system=json_system,
            messages=messages,
            stop_sequences=[_JSON_STOP],
            temperature=1.0
        )
        text = response.content[0].text if response.content else ""
        return ("{" + text).strip()
    except anthropic.AuthenticationError:
        print("Invalid API key. Check ANTHROPIC_API_KEY.")
    except anthropic.RateLimitError as e:
        retry_after = int(e.response.headers.get("retry-after", "60"))
        print(f"Rate limited. Retry after {retry_after}s.")
    except anthropic.APIConnectionError:
        print("Network error. Check your internet connection.")
    except anthropic.APIStatusError as e:
        print(f"API error ({e.status_code}): {e.message}")
    return None


def stream_response(client, messages_history: list, system_context: str, temperature: float = 1.0) -> str:
    stream = client.messages.create(
        model=MODEL_ID,
        max_tokens=1000,
        system=system_context,
        temperature=temperature,
        messages=messages_history,
        stream=True
    )

    full_reply = ""
    for event in stream:
        if event.type == "content_block_delta":
            print(event.delta.text, end="", flush=True)
            full_reply += event.delta.text

    print()  # newline after stream ends
    messages_history.append({"role": "assistant", "content": full_reply})
    return full_reply


if __name__ == "__main__":
    # result = ask_json("Give me a person with name, age, and city. how are you")
    pass