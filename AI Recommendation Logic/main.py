"""
main.py
========
DecodeLabs | Project 3 - AI Recommendation Logic
CLI front-end for the Tech Stack Recommender (the "Digital Matchmaker").

Usage:
    python main.py
        -> interactive mode, prompts you for skills

    python main.py --skills "Python,Cloud Computing,Automation"
        -> one-shot mode

    python main.py --list-skills
        -> shows every skill tag the engine recognizes
"""

import argparse
import os
import sys

from recommender import TechStackRecommender

DATASET_PATH = os.path.join(os.path.dirname(__file__), "raw_skills.csv")
DIVIDER = "-" * 56


def print_banner():
    print(DIVIDER)
    print("  DECODELABS  |  TECH STACK RECOMMENDER ENGINE")
    print("  Project 3: AI Recommendation Logic")
    print(DIVIDER)


def print_results(payload):
    if payload["cold_start"]:
        print("\n[!] COLD START DETECTED")
        print("    None of your skills matched our vocabulary, so we can't")
        print("    run the similarity math yet. Showing trending fallback")
        print("    roles instead (Slide 21: Bypassing the Cold Start).\n")
        for i, (role, _, _) in enumerate(payload["results"], start=1):
            print(f"    {i}. {role}  (trending fallback)")
        print()
        return

    if payload["unrecognized"]:
        print(f"\n[i] Skipped unrecognized tags: {', '.join(payload['unrecognized'])}")
        print("    Tip: run with --list-skills to see supported tags.\n")

    print("\nTOP MATCHES (ranked by Cosine Similarity / angular alignment):\n")
    for rank, (role, score, matched) in enumerate(payload["results"], start=1):
        bar_len = int(score / 5)  # 0-100 scaled to a 0-20 char bar
        bar = "#" * bar_len + "." * (20 - bar_len)
        print(f"  {rank}. {role:<24} [{bar}] {score:>5.1f}%")
        if matched:
            print(f"     matched on: {', '.join(matched)}")
    print()


def interactive_mode(engine: TechStackRecommender):
    print("\nEnter at least 3 skills, separated by commas.")
    print("Example: Python, Cloud Computing, Automation\n")
    raw = input("Your skills > ").strip()
    skills = [s.strip() for s in raw.split(",") if s.strip()]

    while len(skills) < 3:
        print(f"\n[!] You entered {len(skills)} skill(s). Minimum 3 required.")
        raw = input("Your skills > ").strip()
        skills = [s.strip() for s in raw.split(",") if s.strip()]

    payload = engine.recommend(skills, top_n=3)
    print_results(payload)


def main():
    parser = argparse.ArgumentParser(description="DecodeLabs Tech Stack Recommender")
    parser.add_argument("--skills", type=str, help="Comma-separated list of skills, e.g. 'Python,SQL,Docker'")
    parser.add_argument("--top", type=int, default=3, help="Number of recommendations to return (default 3)")
    parser.add_argument("--list-skills", action="store_true", help="List every skill tag the engine recognizes")
    args = parser.parse_args()

    print_banner()
    engine = TechStackRecommender(DATASET_PATH)

    if args.list_skills:
        print("\nRecognized skill vocabulary:\n")
        vocab = engine.list_known_skills()
        for i in range(0, len(vocab), 5):
            print("  " + ", ".join(v.title() for v in vocab[i:i + 5]))
        print()
        return

    if args.skills:
        skills = [s.strip() for s in args.skills.split(",") if s.strip()]
        try:
            payload = engine.recommend(skills, top_n=args.top)
        except ValueError as e:
            print(f"\n[!] {e}")
            sys.exit(1)
        print_results(payload)
    else:
        interactive_mode(engine)


if __name__ == "__main__":
    main()
