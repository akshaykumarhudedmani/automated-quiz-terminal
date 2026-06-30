# Automated Quiz Terminal 🧠🚀

Welcome to the **Automated Quiz Terminal**, a highly interactive, feature-rich command-line quiz application written in Python. Test your knowledge in Science, Math, History, and Computer Science with custom tracking, streaks, flashcards, scoreboards, and question reviews!

## Features

- 🎮 **Multiple Subjects:** Science, Mathematics, History, and Computer Science questions.
- ⏱️ **Timer-Based Scoring:** Earn speed bonuses by answering quickly. Countdown timer per question.
- 🔥 **Streak Multiplier:** Keep a streak of correct answers to multiply your score.
- 📓 **Flashcard Mode:** Study questions at your own pace before taking the real quiz.
- 🔄 **Review Mode:** Automatically logs incorrect answers to review and retry them later.
- 🏆 **Leaderboard (Highscores):** Dynamic local leaderboard records names, scores, and completion times.
- 🎨 **Visual Styling:** Rich terminal colors and dynamic screens (using ANSI colors or Colorama).
- 🧪 **Unit Tested:** Built-in automated test suites to verify loaders, scoring, and quiz state.

---

## Directory Structure

```
automated-quiz-terminal/
│
├── README.md
├── CONTRIBUTORS.md
├── requirements.txt
├── .gitignore                  
│
├── src/
│   ├── main.py                 # Entry point
│   ├── loader.py               # Load questions from JSON
│   ├── quiz.py                 # Quiz logic
│   ├── timer.py                # Timer functionality
│   ├── score.py                # Score calculations
│   ├── review.py               # Review incorrect answers
│   ├── flashcards.py           # Flashcard mode
│   └── utils.py                # Helper functions
│
├── questions/
│   ├── science.json
│   ├── math.json
│   ├── history.json
│   └── computer_science.json
│
├── data/
│   ├── highscores.json
│   └── incorrect_answers.json
│
├── tests/
│   ├── test_loader.py
│   ├── test_quiz.py
│   └── test_score.py
│
├── screenshots/
│   ├── quiz_menu.png
│   ├── quiz_running.png
│   ├── leaderboard.png
│   ├── github_issues.png
│   ├── branches.png
│   └── pull_requests.png
│
└── assets/
    ├── demo.gif
    └── logo.txt
```

---

## Installation & Setup

1. **Clone or download** this repository.
2. Navigate to the project root:
   ```bash
   cd automated-quiz-terminal
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Play

Start the application:
```bash
python src/main.py
```

### Main Menu Options:
1. **Take Quiz:** Select a category, choose a time limit per question, and start. Use `A`, `B`, `C`, or `D` to answer.
2. **Flashcards Mode:** Study any category at your own pace. Reveal answers and explanations.
3. **Review Incorrect Answers:** Re-test yourself only on questions you missed in previous quiz sessions.
4. **Leaderboard:** View high scores across categories.
5. **Exit:** Leave the application.

---

## Running Tests

Verify the code behaves as expected:
```bash
pytest tests/
```
or run with standard Python unittest:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
