"""
Project 1: Rule-Based AI Chatbot
DecodeLabs — Industrial Training Kit | Batch 2026

A deterministic, rule-based conversational agent built on dictionary
lookups (O(1) intent matching) rather than an if-elif ladder (O(n),
flagged as an anti-pattern in the project brief).

Architecture follows the IPO model from the brief:
    INPUT   -> Sanitization & Normalization
    PROCESS -> Intent Matching & State (the "Logic Skeleton")
    OUTPUT  -> Response Generation & Feedback Loop

Author: <your name>
"""

from __future__ import annotations

import random
import sys
from datetime import datetime
from typing import Optional


class RuleBasedChatbot:
    """
    A deterministic chatbot that maps sanitized user intents to
    predefined responses using a dictionary (hash map) knowledge base.

    Why a dictionary instead of if-elif?
    ------------------------------------
    An if-elif chain checks conditions sequentially -> O(n) lookup time
    that degrades as more rules are added. A dictionary resolves any
    key to its value in constant time -> O(1), regardless of how many
    intents the bot knows. This is the "Hash Map Pivot" from the brief.
    """

    EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "stop"}

    def __init__(self, bot_name: str = "DecodeBot") -> None:
        self.bot_name = bot_name
        self.user_name: Optional[str] = None
        self.turn_count: int = 0

        # ---- Knowledge Base (5+ intents, as required by spec) ----
        # Single-response intents
        self.knowledge_base: dict[str, str] = {
            "hello": "Hi there! How can I help you today?",
            "hi": "Hello! Great to see you.",
            "how are you": "I'm just a program, but I'm running smoothly! How about you?",
            "what is your name": f"I'm {self.bot_name}, your rule-based assistant.",
            "what can you do": (
                "I can greet you, tell you the time, answer simple "
                "questions, and chat using predefined rules."
            ),
            "help": (
                "Try: hello, how are you, what is your name, "
                "what can you do, time, joke, or exit."
            ),
            "thank you": "You're welcome!",
            "thanks": "Anytime!",
        }

        # Multi-response intents (adds a touch of personality/variety
        # per the brief's "experiment with unique solutions" suggestion)
        self.varied_responses: dict[str, list[str]] = {
            "joke": [
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "I would tell you a UDP joke, but you might not get it.",
                "There are 10 types of people: those who understand binary, and those who don't.",
            ],
        }

        self.fallback_responses: list[str] = [
            "I do not understand that yet. Try 'help' to see what I can do.",
            "Hmm, that's outside my rule set right now.",
            "I'm not trained on that one. Type 'help' for available commands.",
        ]

    # ------------------------------------------------------------------
    # PHASE 1: INPUT & SANITIZATION
    # ------------------------------------------------------------------
    @staticmethod
    def sanitize_input(raw_input: str) -> str:
        """
        Normalize raw user input so that 'HeLLo', 'hello', and '  hello  '
        all resolve to the same dictionary key.
        """
        return raw_input.lower().strip()

    # ------------------------------------------------------------------
    # PHASE 2: PROCESS (Intent Matching & State)
    # ------------------------------------------------------------------
    def _handle_dynamic_intents(self, clean_input: str) -> Optional[str]:
        """
        Handles intents that require logic beyond a static string
        lookup (state, computation, or randomness). Returns None if
        no dynamic intent matches, signalling the caller to fall
        through to the static knowledge base.
        """
        if clean_input in ("time", "what time is it"):
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

        if clean_input in ("date", "what is the date", "today's date"):
            return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."

        if clean_input.startswith("my name is"):
            name = clean_input.replace("my name is", "", 1).strip().title()
            if name:
                self.user_name = name
                return f"Nice to meet you, {name}! I'll remember that."
            return "I didn't catch a name there."

        if clean_input in ("what is my name", "do you know my name"):
            if self.user_name:
                return f"You told me your name is {self.user_name}."
            return "You haven't told me your name yet. Try: 'My name is ...'"

        if clean_input == "joke":
            return random.choice(self.varied_responses["joke"])

        return None

    def get_response(self, raw_input: str) -> str:
        """
        Core decision-making logic (the 'Logic Skeleton').
        Order of resolution:
            1. Dynamic / stateful intents
            2. Static knowledge base (O(1) dictionary lookup)
            3. Fallback response
        """
        clean_input = self.sanitize_input(raw_input)
        self.turn_count += 1

        if not clean_input:
            return "Please type something so I can respond."

        dynamic_reply = self._handle_dynamic_intents(clean_input)
        if dynamic_reply is not None:
            return dynamic_reply

        # The .get() method performs lookup + fallback as a single
        # atomic operation — no nested if-else required.
        return self.knowledge_base.get(
            clean_input, random.choice(self.fallback_responses)
        )

    # ------------------------------------------------------------------
    # PHASE 3: OUTPUT / CONTROL LOOP (The Heartbeat)
    # ------------------------------------------------------------------
    def is_exit_command(self, raw_input: str) -> bool:
        return self.sanitize_input(raw_input) in self.EXIT_COMMANDS

    def run(self) -> None:
        """
        The continuous interaction loop. The organism stays alive
        until the kill command ('exit', 'quit', 'bye', etc.) is
        received — see 'The Heartbeat: The Infinite Loop' in the brief.
        """
        print(f"{self.bot_name}: Hello! I'm online. Type 'help' anytime, or 'exit' to leave.")

        while True:
            try:
                raw_input_text = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.bot_name}: Session interrupted. Goodbye!")
                break

            if self.is_exit_command(raw_input_text):
                print(f"{self.bot_name}: Goodbye! We exchanged {self.turn_count} messages.")
                break

            reply = self.get_response(raw_input_text)
            print(f"{self.bot_name}: {reply}")


def main() -> None:
    bot = RuleBasedChatbot(bot_name="DecodeBot")
    bot.run()


if __name__ == "__main__":
    sys.exit(main() or 0)
