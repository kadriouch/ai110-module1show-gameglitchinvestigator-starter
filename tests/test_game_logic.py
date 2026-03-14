from logic_utils import check_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# Tests targeting the inverted-hints bug:
# The original code returned "Go HIGHER!" when guess > secret (wrong).
# After the fix, guess > secret must say "Go LOWER!" and vice versa.

def test_hint_says_go_lower_when_guess_is_too_high():
    # Guess 60, secret 50 — guess is too high, so hint must say go lower
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message}"


def test_hint_says_go_higher_when_guess_is_too_low():
    # Guess 40, secret 50 — guess is too low, so hint must say go higher
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message}"


# Tests targeting the score bug:
# The original code gave +5 points on even attempts for "Too High" (wrong guess rewarded).
# After the fix, every wrong guess should always deduct 5 points.

def test_score_deducts_for_too_high_on_even_attempt():
    # Even attempt number — original bug gave +5 here instead of -5
    score = update_score(100, "Too High", attempt_number=2)
    assert score == 95, f"Expected 95 but got {score}"


def test_score_deducts_for_too_high_on_odd_attempt():
    score = update_score(100, "Too High", attempt_number=3)
    assert score == 95, f"Expected 95 but got {score}"


def test_score_deducts_for_too_low():
    score = update_score(100, "Too Low", attempt_number=1)
    assert score == 95, f"Expected 95 but got {score}"
