LLM Eval Harness

A small tool for testing how an LLM answers a fixed set of questions. You can swap the prompt, re-run the same questions, and get scores from a simple judge. Useful when you want to see if a prompt change actually helped.

It runs in mock mode by default so you do not need API keys. You can also point it at a real model if you want.

What you can learn
- How to structure a basic eval loop with questions, model responses, and scoring.
- Why small prompt changes can shift scores on the same set of questions.
- How to keep the judge separate so you can swap scoring methods later.

Learning from mistakes
- Keyword matching is weak. A good answer can miss the exact words and still be correct.
- Running the judge on every change gets expensive fast if you use a real API for every question.

How to run
python eval_harness.py

That runs the mock model and mock judge on all questions and prints a summary. Results are also saved to results.json.

To use a different system prompt, edit the SYSTEM_PROMPT string at the top of eval_harness.py and run again.

Notes
The questions cover simple facts, reasoning, and a few edge cases. Scores are 1-5. In mock mode the judge looks for keywords and length. Replace the judge function if you want a real LLM-as-judge.

License
MIT
