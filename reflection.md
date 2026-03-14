# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Based on my first impression, the game looks logic and interesting to play.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  * The Developer Debug revealed the secret number was 24, I entered 25, the hint asked me to go higher. I also guessed 23 and the hint message asked me go lower.
  * The game is displaying the message: "You already won. Start a new game to play again." However, clicking the button doesn't seem to clear this flag or reset the UI.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I am using Claude AI
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Claude confirmed the bugs that I discovered while playing 2 games. Claude suggested that the inverted hints were caused by a flipped comparison in check_guess, when guess > secret, the returned "GO HIGHER!" instead of "GO LOWER!". I verified this by checking the Developer Debug panel, confirming the secret was 24, guessing 25 (higher), and seeing the game tell me to go higher instead of lower.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Claude initially suggested that the "You already won" bug was caused by the st.stop() call on line 145 blocking the New Game button from executing. I tested this by moving st.stop() lower in the file, but the bug persisted. After reading the code more carefully, I found the real cause: the new_game block never resets st.session_state.status back to "playing", so the game stays stuck in the "won" state no matter what. The AI's first explanation pointed me to the wrong line and I had to trace the status variable myself to find the actual fix.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I check if a bug is really fixed by reproducing the exact steps that caused it originally, then confirming the broken behavior no longer happened. For the inverted hints, I used the Developer Debug panel to confirm the secret number, then guessed one number above and one below it to verify both directions gave the correct feedback. For the "You already won" bug, I deliberately won a game, then clicked New Game and immediately tried to play — if I could submit a guess without seeing the stuck message, the fix worked. I treated each bug like a small test: same input, different expected output.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
I tested manually using the Developer Debug panel to know the secret number in advance. I set the secret to 24 by refreshing until I saw it, then guessed 25 (one above) and watched the hint. It said "Go HIGHER!" — which is wrong since my guess was already too high. This confirmed the comparison in check_guess was inverted and showed me exactly which line needed to change.

- Did AI help you design or understand any tests? How?
Yes, Claude helped me understand what to test and why. When I described the inverted hints bug, Claude explained that a good test should use a known secret number and check both directions — one guess above and one below — to confirm both hint messages were correct. It also pointed out that the Developer Debug panel was essentially acting as a test fixture, giving me a known input to test against. I wouldn't have thought to test both directions systematically without that suggestion.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
In the original app, the secret number was generated with `random.randint()` directly every time the script ran, without checking if one already existed. Streamlit reruns the entire Python script from top to bottom on every user interaction — clicking a button, typing in a field, anything. So every interaction triggered a new random number, replacing the old one. The fix was wrapping the generation in `if "secret" not in st.session_state`, which makes Streamlit only generate the number once and store it persistently across reruns.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine every time you click a button on a webpage, the whole page reloads from scratch and forgets everything. That's basically what Streamlit does — every interaction reruns the entire Python script. Session state is like a sticky notepad that survives those reloads. Instead of losing your data on every rerun, you store it in `st.session_state` and Streamlit remembers it. So the secret number, your score, and your guess history all stay intact between clicks because they're saved on that notepad, not just in a regular variable that disappears.
- What change did you make that finally gave the game a stable secret number?
I wrapped the secret number generation in an `if "secret" not in st.session_state` check, so the random number is only generated once — the very first time the app loads. After that, every rerun finds the key already in session state and skips the generation entirely. I also stored the result in `st.session_state.secret` instead of a plain variable, so it persists across all interactions for the life of the session.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I want to keep using the "reproduce first, then fix" habit — always confirming I can reliably trigger a bug before attempting a fix. This project showed me that if you can't reproduce a bug consistently, you don't fully understand it yet, and any fix you make is just a guess.
- What is one thing you would do differently next time you work with AI on a coding task?
Next time, I would ask AI to explain *why* a fix works, not just *what* to change. On this project I sometimes applied a suggestion without fully understanding the reasoning, which made it harder to catch when the AI was wrong. Asking "why does this fix it?" would have helped me verify suggestions faster.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project taught me that AI-generated code can look completely correct and still have subtle logic bugs baked in. I now treat AI output as a first draft that needs the same careful review I'd give any untested code.
