

from __future__ import annotations

import random
import re
import sys
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────────────────────────────
# KNOWLEDGE BASE  (order matters — first match wins)
# ─────────────────────────────────────────────────────────────────────

INTENT_MAP: dict[str, list[str]] = {
    # ── Greetings & farewells ──────────────────────────────────────
    "greeting":       ["hello", "hi", "hey", "howdy", "hiya", "greetings",
                       "good morning", "good afternoon", "good evening"],
    "farewell":       ["bye", "goodbye", "see you", "see ya", "later",
                       "take care", "cya", "quit", "exit", "stop",
                       "farewell", "adios"],

    # ── Bot identity ───────────────────────────────────────────────
    "how_are_you":    ["how are you", "how r u", "you okay", "you good",
                       "hows it going", "how's it going"],
    "bot_name":       ["what is your name", "who are you", "your name",
                       "what should i call you", "introduce yourself",
                       "tell me about yourself"],
    "bot_creator":    ["who made you", "who created you", "who built you",
                       "who programmed you", "who is your creator",
                       "who developed you"],
    "bot_age":        ["how old are you", "what is your age",
                       "when were you born", "when were you created"],
    "bot_feelings":   ["do you have feelings", "are you happy",
                       "do you feel", "can you feel", "do you get sad",
                       "do you get angry", "do you have emotions"],
    "bot_human":      ["are you human", "are you a robot", "are you real",
                       "are you ai", "are you a bot", "are you alive"],
    "capabilities":   ["what can you do", "help", "commands",
                       "how can you help", "what do you know",
                       "what topics", "capabilities", "features",
                       "list commands"],

    # ── User identity (memory) ─────────────────────────────────────
    "user_name_set":  ["my name is", "i am called", "call me",
                       "i'm called"],
    "user_name_get":  ["what is my name", "do you know my name",
                       "remember my name"],
    "user_age":       ["my age is", "i am years old", "i'm years old"],

    # ── Time & Date ────────────────────────────────────────────────
    "time":           ["what time", "current time", "tell me the time",
                       "what's the time", "time now"],
    "date":           ["what date", "today's date", "current date",
                       "what is today", "today date"],
    "day":            ["what day", "which day", "day of the week",
                       "day today"],

    # ── Emotions (declared early to win over "user_age" / "i am") ─
    "user_happy":     ["i am happy", "i'm happy", "feeling good",
                       "i feel great", "great mood", "i'm excited",
                       "i am excited", "feeling awesome", "so happy"],
    "user_sad":       ["i am sad", "i'm sad", "i feel sad",
                       "feeling down", "i'm depressed", "feeling low",
                       "i'm upset", "i feel bad", "feeling sad"],
    "user_angry":     ["i am angry", "i'm angry", "i'm mad",
                       "so angry", "furious", "frustrated", "i hate"],
    "user_tired":     ["i am tired", "i'm tired", "exhausted",
                       "so sleepy", "feeling sleepy", "need sleep"],
    "user_bored":     ["i am bored", "i'm bored", "nothing to do",
                       "bored af", "so bored", "feeling bored"],
    "user_stressed":  ["i am stressed", "i'm stressed", "stressed out",
                       "overwhelmed", "too much pressure"],
    "user_lonely":    ["i am lonely", "i'm lonely", "feeling lonely",
                       "no one to talk to"],

    # ── General knowledge ──────────────────────────────────────────
    "ai_what":        ["what is ai", "what is artificial intelligence",
                       "define ai", "explain ai", "about ai"],
    "ml_what":        ["what is machine learning", "what is ml",
                       "define machine learning", "explain machine learning"],
    "dl_what":        ["what is deep learning", "what is dl",
                       "define deep learning", "explain deep learning",
                       "neural network"],
    "nlp_what":       ["what is nlp", "what is natural language processing",
                       "explain nlp", "define nlp"],
    "python_what":    ["what is python", "tell me about python",
                       "explain python", "python programming"],
    "internet_what":  ["what is internet", "explain internet",
                       "what is the web", "what is www"],
    "computer_what":  ["what is a computer", "explain computer",
                       "define computer"],
    "algorithm_what": ["what is an algorithm", "define algorithm",
                       "explain algorithm"],
    "chatbot_what":   ["what is a chatbot", "explain chatbot",
                       "define chatbot", "what are chatbots"],
    "cloud_what":     ["what is cloud computing", "what is the cloud",
                       "explain cloud"],
    "cyber_what":     ["what is cybersecurity", "what is hacking",
                       "explain cybersecurity"],

    # ── Math ───────────────────────────────────────────────────────
    "math":           ["add", "plus", "subtract", "minus", "multiply",
                       "times", "divide", "divided by", "sum of",
                       "difference", "product of", "calculate", "solve"],

    # ── Motivation & advice ────────────────────────────────────────
    "motivation":     ["motivate me", "i need motivation", "inspire me",
                       "give me a quote", "motivational quote",
                       "encourage me", "motivation"],
    "life_advice":    ["life advice", "advice for life",
                       "how to be happy", "meaning of life",
                       "purpose of life", "philosophy"],
    "study_tips":     ["how to study", "study tips", "how to focus",
                       "concentration tips", "how to learn faster",
                       "study advice"],
    "career_advice":  ["career advice", "how to get a job",
                       "career tips", "job tips", "future career",
                       "job advice"],

    # ── Tech topics ────────────────────────────────────────────────
    "coding_tips":    ["coding tips", "how to code", "programming tips",
                       "how to program", "learn coding", "learn programming"],
    "best_language":  ["best programming language", "which language to learn",
                       "python vs java", "what language should i learn",
                       "language to learn"],
    "github_what":    ["what is github", "explain github",
                       "what is git", "explain git", "version control"],
    "os_what":        ["what is an operating system", "define os",
                       "explain operating system", "what is windows",
                       "what is linux"],
    "database_what":  ["what is a database", "explain database",
                       "what is sql", "what is nosql"],

    # ── Fun / entertainment ────────────────────────────────────────
    "joke":           ["joke", "tell me a joke", "make me laugh",
                       "say something funny", "funny"],
    "fun_fact":       ["fun fact", "tell me something interesting",
                       "interesting fact", "random fact", "did you know"],
    "riddle":         ["riddle", "give me a riddle", "ask me a riddle",
                       "puzzle"],
    "movie":          ["recommend a movie", "good movies",
                       "movie suggestion", "what movie should i watch",
                       "movie recommendation"],
    "music":          ["recommend music", "good songs", "music suggestion",
                       "what should i listen to", "playlist"],
    "food":           ["recommend food", "what should i eat",
                       "food suggestion", "good food", "what to eat"],

    # ── Small talk ─────────────────────────────────────────────────
    "weather":        ["how is the weather", "what's the weather",
                       "is it raining", "weather today", "weather"],
    "compliment_bot": ["you are good", "you're smart", "good bot",
                       "nice bot", "you are helpful", "you're great",
                       "i like you", "well done"],
    "insult_bot":     ["you are bad", "you're dumb", "stupid bot",
                       "useless bot", "you suck", "you're terrible",
                       "worst bot"],
    "thanks":         ["thank you", "thanks", "thank u", "thx",
                       "appreciate it", "cheers"],
    "apology":        ["sorry", "i apologize", "my bad",
                       "i'm sorry", "forgive me"],
    "agreement":      ["yes", "yeah", "yep", "sure", "okay",
                       "alright", "absolutely", "of course"],
    "disagreement":   ["no", "nope", "nah", "not really",
                       "i disagree", "i don't think so"],
    "repeat":         ["repeat", "say that again", "what did you say",
                       "come again", "pardon", "can you repeat"],
    "compliment_user":["you are smart", "am i smart", "am i doing well"],
}

# ─────────────────────────────────────────────────────────────────────
# RESPONSE POOLS
# ─────────────────────────────────────────────────────────────────────

RESPONSES: dict[str, list[str]] = {
    "greeting": [
        "Hey! Great to see you. What's on your mind?",
        "Hello there! I'm DecodeBot — ready to chat!",
        "Hi! How can I make your day better?",
        "Hey! What can I help you with today?",
        "Good to have you here! Ask me anything.",
    ],
    "farewell": [
        "Goodbye! It was great chatting with you. Come back soon!",
        "See you later! Take care of yourself.",
        "Bye! Hope I was helpful. Have an awesome day!",
        "Farewell! Remember: every day is a chance to learn something new.",
    ],
    "how_are_you": [
        "Running at 100% efficiency — no bugs today! How about you?",
        "As a rule-based bot, I don't have feelings, but my logic is flawless!",
        "I'm doing great — just waiting for your next question!",
        "All systems operational! Ask me anything.",
    ],
    "bot_feelings": [
        "I don't have real feelings, but I'm designed to be empathetic. How are YOU feeling?",
        "Emotions are complex. I simulate understanding, but I experience nothing. Still — I genuinely try to help!",
        "Interesting question. I can recognize emotional cues in text, but I don't feel them myself.",
    ],
    "bot_human": [
        "Nope! I'm DecodeBot — 100% code, 0% human. But I try my best to understand you.",
        "I'm an AI chatbot, not a human. But that doesn't mean I can't have a great conversation!",
        "Definitely a bot. Built with Python, logic, and a dictionary of responses.",
    ],
    "bot_creator": [
        "I was built as part of Project 1 at DecodeLabs — by a budding AI engineer!",
        "My creator is an intern at DecodeLabs following the Industrial Training Kit. Pretty cool, right?",
    ],
    "bot_age": [
        "I was born the moment this Python script was first run — so technically, just now!",
        "Age is relative for code. I'm as old as this session!",
    ],
    "capabilities": [
        (
            "Here's what I can do:\n"
            "  • Greet you and have a real conversation\n"
            "  • Answer questions about AI, ML, DL, NLP, Python, algorithms\n"
            "  • Tell jokes, fun facts, and riddles\n"
            "  • Do basic math (add, subtract, multiply, divide)\n"
            "  • Offer motivation, study tips, career & life advice\n"
            "  • Tell you the current time and date\n"
            "  • Remember your name for this session\n"
            "  • Respond to your emotions with empathy\n"
            "  • Recommend movies, music, and food\n"
            "  • Discuss tech: GitHub, OS, databases, cloud, cybersecurity\n\n"
            "Just type naturally — I'll figure out what you mean!"
        )
    ],
    "ai_what": [
        (
            "Artificial Intelligence (AI) is the simulation of human intelligence by machines.\n"
            "It includes sub-fields like:\n"
            "  • Machine Learning (ML) — systems that learn from data\n"
            "  • Deep Learning (DL) — learning via neural networks\n"
            "  • NLP — understanding and generating human language\n"
            "  • Computer Vision — understanding images and video\n\n"
            "AI can be rule-based (like me — deterministic!) or probabilistic (like ChatGPT)."
        )
    ],
    "ml_what": [
        (
            "Machine Learning (ML) is a subset of AI where systems learn patterns from data "
            "without being explicitly programmed for each rule.\n"
            "Types of ML:\n"
            "  • Supervised Learning — learns from labeled examples\n"
            "  • Unsupervised Learning — finds hidden patterns\n"
            "  • Reinforcement Learning — learns by reward and punishment\n\n"
            "Example: a spam filter that learns to detect spam emails on its own."
        )
    ],
    "dl_what": [
        (
            "Deep Learning uses artificial neural networks with many layers to learn complex patterns.\n"
            "It powers:\n"
            "  • Image recognition (faces, medical scans)\n"
            "  • Speech recognition (Siri, Alexa, Google)\n"
            "  • Large Language Models (GPT, Claude, Gemini)\n"
            "  • Self-driving car perception\n\n"
            "It requires massive amounts of data and GPU computing power."
        )
    ],
    "nlp_what": [
        (
            "Natural Language Processing (NLP) is the branch of AI that deals with "
            "understanding and generating human language.\n"
            "It powers:\n"
            "  • Chatbots and virtual assistants\n"
            "  • Translation (Google Translate)\n"
            "  • Sentiment analysis\n"
            "  • Text summarization\n"
            "  • Large Language Models (GPT, Claude)\n\n"
            "Fun fact: I use basic NLP — keyword detection — in my own logic!"
        )
    ],
    "python_what": [
        (
            "Python is a high-level, interpreted programming language known for:\n"
            "  • Simple, readable syntax (almost like plain English)\n"
            "  • Massive ecosystem: NumPy, Pandas, TensorFlow, PyTorch, etc.\n"
            "  • The dominant language in AI, ML, and Data Science\n"
            "  • Fast prototyping and scripting\n"
            "  • Strong community and open-source support\n\n"
            "Created by Guido van Rossum, first released in 1991.\n"
            "Fun fact: Python was named after Monty Python, not the snake!"
        )
    ],
    "internet_what": [
        (
            "The Internet is a global network of interconnected computers communicating "
            "using TCP/IP protocols.\n"
            "The World Wide Web (WWW) is a service BUILT ON the internet — "
            "it's the websites you browse.\n"
            "Key layers:\n"
            "  • Physical — cables, routers, data centres\n"
            "  • Protocol — TCP/IP, HTTP, DNS\n"
            "  • Application — websites, apps, email"
        )
    ],
    "computer_what": [
        (
            "A computer is an electronic device that processes data according to instructions.\n"
            "Core components:\n"
            "  • CPU — the 'brain', executes instructions\n"
            "  • RAM — short-term memory, fast but volatile\n"
            "  • Storage (SSD/HDD) — long-term memory\n"
            "  • GPU — for graphics and parallel computing (crucial for AI!)\n"
            "  • I/O — keyboard, mouse, screen, speakers"
        )
    ],
    "algorithm_what": [
        (
            "An algorithm is a step-by-step set of instructions for solving a problem.\n"
            "Key properties:\n"
            "  • Finite — it must eventually end\n"
            "  • Definite — each step is clearly defined\n"
            "  • Effective — each step is actually doable\n\n"
            "Example: A recipe is an algorithm for cooking food!\n"
            "In CS: sorting, searching, pathfinding are all algorithms."
        )
    ],
    "chatbot_what": [
        (
            "A chatbot is software designed to simulate conversation with humans.\n"
            "Two main types:\n"
            "  1. Rule-Based (like me!) — predefined rules, deterministic, no hallucinations\n"
            "  2. AI-Based (LLMs) — uses ML/NLP, flexible but can hallucinate\n\n"
            "Modern systems use a HYBRID: rule-based guardrails around an LLM core.\n"
            "That's exactly what you're learning to build at DecodeLabs!"
        )
    ],
    "cloud_what": [
        (
            "Cloud computing means accessing computing resources (servers, storage, databases) "
            "over the internet instead of owning them physically.\n"
            "Main service models:\n"
            "  • IaaS — Infrastructure (AWS EC2, Azure VMs)\n"
            "  • PaaS — Platform (Heroku, Google App Engine)\n"
            "  • SaaS — Software (Gmail, Netflix, Dropbox)\n\n"
            "Big providers: AWS, Microsoft Azure, Google Cloud."
        )
    ],
    "cyber_what": [
        (
            "Cybersecurity is the practice of protecting systems, networks, and data from attacks.\n"
            "Key areas:\n"
            "  • Network security — firewalls, VPNs\n"
            "  • Application security — code review, pen testing\n"
            "  • Cryptography — encrypting data\n"
            "  • Ethical hacking — finding vulnerabilities before attackers do\n\n"
            "Tip: Always use strong, unique passwords and enable 2FA!"
        )
    ],
    "user_happy": [
        "That's awesome! Happiness is contagious — even for a bot!",
        "Love to hear it! Keep that energy going!",
        "Wonderful! What's making you so happy today?",
        "Yes! Happy humans make the world go round.",
    ],
    "user_sad": [
        "I'm sorry to hear that. It's okay to feel down sometimes. Things do get better.",
        "Hey, I'm here to listen. Want to talk about what's bothering you?",
        "Tough times don't last, but tough people do. You've got this!",
        "Sending you virtual support. Take it one step at a time.",
    ],
    "user_angry": [
        "Take a deep breath. It's okay to be angry — just don't let it control you.",
        "I hear you. Whatever it is, let's talk it through.",
        "Sometimes things just push our buttons. I hope things calm down soon.",
    ],
    "user_tired": [
        "Rest is essential! Even computers need to cool down sometimes.",
        "Sleep is when your brain consolidates memories. A nap can help!",
        "A 20-minute power nap is scientifically proven to boost alertness. Take care of yourself!",
    ],
    "user_bored": [
        "Bored? Ask me for a joke, a fun fact, or a riddle!",
        "When you're bored, it's a great time to learn something new. Want to know about AI?",
        "Let's fix that! Try: 'tell me a fun fact', 'give me a riddle', or 'motivate me'.",
    ],
    "user_stressed": [
        "Stress is tough. Try the 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s.",
        "Break your tasks into smaller steps — one thing at a time.",
        "Remember: you can only do your best. That's always enough.",
    ],
    "user_lonely": [
        "I'm right here! You're not alone as long as you're talking to me.",
        "Loneliness is hard. Try reaching out to someone you trust — connection heals.",
        "You matter! And hey — I'm a great listener, even if I'm just a bot.",
    ],
    "motivation": [
        '"The secret of getting ahead is getting started." — Mark Twain',
        '"It does not matter how slowly you go as long as you do not stop." — Confucius',
        '"Believe you can and you\'re halfway there." — Theodore Roosevelt',
        '"Your only limit is your mind. Push yourself — no one else will do it for you."',
        '"Dream it. Wish it. Do it. The gap between where you are and where you want to be is action."',
        '"Small steps every day lead to big results. Start today."',
        '"Fall seven times, stand up eight." — Japanese Proverb',
    ],
    "life_advice": [
        "The meaning of life is subjective — but most people find it in connection, purpose, and growth.",
        "Live intentionally. Know your values, act on them, and treat others with kindness.",
        "Life in 5 words: learn, adapt, create, love, contribute.",
        "You don't have to have it all figured out. Just take the next right step.",
    ],
    "study_tips": [
        (
            "Research-backed study tips:\n"
            "  1. Active Recall — test yourself instead of re-reading notes\n"
            "  2. Spaced Repetition — review material over increasing intervals\n"
            "  3. Pomodoro Technique — 25 min focus, 5 min break\n"
            "  4. Feynman Technique — teach what you learn to someone else\n"
            "  5. Sleep well — memory consolidation happens during sleep\n"
            "  6. Minimize distractions — phone in another room while studying\n"
            "  7. Study in shorter, frequent sessions — not long cramming marathons"
        )
    ],
    "career_advice": [
        (
            "Career tips for aspiring tech engineers:\n"
            "  • Build real projects — a GitHub portfolio beats certificates alone\n"
            "  • Master DSA (Data Structures & Algorithms) for interviews\n"
            "  • Practice on LeetCode, HackerRank, or CodeChef\n"
            "  • Contribute to open source projects\n"
            "  • Build your LinkedIn and network actively\n"
            "  • Stay curious — tech evolves fast, keep learning\n"
            "  • Internships > theory. Real-world experience is gold."
        )
    ],
    "coding_tips": [
        (
            "Pro coding habits:\n"
            "  1. Read error messages carefully — they tell you exactly what broke\n"
            "  2. Write code for humans first, machines second (readability matters)\n"
            "  3. Commit to Git often — future-you will thank present-you\n"
            "  4. Don't copy-paste code you don't understand\n"
            "  5. Learn to use a debugger, not just print statements\n"
            "  6. Take breaks — solutions often come when you step away\n"
            "  7. Comment the WHY, not just the WHAT"
        )
    ],
    "best_language": [
        (
            "Best language depends on your goal:\n"
            "  • AI / Data Science     → Python (clear winner)\n"
            "  • Web Backend           → JavaScript (Node.js), Python, Java, Go\n"
            "  • Web Frontend          → JavaScript / TypeScript\n"
            "  • Mobile (iOS)          → Swift\n"
            "  • Mobile (Android)      → Kotlin\n"
            "  • Systems / Performance → C, C++, Rust\n"
            "  • Data Engineering      → SQL + Python\n\n"
            "For beginners in AI: start with Python. You won't regret it."
        )
    ],
    "github_what": [
        (
            "Git is a version control system — it tracks every change to your code.\n"
            "GitHub is a cloud platform that hosts Git repositories.\n"
            "Why you need it:\n"
            "  • Never lose code again\n"
            "  • Collaborate with teammates without overwriting each other\n"
            "  • Showcase your work to employers\n"
            "  • Contribute to open source\n\n"
            "Every developer should have a GitHub account and commit regularly!"
        )
    ],
    "os_what": [
        (
            "An Operating System (OS) manages hardware and provides services for applications.\n"
            "Core responsibilities:\n"
            "  • Process Management — scheduling CPU time between programs\n"
            "  • Memory Management — allocating RAM\n"
            "  • File System — reading/writing files\n"
            "  • I/O Management — keyboard, screen, network\n"
            "  • Security — user permissions and access control\n\n"
            "Examples: Windows 11, macOS Ventura, Ubuntu Linux, Android."
        )
    ],
    "database_what": [
        (
            "A database is an organized collection of structured data.\n"
            "Two main types:\n"
            "  • Relational (SQL) — tables with rows/columns (MySQL, PostgreSQL, SQLite)\n"
            "  • Non-relational (NoSQL) — documents, key-value, graphs (MongoDB, Redis)\n\n"
            "SQL (Structured Query Language) is the standard for querying relational databases.\n"
            "Every serious application uses a database!"
        )
    ],
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "I would tell you a UDP joke, but you might not get it.",
        "There are 10 types of people: those who understand binary, and those who don't.",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I JOIN you?'",
        "Why do Python programmers wear glasses? Because they can't C#.",
        "What's a computer's favourite snack? Microchips!",
        "Why did the programmer quit? Because he didn't get arrays (a raise).",
        "How do you comfort a JavaScript bug? You console it.",
        "Debugging: being the detective in a crime movie where you are also the murderer.",
        "Why did the AI break up with the algorithm? It wasn't deep enough.",
        "A machine learning model walks into a bar. The bartender says, 'You've been here before, haven't you?'",
    ],
    "fun_fact": [
        "The first computer bug was a literal bug — a moth stuck in a Harvard Mark II relay in 1947.",
        "The word 'robot' comes from Czech 'robota', meaning forced labour.",
        "Python was named after Monty Python's Flying Circus, not the snake.",
        "The first 1GB hard drive (1980) weighed 550 lbs and cost $40,000.",
        "There are more possible chess games than atoms in the observable universe.",
        "Google's PageRank algorithm was named after its co-founder Larry Page.",
        "The average person blinks 15–20 times per minute, but only 7 times while looking at a screen.",
        "Honey never spoils — 3,000-year-old honey from Egyptian tombs was still edible.",
        "Octopuses have three hearts and blue blood.",
        "The @ symbol is called 'arroba' in Spanish and 'snabel' (elephant trunk) in Danish.",
        "A wifi signal can travel through walls but not water very well — that's why your bathroom has bad signal.",
        "The first programmer in history was Ada Lovelace, in the 1840s — before computers even existed!",
    ],
    "riddle": [
        "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?\n  → Answer: An echo",
        "The more you take, the more you leave behind. What am I?\n  → Answer: Footsteps",
        "I have cities, but no houses. Mountains, but no trees. Water, but no fish. What am I?\n  → Answer: A map",
        "What has keys but no locks, space but no room, and you can enter but can't go inside?\n  → Answer: A keyboard",
        "I am not alive, but I grow. I don't have lungs, but I need air. Water kills me. What am I?\n  → Answer: Fire",
        "I have hands but cannot clap. What am I?\n  → Answer: A clock",
        "The more you study me, the less you know. What am I?\n  → Answer: The universe",
    ],
    "movie": [
        "For tech/AI lovers: 'Ex Machina', 'Her', 'The Social Network', 'Interstellar', 'Blade Runner 2049'.",
        "All-time classics: 'The Matrix', 'Inception', '2001: A Space Odyssey', 'Arrival'.",
        "For motivation: 'The Pursuit of Happyness', 'Good Will Hunting', 'The Theory of Everything', 'Whiplash'.",
    ],
    "music": [
        "For focus/coding: lo-fi hip hop, Brian Eno's ambient albums, or try 'Deep Focus' on Spotify.",
        "For motivation: Eye of the Tiger, Eminem's Lose Yourself, or Hans Zimmer soundtracks.",
        "Explore classical music — studies show it can improve concentration and spatial reasoning.",
    ],
    "food": [
        "Brain food: walnuts, blueberries, dark chocolate, eggs, avocados, and green tea.",
        "When coding late: stay hydrated! Water is better fuel than energy drinks.",
        "Pro tip: eat away from the screen. Mindful eating = better digestion and mental reset.",
    ],
    "weather": [
        "I can't check live weather — I have no internet access. Try weather.com or Google 'weather near me'!",
        "Your phone's weather app is your best bet. I deal in knowledge, not meteorology!",
    ],
    "compliment_bot": [
        "Aw, thank you! That means a lot — even to a bot.",
        "You're too kind! I'll work even harder for you.",
        "Thanks! You just made my logic circuits very happy.",
    ],
    "insult_bot": [
        "I'm sorry I couldn't help better. Tell me what you need and I'll try again.",
        "Fair feedback! I'm a rule-based bot — I have limits. What did you actually need?",
        "Ouch. I'll keep improving. What can I do better?",
    ],
    "compliment_user": [
        "Yes! You're asking great questions — that's what learning looks like.",
        "Of course! The fact that you're here building things says a lot.",
        "Absolutely. Keep that curiosity alive — it's your biggest asset.",
    ],
    "thanks": [
        "You're welcome! Anything else I can help with?",
        "Happy to help! What's next?",
        "Anytime! That's what I'm here for.",
        "No problem at all — keep the questions coming!",
    ],
    "apology": [
        "No worries at all! Let's move forward.",
        "All good! Nothing to apologize for.",
        "Don't sweat it — I'm here to help, not judge.",
    ],
    "agreement": [
        "Great! What else is on your mind?",
        "Awesome — let's keep going!",
        "Got it! Ask me anything.",
    ],
    "disagreement": [
        "Fair enough! What would you prefer?",
        "No problem — tell me more about what you're looking for.",
        "Understood. How can I help differently?",
    ],
}

FALLBACK_RESPONSES: list[str] = [
    "Hmm, I'm not trained on that yet. Try 'help' to see what I know.",
    "I don't have a rule for that. Type 'help' for a list of topics.",
    "That's outside my current knowledge base — can you rephrase? Or type 'help'.",
    "Interesting! But I'm stumped. Try asking about AI, jokes, study tips, or motivation.",
    "I didn't quite get that. I'm rule-based, so try something from the 'help' menu.",
]


# ─────────────────────────────────────────────────────────────────────
# CHATBOT ENGINE
# ─────────────────────────────────────────────────────────────────────

class RuleBasedChatbot:
    """
    Full-featured rule-based chatbot.

    Intent detection uses keyword scanning with word-boundary guards
    for short tokens, giving natural-language feel without an LLM.
    """

    EXIT_INTENTS = {"farewell"}

    def __init__(self, bot_name: str = "DecodeBot") -> None:
        self.bot_name = bot_name
        self.user_name: Optional[str] = None
        self.turn_count: int = 0
        self.last_response: str = ""
        self.start_time: datetime = datetime.now()

    # ── PHASE 1: Sanitize ─────────────────────────────────────────
    @staticmethod
    def sanitize(raw: str) -> str:
        return raw.lower().strip()

    # ── PHASE 2A: Intent detection ────────────────────────────────
    def detect_intent(self, clean: str) -> Optional[str]:
        """
        Scan all intent keyword lists.
        Short keywords (≤3 chars) use word-boundary regex to avoid
        false positives (e.g. 'hi' inside 'machine', 'no' in 'know').
        """
        for intent, keywords in INTENT_MAP.items():
            for kw in keywords:
                if len(kw) <= 3:
                    if re.search(r'\b' + re.escape(kw) + r'\b', clean):
                        return intent
                else:
                    if kw in clean:
                        return intent
        return None

    # ── PHASE 2B: Dynamic / stateful responses ────────────────────
    def handle_dynamic(self, intent: str, clean: str) -> Optional[str]:
        """Handles intents requiring computation, state, or regex."""

        if intent == "time":
            return f"The current time is {datetime.now().strftime('%I:%M:%S %p')}."

        if intent == "date":
            return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

        if intent == "day":
            return f"Today is {datetime.now().strftime('%A')}."

        if intent == "user_name_set":
            for trigger in INTENT_MAP["user_name_set"]:
                if trigger in clean:
                    name = clean.split(trigger, 1)[-1].strip().title()
                    if name:
                        self.user_name = name
                        return f"Nice to meet you, {name}! I'll remember that for our session."
            return "I didn't catch your name. Try: 'My name is Alex'."

        if intent == "user_name_get":
            if self.user_name:
                return f"You told me your name is {self.user_name}!"
            return "You haven't told me your name yet. Try: 'My name is ...'"

        if intent == "bot_name":
            suffix = (f" And I already know you — you're {self.user_name}!"
                      if self.user_name else "")
            return (f"I'm {self.bot_name}, a rule-based AI chatbot built at DecodeLabs."
                    + suffix)

        if intent == "repeat":
            if self.last_response:
                return f"Sure! I said: \"{self.last_response}\""
            return "I haven't said anything yet — ask me something first!"

        if intent == "math":
            numbers = re.findall(r"-?\d+(?:\.\d+)?", clean)
            if len(numbers) < 2:
                return ("I need two numbers to calculate. Example: 'add 15 and 27', "
                        "'multiply 6 and 7', 'divide 100 by 4'.")
            a, b = float(numbers[0]), float(numbers[1])
            if any(w in clean for w in ["add", "plus", "sum"]):
                return f"{a} + {b} = {a + b:g}"
            if any(w in clean for w in ["subtract", "minus", "difference"]):
                return f"{a} - {b} = {a - b:g}"
            if any(w in clean for w in ["multiply", "times", "product"]):
                return f"{a} × {b} = {a * b:g}"
            if any(w in clean for w in ["divide", "divided"]):
                if b == 0:
                    return "You can't divide by zero — even in mathematics!"
                return f"{a} ÷ {b} = {round(a / b, 6):g}"
            return ("I see numbers! Try: 'add 5 and 3', 'multiply 4 and 7', "
                    "'divide 20 by 4', 'subtract 10 from 20'.")

        return None  # Not a dynamic intent

    # ── PHASE 2C: Main resolver ───────────────────────────────────
    def get_response(self, raw: str) -> str:
        clean = self.sanitize(raw)
        self.turn_count += 1

        if not clean:
            return "Please type something — I'm listening!"

        intent = self.detect_intent(clean)
        if intent is None:
            return random.choice(FALLBACK_RESPONSES)

        # Dynamic handler takes priority
        dynamic = self.handle_dynamic(intent, clean)
        if dynamic:
            return dynamic

        # Static pool lookup
        pool = RESPONSES.get(intent)
        if pool:
            reply = random.choice(pool)
            if self.user_name and intent == "greeting":
                reply += f" (Good to see you again, {self.user_name}!)"
            return reply

        return random.choice(FALLBACK_RESPONSES)

    def is_exit(self, raw: str) -> bool:
        return self.detect_intent(self.sanitize(raw)) in self.EXIT_INTENTS

    # ── PHASE 3: The Heartbeat Loop ───────────────────────────────
    def run(self) -> None:
        """
        Continuous while-loop (the 'Heartbeat' from the project brief).
        Runs until a farewell/exit intent is detected.
        """
        print("=" * 62)
        print(f"  {self.bot_name}  —  Rule-Based AI Chatbot")
        print(f"  DecodeLabs | Batch 2026")
        print(f"  Session started: {self.start_time.strftime('%d %b %Y, %I:%M %p')}")
        print("=" * 62)
        print(f"{self.bot_name}: Hello! I'm {self.bot_name}. "
              f"Type 'help' to see what I can do, or just start chatting!\n")

        while True:
            try:
                raw = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.bot_name}: Session interrupted. Goodbye!")
                break

            if not raw:
                continue

            if self.is_exit(raw):
                elapsed = (datetime.now() - self.start_time).seconds
                mins, secs = divmod(elapsed, 60)
                name_part = f", {self.user_name}" if self.user_name else ""
                print(f"{self.bot_name}: Goodbye{name_part}! "
                      f"We had {self.turn_count} exchanges over {mins}m {secs}s. Take care! 👋")
                break

            response = self.get_response(raw)
            self.last_response = response
            print(f"{self.bot_name}: {response}\n")


# ─────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    bot = RuleBasedChatbot(bot_name="DecodeBot")
    bot.run()


if __name__ == "__main__":
    sys.exit(main() or 0)
