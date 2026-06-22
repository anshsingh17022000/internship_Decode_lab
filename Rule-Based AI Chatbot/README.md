# Rule-Based AI Chatbot

**Project 1 — Industrial Training Kit | DecodeLabs | Batch 2026**

A deterministic, rule-based conversational agent built with Python. This is the foundation project for the AI Engineering track: before building systems that *learn*, you build one that *decides* — using explicit control flow and a hash-map knowledge base instead of a brittle if-elif ladder.

---

## Features

- **Continuous interaction loop** — runs until an exit command is given
- **Input sanitization** — case-insensitive, whitespace-trimmed matching
- **Dictionary-based knowledge base** — O(1) intent lookup, 8+ static intents
- **Dynamic intents** — current time, current date, remembers your name for the session
- **Fallback handling** — graceful, varied responses for unrecognized input
- **Clean exit strategy** — multiple exit synonyms (`exit`, `quit`, `bye`, `stop`)

## Why a dictionary instead of if-elif?

| Approach | Lookup Time | Maintainability |
|---|---|---|
| `if/elif` ladder | O(n) — checks each condition in sequence | Gets fragile fast; easy to introduce cascading bugs |
| `dict.get()` | O(1) — constant time regardless of size | Add a new intent in one line, no restructuring |

```python
# Anti-pattern (avoid)
if user_input == "hello":
    reply = "Hi there!"
elif user_input == "bye":
    reply = "Goodbye!"
# ...grows unstable as rules increase

# Preferred approach
responses = {"hello": "Hi there!", "bye": "Goodbye!"}
reply = responses.get(user_input, "I do not understand.")
```

## Requirements

- Python 3.9+ (no external dependencies — standard library only)

## How to Run

```bash
python3 chatbot.py
```

You'll see:

```
DecodeBot: Hello! I'm online. Type 'help' anytime, or 'exit' to leave.
You: hello
DecodeBot: Hi there! How can I help you today?
You: exit
DecodeBot: Goodbye! We exchanged 1 messages.
```

## Supported Commands

| Input | Response Type |
|---|---|
| `hello`, `hi` | Greeting |
| `how are you` | Status check |
| `what is your name` | Identity |
| `what can you do` | Capabilities |
| `help` | List of commands |
| `time` | Current system time |
| `date` | Current system date |
| `my name is <name>` | Stores your name for the session |
| `what is my name` | Recalls stored name |
| `joke` | Random joke (varied responses) |
| `thank you` / `thanks` | Acknowledgement |
| `exit` / `quit` / `bye` / `stop` | Ends the session |
| *(anything else)* | Random fallback response |

## Project Structure

```
chatbot/
├── chatbot.py    # Main application (single-file, self-contained)
└── README.md     # This file
```

## Architecture (IPO Model)

```
INPUT                  PROCESS                    OUTPUT
─────                  ───────                     ──────
Raw user text   ──►   Sanitize (lower/strip)  ──►  Match dynamic intent?
                       │                             │
                       ▼                             ▼
                       Dictionary lookup        ──►  Found? return value
                       │                             │
                       ▼                             ▼
                       No match                 ──►  Random fallback
```

## Extending This Project

Ideas for going further, in increasing order of difficulty:

1. **More intents** — add new key-value pairs to `knowledge_base`
2. **Synonym handling** — map multiple phrasings (`"hey"`, `"yo"`) to the same intent
3. **Persistent memory** — save `user_name` to a file so it survives restarts
4. **Logging** — write each conversation turn to a `.log` file with timestamps
5. **Hybrid architecture** — if no rule matches, pass the query to an LLM API instead of a generic fallback (this is the bridge to Project 2)

## Author

`<your name>`
Industrial Training Kit — DecodeLabs, Batch 2026

## Contact

📞 +91 89330 06408
✉️ decodelabs.tech@gmail.com
🌐 www.decodelabs.tech
