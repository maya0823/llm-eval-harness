#!/usr/bin/env python3
"""Simple LLM evaluation harness.

Runs a set of questions against a model (mock by default) and scores
the answers with a judge. Edit SYSTEM_PROMPT and re-run to see the effect.
"""

import json
import random
from pathlib import Path

# Change this and re-run to test prompt variations.
SYSTEM_PROMPT = """You are a helpful assistant. Answer questions clearly and accurately.
Keep answers short unless the question asks for detail."""

QUESTIONS_FILE = Path("questions.json")
RESULTS_FILE = Path("results.json")


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def mock_model(question: str, system_prompt: str) -> str:
    """Fake model responses for offline testing."""
    # Simple canned answers that sometimes match keywords.
    canned = {
        "What is the capital of France?": "The capital of France is Paris.",
        "What is 15 times 7?": "15 times 7 is 105.",
        "Who wrote Romeo and Juliet?": "William Shakespeare wrote Romeo and Juliet.",
        "What is the largest planet in our solar system?": "Jupiter is the largest planet.",
        "What is the boiling point of water in Celsius?": "Water boils at 100 degrees Celsius.",
        "How many days are in a leap year?": "A leap year has 366 days.",
        "Name three primary colors.": "The primary colors are red, blue, and yellow.",
        "What does HTTP stand for?": "HTTP stands for Hypertext Transfer Protocol.",
        "What is the square root of 144?": "The square root of 144 is 12.",
        "What is 2 to the power of 10?": "2 to the power of 10 is 1024.",
        "What is the capital of Japan?": "The capital of Japan is Tokyo.",
        "What is the chemical formula for water?": "The chemical formula for water is H2O.",
        "What is 100 divided by 4?": "100 divided by 4 is 25.",
        "What is 9 times 9?": "9 times 9 is 81.",
        "Name the planet closest to the sun.": "Mercury is the planet closest to the sun.",
        "What does CPU stand for?": "CPU stands for Central Processing Unit.",
        "How many hours are in a day?": "There are 24 hours in a day.",
        "How many minutes are in an hour?": "There are 60 minutes in an hour.",
        "What is the opposite of hot?": "The opposite of hot is cold.",
        "Name the largest ocean.": "The Pacific Ocean is the largest.",
        "What is the capital of Canada?": "The capital of Canada is Ottawa.",
        "How many legs does a spider have?": "A spider has 8 legs.",
        "How many sides does a hexagon have?": "A hexagon has 6 sides.",
        "How many continents are there?": "There are 7 continents.",
        "Which element has the chemical symbol O?": "Oxygen has the chemical symbol O.",
        "What gas do plants absorb from the air?": "Plants absorb carbon dioxide from the air.",
        "What is the freezing point of water in Fahrenheit?": "Water freezes at 32 degrees Fahrenheit.",
        "Name a programming language that starts with P.": "Python is a programming language that starts with P.",
        "Name the three states of matter.": "The three states of matter are solid, liquid, and gas.",
        "Name the four seasons.": "The four seasons are spring, summer, autumn, and winter.",
        "Convert 32 degrees Fahrenheit to Celsius.": "32 degrees Fahrenheit is 0 degrees Celsius.",
    }
    if question in canned:
        return canned[question]
    # Fallback: generic response that may or may not hit keywords.
    return f"Based on the prompt '{system_prompt[:40]}...', the answer involves relevant facts about the topic."


def mock_judge(question: str, answer: str, keywords: list) -> dict:
    """Simple keyword-based judge for offline use.

    In a real setup you would call an LLM here with a scoring prompt.
    """
    answer_lower = answer.lower()
    hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
    # Score 1-5 based on keyword hits and answer length.
    if hits == 0:
        score = 1
    elif hits == 1:
        score = 3
    else:
        score = 5
    # Slight penalty for very short answers.
    if len(answer) < 20:
        score = max(1, score - 1)
    reason = f"Matched {hits}/{len(keywords)} keywords."
    return {"score": score, "reason": reason}


def run_eval():
    questions = load_questions()
    results = []
    total_score = 0

    print(f"Running {len(questions)} questions with system prompt:")
    print(SYSTEM_PROMPT)
    print("-" * 60)

    for q in questions:
        answer = mock_model(q["question"], SYSTEM_PROMPT)
        judgment = mock_judge(q["question"], answer, q.get("keywords", []))
        results.append({
            "id": q["id"],
            "question": q["question"],
            "category": q.get("category", ""),
            "answer": answer,
            "score": judgment["score"],
            "reason": judgment["reason"],
        })
        total_score += judgment["score"]
        print(f"[{q['id']}] Score {judgment['score']}/5 - {q['question'][:50]}...")

    avg = total_score / len(questions)
    summary = {
        "total_questions": len(questions),
        "average_score": round(avg, 2),
        "system_prompt": SYSTEM_PROMPT,
        "results": results,
    }

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("-" * 60)
    print(f"Average score: {avg:.2f}/5")
    print(f"Full results written to {RESULTS_FILE}")


if __name__ == "__main__":
    run_eval()
