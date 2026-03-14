# FEATURE: High Score tracker — added via Agent Mode for Challenge 2.
# Saves and loads per-difficulty high scores to high_scores.json.
# Claude Agent Mode suggested using json for simplicity over a database,
# and using a try/except so the app doesn't crash if the file doesn't exist yet.

import json
import os

SCORES_FILE = os.path.join(os.path.dirname(__file__), "high_scores.json")


def load_high_scores() -> dict:
    """Load high scores from file. Returns empty dict if file doesn't exist."""
    try:
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_high_score(difficulty: str, score: int) -> bool:
    """
    Save score if it beats the current high score for this difficulty.
    Returns True if a new high score was set.
    """
    scores = load_high_scores()
    current_best = scores.get(difficulty, None)

    if current_best is None or score > current_best:
        scores[difficulty] = score
        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f)
        return True
    return False
