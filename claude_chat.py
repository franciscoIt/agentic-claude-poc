import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "claude-sonnet-4-6"
MAX_TOKENS = 4096

messages_history:list= []

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    """Return the shared Anthropic client, creating it on first call.

    Reads ANTHROPIC_API_KEY from the environment (loaded via python-dotenv).
    The client is created once and reused for all subsequent calls to avoid
    the overhead of re-initialising the HTTP connection pool.

    Returns:
        anthropic.Anthropic: The singleton client instance.
    """
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def send_msg(msg: str = "Hi", system: str | None = None, temperature: float | None = None) -> anthropic.types.Message | None:
    """Send a user message to Claude and append both turns to the shared history.

    Maintains a module-level ``messages_history`` list so each call builds on
    the previous conversation.  The assistant reply is stored as plain text
    (``response.content[0].text``) rather than as the full content-block list,
    which keeps the serialised history compact and compatible with the Messages
    API's expected format.

    Args:
        msg (str): The user message to send. Defaults to ``"Hi"``.
        system (str | None): Optional system prompt that sets Claude's role,
            persona, or behavioural constraints for the entire conversation.
            Passed directly to the ``system`` parameter of the Messages API.
            If ``None``, no system prompt is sent.
        temperature (float | None): Sampling temperature in the range ``[0, 1]``
            (extended to ``2`` for some models via the API).  Lower values make
            responses more deterministic; higher values increase variety.
            If ``None``, the model's default temperature is used.

    Returns:
        anthropic.types.Message | None: The raw API response object on success,
        or ``None`` if any handled exception was raised.

    Raises (handled internally):
        anthropic.AuthenticationError: Invalid or missing ``ANTHROPIC_API_KEY``.
        anthropic.RateLimitError: Request quota exceeded; prints retry delay.
        anthropic.APIConnectionError: Network-level failure.
        anthropic.APIStatusError: Any other non-2xx HTTP response from the API.
    """
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
    """Run an interactive, multi-turn CLI chat session with Claude.

    Reads user input from stdin in a loop, forwards each message to
    ``send_msg``, and prints Claude's reply.  The shared ``messages_history``
    list accumulates every turn so the model has full conversation context.

    The session ends when the user types ``exit`` or ``quit`` (case-insensitive),
    sends EOF (Ctrl-D / Ctrl-Z), or interrupts with Ctrl-C.

    Args:
        system (str | None): System prompt forwarded verbatim to every
            ``send_msg`` call.  Use this to give Claude a persistent role or
            set of instructions for the whole session (e.g. ``"You are a
            helpful Python tutor."``).  If ``None``, no system prompt is used.
        temperature (float | None): Sampling temperature forwarded to every
            ``send_msg`` call.  Controls response randomness on a scale of
            roughly ``0`` (deterministic) to ``1`` (creative).  Pass ``None``
            to use the model default.

    Returns:
        None
    """
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




_PREFILL_MODEL = "claude-haiku-4-5-20251001"


def ask_structured_response(prompt: str, start_sequence_var: str, stop_sequences_var: list = [], system: str | None = None) -> str | None:
    """Ask Claude for a structured response using message prefilling and stop sequences.

    Forces the model to produce output in a specific format by:
    1. **Prefilling** the assistant turn with ``start_sequence_var`` so the model
       continues from that exact token (e.g. ``"{"`` guarantees a JSON object).
    2. **Stop sequences** that halt generation as soon as one of the tokens in
       ``stop_sequences_var`` is produced, preventing the model from adding
       prose after the structured block.

    The returned string is the complete structured fragment, reconstructed by
    prepending ``start_sequence_var`` to the model's continuation (the API
    strips the prefilled prefix from the response body).

    Model compatibility:
        This function intentionally uses ``_PREFILL_MODEL`` (``claude-haiku-4-5-20251001``)
        rather than the module-level ``MODEL_ID``.  As of 2026, message prefilling
        is **not supported** on Claude Opus 4.6/4.7 and Claude Sonnet 4.6 — the
        API returns a 400 error when an assistant-turn prefill is submitted to
        those models.  Haiku 4.5 is the latest model in the current lineup that
        still accepts assistant-turn prefilling.  If you upgrade this module's
        ``MODEL_ID`` to a newer release, do **not** change ``_PREFILL_MODEL``
        without verifying that the new model supports prefilling.

    Temperature note:
        Temperature is fixed at ``1.0``.  Extended thinking and certain structured-
        output workflows on Anthropic models require a temperature of exactly
        ``1.0``; passing a lower value can cause API errors on some model versions.

    Args:
        prompt (str): The user question or instruction.  Should describe what
            structured data you want (e.g. ``"Give me a person with name, age,
            and city."``).
        start_sequence_var (str): The opening token(s) used for both prefilling
            and reconstructing the final string.  Common values:
            - ``"{"``  — forces a bare JSON object
            - ``"```json"`` — forces a fenced JSON code block
            - ``"```español"`` — forces a fenced block labelled with a language tag
        stop_sequences_var (list[str]): List of tokens at which generation halts.
            The matching token itself is **not** included in the response.
            For fenced blocks, use ``["```"]``; for bare JSON, ``["}"]`` or
            ``["\\n\\n"]`` are common choices.  Defaults to ``[]`` (no stop
            sequences — generation continues to ``max_tokens``).
        system (str | None): Optional extra system-prompt text appended after
            the built-in format instruction.  Use to add domain context or
            additional constraints without overriding the format directive.
            If ``None``, only the auto-generated format instruction is used.

    Returns:
        str | None: The complete structured string (``start_sequence_var`` +
        model continuation) on success, or ``None`` if an error occurred.

    Raises (handled internally):
        anthropic.AuthenticationError: Invalid or missing ``ANTHROPIC_API_KEY``.
        anthropic.RateLimitError: Request quota exceeded; prints retry delay.
        anthropic.APIConnectionError: Network-level failure.
        anthropic.APIStatusError: Any other non-2xx HTTP response from the API.
    """
    client = _get_client()
    json_system = (
        f"Respond only with valid {start_sequence_var} format. "
        f"After the closing brace write {stop_sequences_var} on its own line."
    )
    if system:
        json_system = f"{json_system}\n\n{system}"

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": start_sequence_var}, # prefill — forces JSON object start
    ]
    try:
        response = client.messages.create(
            model=_PREFILL_MODEL,
            max_tokens=MAX_TOKENS,
            system=json_system,
            messages=messages,
            stop_sequences=stop_sequences_var,
            temperature=1.0
        )
        text = response.content[0].text if response.content else ""
        return (text)
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


def stream_response(client: anthropic.Anthropic, messages_history: list, system_context: str, temperature: float = 1.0) -> str:
    """Stream a Claude response token-by-token and print each chunk as it arrives.

    Uses the Messages API's server-sent-events stream so output appears
    progressively in the terminal rather than waiting for the full response.
    Only ``content_block_delta`` events (carrying text deltas) are processed;
    other event types (``message_start``, ``message_stop``, etc.) are ignored.

    The completed assistant reply is appended to ``messages_history`` so the
    caller's conversation state stays in sync.

    Note: ``max_tokens`` is hard-coded to ``1000`` inside this function.  If
    you need longer replies, adjust that value directly.

    Args:
        client (anthropic.Anthropic): An initialised Anthropic client.  Pass
            the result of ``_get_client()`` or any client configured with the
            desired API key / base URL.
        messages_history (list): The running conversation as a list of
            ``{"role": ..., "content": ...}`` dicts.  The new assistant turn
            is appended in-place, mutating the list the caller provided.
        system_context (str): System prompt that establishes Claude's role or
            constraints for this request.  Unlike ``send_msg``, this parameter
            is required — pass an empty string ``""`` if no system prompt is
            needed.
        temperature (float): Sampling temperature in the range ``[0, 1]``
            (approximately).  Lower values produce more focused, deterministic
            output; higher values increase creativity and variety.
            Defaults to ``1.0``.

    Returns:
        str: The full assistant reply assembled from all streamed deltas.
    """
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
    start_sequence_var="```csv"
    result = ask_structured_response("canciones mas populares en el año 1969",start_sequence_var, stop_sequences_var=["```"])
    print(result)