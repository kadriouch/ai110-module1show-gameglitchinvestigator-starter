import random
import streamlit as st
# FIX: Refactored all game logic out of app.py into logic_utils.py using Claude Agent mode.
# Verified by importing and running pytest — all 8 tests pass.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
# FEATURE (Challenge 2): High score tracker added via Agent Mode.
# high_scores.py handles reading/writing per-difficulty best scores to high_scores.json.
from high_scores import load_high_scores, save_high_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FEATURE (Challenge 2): Show high scores per difficulty in the sidebar.
# Claude Agent Mode suggested placing this near the top of the sidebar so it's
# always visible, and using st.sidebar.metric for a clean display.
st.sidebar.divider()
st.sidebar.subheader("🏆 High Scores")
high_scores = load_high_scores()
for diff in ["Easy", "Normal", "Hard"]:
    best = high_scores.get(diff, "—")
    st.sidebar.metric(label=diff, value=best)

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: Attempts initialized to 1 instead of 0, causing the counter to be off by one.
# Noticed when Debug panel showed attempts=3 after only 2 guesses. Fixed to start at 0.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game handler never reset status, so "won"/"lost" state persisted after clicking New Game.
# Claude initially pointed to st.stop() as the cause (incorrect). After tracing the status variable,
# found the real fix: add st.session_state.status = "playing" here. Verified by winning then clicking New Game.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

# FEATURE (Challenge 2): Guess History visualization.
# When a game is over (won or lost), show how close each guess was to the secret.
# Claude Agent Mode suggested using st.progress() with a normalized distance value,
# and color-coding rows by direction (too high = red, too low = blue, correct = green).
if st.session_state.status != "playing" and st.session_state.history:
    st.subheader("📊 Guess History")
    secret = st.session_state.secret
    range_size = high - low

    for i, guess in enumerate(st.session_state.history):
        if not isinstance(guess, int):
            continue
        distance = abs(guess - secret)
        closeness = max(0.0, 1.0 - distance / range_size)

        if guess == secret:
            label = f"Guess {i+1}: {guess} ✅ Correct!"
            color = "normal"
        elif guess > secret:
            label = f"Guess {i+1}: {guess} 🔴 Too High (off by {distance})"
            color = "normal"
        else:
            label = f"Guess {i+1}: {guess} 🔵 Too Low (off by {distance})"
            color = "normal"

        st.write(label)
        st.progress(closeness)

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # FEATURE (Challenge 2): Save high score on win.
            is_new_record = save_high_score(difficulty, st.session_state.score)
            win_msg = (
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            if is_new_record:
                win_msg += " 🏆 New high score!"
            st.success(win_msg)
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
