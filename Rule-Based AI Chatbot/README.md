# DecodeBot — Rule-Based AI Chatbot

**Project 1 | Industrial Training Kit | DecodeLabs | Batch 2026**

> *"An LLM without rules is a hallucination engine. Today, we build the skeleton that holds the intelligence."*

---

## What Is This?

DecodeBot is a fully-featured, deterministic chatbot built entirely in Python — no libraries, no APIs, no machine learning. It responds to natural language using keyword-based intent detection and a dictionary-backed knowledge base.

This is Project 1 of the DecodeLabs AI Engineering track: before you build systems that *learn*, you build one that *decides*. Master the logic engine first.

---

## Features at a Glance

| Category | What It Does |
|---|---|
| **Greetings & Small Talk** | Natural conversation, compliments, apologies |
| **AI Knowledge Base** | Explains AI, ML, Deep Learning, NLP, Python, algorithms |
| **Tech Topics** | Git/GitHub, OS, databases, cloud computing, cybersecurity |
| **Emotions & Empathy** | Recognizes 7 emotional states and responds with care |
| **Math Engine** | Add, subtract, multiply, divide — with divide-by-zero guard |
| **Advice Engine** | Study tips, career advice, life philosophy, coding habits |
| **Entertainment** | 12 jokes, 12 fun facts, 7 riddles — randomized every time |
| **Recommendations** | Movies, music, food |
| **Memory** | Remembers your name for the full session |
| **Time & Date** | Live system time, date, and day of week |
| **Session Stats** | Total exchanges and duration shown on exit |

---

## Why a Dictionary Instead of If-Elif?

This is the core architectural lesson of Project 1.

```python
# ❌ Anti-pattern: if-elif ladder — O(n) time, high technical debt
if user_input == "hello":
    reply = "Hi!"
elif user_input == "bye":
    reply = "Goodbye!"
elif user_input == "help":
    reply = "..."
# ... grows unstable as rules multiply

# ✅ Professional approach: dictionary lookup — O(1) constant time
responses = {
    "hello": "Hi!",
    "bye":   "Goodbye!",
    "help":  "..."
}
reply = responses.get(user_input, "I do not understand.")
```

The `.get()` method performs lookup **and** fallback in a single atomic operation. No restructuring needed when you add new intents — just add a key.

---

## Architecture (IPO Model)

```
┌─────────────────────────────────────────────────────────────────┐
│                        IPO MODEL                                │
│                                                                 │
│   INPUT             PROCESS              OUTPUT                 │
│   ─────             ───────              ──────                 │
│                                                                 │
│  Raw text    ──►   Sanitize()    ──►   detect_intent()         │
│  from user          lower/strip         keyword scan            │
│                          │                    │                 │
│                          ▼                    ▼                 │
│                    Word-boundary      Dynamic handler?          │
│                    regex guard        (time/math/name)          │
│                                            │                    │
│                                            ▼                    │
│                                    Static pool lookup           │
│                                    random.choice(pool)          │
│                                            │                    │
│                                            ▼                    │
│                                      Fallback if                │
│                                      no match found             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Requirements

- **Python 3.9+**
- No external dependencies — standard library only (`re`, `random`, `datetime`, `sys`)

---

## How to Run

```bash
python3 chatbot.py
```

Sample session:

```
══════════════════════════════════════════════════════════════
  DecodeBot  —  Rule-Based AI Chatbot
  DecodeLabs | Batch 2026
  Session started: 23 Jun 2026, 10:30 AM
══════════════════════════════════════════════════════════════
DecodeBot: Hello! I'm DecodeBot. Type 'help' to see what I can do!

You: my name is Aryan
DecodeBot: Nice to meet you, Aryan! I'll remember that for our session.

You: what is machine learning
DecodeBot: Machine Learning (ML) is a subset of AI where systems learn
patterns from data without being explicitly programmed...

You: add 47 and 83
DecodeBot: 47.0 + 83.0 = 130

You: i am stressed
DecodeBot: Break your tasks into smaller steps — one thing at a time.

You: tell me a joke
DecodeBot: A SQL query walks into a bar, walks up to two tables and asks...
'Can I JOIN you?'

You: bye
DecodeBot: Goodbye, Aryan! We had 6 exchanges over 1m 42s. Take care! 👋
```

---

## Supported Inputs

Just type naturally. DecodeBot scans for keywords, not exact phrases.

| Try Saying | Intent |
|---|---|
| `hello` / `hi` / `hey` / `good morning` | Greeting |
| `how are you` / `you good?` | Bot status |
| `my name is [name]` | Set your name |
| `what is my name` | Recall your name |
| `what time is it` / `time now` | Current time |
| `what day is it` / `today's date` | Date & day |
| `what is AI` / `explain ML` / `what is NLP` | Knowledge base |
| `what is python` / `what is github` | Tech topics |
| `add 25 and 37` / `multiply 6 and 7` | Math engine |
| `i am sad` / `i am bored` / `i am stressed` | Empathy mode |
| `motivate me` / `give me a quote` | Motivation |
| `study tips` / `career advice` | Advice engine |
| `tell me a joke` / `fun fact` / `riddle` | Entertainment |
| `recommend a movie` / `music` / `food` | Recommendations |
| `help` | Full command list |
| `bye` / `exit` / `quit` / `goodbye` | End session |

---

## Project Structure

```
chatbot/
├── chatbot.py    ← Main application (single-file, no dependencies)
└── README.md     ← This file
```

Inside `chatbot.py`:

```
INTENT_MAP        — maps intent names to keyword trigger lists (40+ intents)
RESPONSES         — maps intent names to response pools (randomized)
FALLBACK_RESPONSES— shown when no intent is detected
RuleBasedChatbot  — main class
  ├── sanitize()        Phase 1: normalize input
  ├── detect_intent()   Phase 2A: keyword scan with word-boundary guard
  ├── handle_dynamic()  Phase 2B: computed responses (time, math, memory)
  ├── get_response()    Phase 2C: orchestrates the full resolution chain
  ├── is_exit()         checks if input triggers a farewell intent
  └── run()             Phase 3: the continuous heartbeat loop
```

---

## How Intent Detection Works

```python
def detect_intent(self, clean: str) -> Optional[str]:
    for intent, keywords in INTENT_MAP.items():
        for kw in keywords:
            if len(kw) <= 3:
                # Short tokens use word-boundary regex
                # e.g. "hi" must not match inside "machine"
                if re.search(r'\b' + re.escape(kw) + r'\b', clean):
                    return intent
            else:
                if kw in clean:
                    return intent
    return None
```

Emotion intents (`i am sad`, `i am bored`) are declared **before** the generic `user_age` pattern in the map, so they win on first match — no edge-case bugs.

---

## Extending This Project

| Difficulty | Idea |
|---|---|
| ⭐ Easy | Add more intents/responses to `INTENT_MAP` and `RESPONSES` |
| ⭐⭐ Medium | Add synonym grouping so `"what's the time"` and `"time please"` both work |
| ⭐⭐ Medium | Log every conversation to a `.txt` file with timestamps |
| ⭐⭐⭐ Hard | Add persistent memory (save name to a JSON file across sessions) |
| ⭐⭐⭐ Hard | Add a confidence score system instead of first-match |
| ⭐⭐⭐⭐ Expert | Hybrid mode — if no rule matches, call an LLM API as fallback |

The expert extension is exactly what Project 2 at DecodeLabs is about.

---

## Key Concepts Demonstrated

- **Control Flow** — while loop, break, conditional branching
- **Data Structures** — dictionaries (hash maps), lists, sets
- **String Processing** — `.lower()`, `.strip()`, `.split()`, `re.search()`
- **OOP** — class with encapsulated state and methods
- **Algorithmic Thinking** — O(1) dict lookup vs O(n) if-elif
- **IPO Model** — Input → Process → Output architecture
- **Defensive Programming** — divide-by-zero guard, EOFError handling, empty input check

---

## Author

`<your name>`
Industrial Training Kit — DecodeLabs, Batch 2026

---

## Contact

| | |
|---|---|
| 📞 | +91 89330 06408 |
| ✉️ | decodelabs.tech@gmail.com |
| 🌐 | www.decodelabs.tech |
| 📍 | Greater Lucknow, India |
