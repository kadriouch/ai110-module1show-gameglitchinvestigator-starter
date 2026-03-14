# FIX: Refactored all game logic from app.py into this module using Claude Agent mode.
# Claude identified the function boundaries and suggested the refactor structure.
# Verified by running pytest and confirming all 8 tests pass.

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard range was 1-50 and Normal was 1-100, making Hard easier than Normal.
    # Claude confirmed the ranges were illogical. Fixed by reassigning:
    # Easy=1-20, Normal=1-50, Hard=1-100. Verified in sidebar after each difficulty switch.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Original hints were inverted — guess > secret said "Go HIGHER!" (wrong).
    # Claude confirmed the comparison was flipped. Fixed by swapping the messages.
    # Verified manually: used Developer Debug panel to confirm secret=24,
    # guessed 25 (too high) and confirmed hint now correctly says "Go LOWER!".
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Original code gave +5 points on even attempts for "Too High" (wrong guess rewarded).
    # Claude identified the even/odd check as the bug. Removed it so all wrong guesses deduct 5.
    # Verified with pytest: test_score_deducts_for_too_high_on_even_attempt confirms -5 on attempt 2.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
