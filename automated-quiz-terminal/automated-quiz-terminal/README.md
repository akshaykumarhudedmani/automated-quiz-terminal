# Automated Quiz Terminal

The **Automated Quiz Terminal** is a Python-based command-line application designed for interactive knowledge assessment[cite: 1]. It features subject-specific quizzes, timed scoring systems, flashcard study modes, performance tracking, and a local leaderboard[cite: 1]. 

## Key Features

* **Multi-Subject Quizzes:** Supports structured question sets across Science, Mathematics, History, and Computer Science[cite: 1].
* **Timed Scoring System:** Incorporates a countdown timer per question with dynamic speed bonuses for quick responses[cite: 1].
* **Streak Multiplier:** Tracks consecutive correct answers to apply scoring multipliers[cite: 1].
* **Flashcard Mode:** Allows self-paced study and question review prior to taking active quizzes[cite: 1].
* **Review Mode:** Captures incorrect answers automatically, enabling targeted re-testing and remediation[cite: 1].
* **Local Leaderboard:** Records user performance metrics, including names, total scores, and completion times[cite: 1].
* **Terminal UI Styling:** Utilizes ANSI formatting and Colorama for structured, readable command-line interfaces[cite: 1].
* **Automated Testing:** Equipped with a comprehensive `pytest`/`unittest` suite verifying data loading, scoring logic, and state management[cite: 1].

---

## Directory Structure

```text
automated-quiz-terminal/
│
├── README.md
├── CONTRIBUTORS.md
├── requirements.txt
├── .gitignore                  
│
├── src/
│   ├── main.py                 # Application entry point
│   ├── loader.py               # JSON data parsing and validation
│   ├── quiz.py                 # Core quiz state and runtime logic
│   ├── timer.py                # Countdown and timing mechanics
│   ├── score.py                # Scoring and multiplier calculations
│   ├── review.py               # Logic for reviewing incorrect answers
│   ├── flashcards.py           # Flashcard execution engine
│   └── utils.py                # Shared utility functions
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
```[cite: 1]

---

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/automated-quiz-terminal.git](https://github.com/yourusername/automated-quiz-terminal.git)
   ```[cite: 1]
2. Navigate to the project root directory:
   ```bash
   cd automated-quiz-terminal
   ```[cite: 1]
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```[cite: 1]

---

## Usage Guide

Execute the application entry point to start the terminal interface:
```bash
python src/main.py
```[cite: 1]

### Application Modes:
1. **Take Quiz:** Select a question category and set a per-question time limit. Input answers using `A`, `B`, `C`, or `D`[cite: 1].
2. **Flashcards Mode:** Browse questions within a specific category without time constraints. Includes answer reveals and explanations[cite: 1].
3. **Review Mode:** Isolates and re-tests questions failed during previous quiz attempts[cite: 1].
4. **Leaderboard:** Displays historical high scores filtered by category[cite: 1].
5. **Exit:** Terminate the session and safely close the application[cite: 1].

---

## Running the Test Suite

To execute the automated test suite and verify system components, run:

```bash
pytest tests/
```[cite: 1]

Alternatively, you can use Python's built-in `unittest` module:
```bash
python -m unittest discover -s tests -p "test_*.py"