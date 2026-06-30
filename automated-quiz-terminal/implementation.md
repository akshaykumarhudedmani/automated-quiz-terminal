# IMPLEMENTATION.md

# Automated Quiz / Flashcard Terminal Application

## Team 4 — SCM Final Project

---
# What our problem statement and question was for this assignment (Teacher's WhatsApp msg)
we have this as our final project for our source code management

I have attached the Google Sheets link containing the project problem statements assigned to each team. You may start working on the project allocated to your team. If you have any queries or require any changes to the assigned problem statement, please contact me.

Link: https://docs.google.com/spreadsheets/d/1Zsn1MxMZTqImFG1ZxyA3d9_5h2OoXIBxi4xHNKSX-rU/edit?usp=sharing

Project Requirements (Mandatory):
* Maintain a GitHub repository for the project.
* Use GitHub branches for development.
* Create a minimum of 25 commits.
* Use pull requests for merging changes.
* Maintain a CONTRIBUTORS.md file.
* Write a proper README.md file.
* Use a .gitignore file.
* Create at least 5 GitHub Issues.
* Tag at least one release version.
* Submit project screenshots or …
[11:49 PM, 6/17/2026] +91 79871 32385: Students whose names are not mentioned in the project tracker or who have not been assigned to any team are requested to contact me either via text message or in person on or before 20th June.

All teams must submit their github project link by 30th June. A short project presentation & review will be conducted on 1st July.


the team and the statement we are assigned is 	"Automated Quiz/Flashcard Terminal Application

A terminal app that loads question banks from external files, runs timed multiple-choice quizzes, tracks high scores, and saves incorrect answers for later review."
( Team 4	Akshay Kumar	
Thanmay M Gowda	
	B S Lichal Bopanna	
	Mohammed Huzain Raza	
	Basava Anand Akkimaradi	
	Jayanth P	
	Dhanush B N	) here im akshay the main guy to do all things, they all dont know much, so i will give them something easy role or commiting things with guiding them , so say me everything we have to do first, like what w e are given and wt we have to do and how to maximize  the full score potential
, here also we have to present it




# Purpose

This document explains **exactly what needs to be coded**, in what order, what each module should do, what its inputs and outputs are, and how the final application should behave.

This serves as:

* Coding reference
* LLM prompt context
* Team implementation guide
* Revision document
* Progress tracker

---

# Development Philosophy

This is an SCM project.

Priority order:

1. Working application
2. Clean architecture
3. Git practices
4. Documentation
5. Bonus features

Do not overengineer.

A stable implementation is better than an advanced but broken implementation.

---

# Final Application Flow

```text
User launches app

↓

Main Menu

↓

Select Mode

↓

Quiz
Flashcards
Review
Leaderboard

↓

Load JSON data

↓

Execute feature

↓

Update persistent storage

↓

Return to menu
```

---

# Coding Order

Implement modules in this sequence.

## Step 1

loader.py

## Step 2

score.py

## Step 3

review.py

## Step 4

flashcards.py

## Step 5

quiz.py

## Step 6

main.py

## Step 7

timer.py

## Step 8

testing

## Step 9

polishing

---

# MODULE 1

# loader.py

## Purpose

Loads question files.

Reads JSON.

Validates structure.

Returns Python objects.

---

## Questions Format

Example

```json
[
 {
  "id":1,

  "question":"Capital of India?",

  "options":
  [
   "Delhi",
   "Mumbai",
   "Pune",
   "Chennai"
  ],

  "answer":0,

  "explanation":"Delhi is India's capital."
 }
]
```

---

## Required Functions

### load_questions()

Input

```python
"questions/science.json"
```

Output

```python
list
```

Example

```python
questions = load_questions("questions/science.json")
```

---

### validate_questions()

Checks:

Question exists

Options exist

Exactly four options

Answer exists

Answer index valid

Question id valid

---

### get_categories()

Returns

```python
[
"science",

"math",

"history",

"computer_science"
]
```

---

Expected status after completion

✓ Questions load

✓ Invalid JSON rejected

✓ Categories available

---

# MODULE 2

# score.py

Purpose

Manage leaderboard.

Calculate final score.

Persist scores.

---

Storage file

```text
data/highscores.json
```

---

Functions

### save_score()

Input

```python
name

score
```

Append record.

Save JSON.

---

### load_scores()

Read file.

Return list.

---

### sort_scores()

Sort descending.

Highest score first.

---

### display_leaderboard()

Output

```text
LEADERBOARD

1 Akshay 950

2 Basava 920

3 Huzain 880
```

---

Expected completion

✓ Score saving works

✓ Leaderboard sorted

✓ JSON persists

---

# MODULE 3

# review.py

Purpose

Store incorrect answers.

Allow retrying mistakes.

---

Storage

```text
data/incorrect_answers.json
```

---

Functions

### save_incorrect()

Input

Question object.

Store in file.

---

### load_incorrect()

Read file.

Return list.

---

### review_questions()

Display mistakes.

Show answer.

Allow retry.

---

### remove_completed()

Delete correctly answered entries.

---

Expected state

✓ Wrong questions stored

✓ Review works

✓ Retry works

---

# MODULE 4

# flashcards.py

Purpose

Study mode.

No timer.

No scoring.

Learning only.

---

Functions

### show_flashcards()

Select category.

Load questions.

---

Display

```text
Question

↓

Press Enter

↓

Answer

↓

Next card
```

---

Example

```text
Question:

What is RAM?

Press Enter

Answer:

Random Access Memory
```

---

Expected state

✓ Flashcards usable

✓ Cards cycle properly

---

# MODULE 5

# timer.py

Purpose

Countdown system.

---

Simple implementation preferred.

Avoid complex keyboard hooks.

---

Functions

### start_timer()

Input

```python
seconds=15
```

Output

Remaining time.

---

Alternative

Measure elapsed time.

Example

```python
start=time.time()

answer=input()

elapsed=time.time()-start
```

---

If elapsed > limit

```text
Time Up
```

---

Expected state

✓ Timer functional

✓ Expired questions detected

---

# MODULE 6

# quiz.py

Purpose

Core gameplay engine.

This is the largest module.

---

Workflow

```text
Load questions

↓

Shuffle

↓

Display question

↓

Start timer

↓

Get answer

↓

Check correctness

↓

Update score

↓

Save mistakes

↓

Next question

↓

Final summary
```

---

Functions

### start_quiz()

Main controller.

---

### ask_question()

Display MCQ.

---

### check_answer()

Compare answer.

Return True or False.

---

### calculate_result()

Correct count.

Wrong count.

Accuracy.

---

### save_wrong_answer()

Call review module.

---

Expected state

✓ Full quiz works

✓ Questions cycle

✓ Score updates

✓ Mistakes stored

---

# MODULE 7

# main.py

Purpose

Application entry point.

Navigation system.

---

Banner

```text
==================================

AUTOMATED QUIZ TERMINAL

==================================
```

---

Menu

```text
1 Start Quiz

2 Flashcards

3 Review Mistakes

4 Leaderboard

5 Exit
```

---

Flow

Choice 1

↓

Quiz

Choice 2

↓

Flashcards

Choice 3

↓

Review

Choice 4

↓

Leaderboard

Choice 5

↓

Exit

---

Functions

### show_menu()

---

### execute_choice()

---

### run()

Main loop.

---

Expected state

✓ Menu stable

✓ Navigation works

✓ Exit safe

---

# MODULE 8

# utils.py

Purpose

Reusable helper functions.

---

Functions

### clear_screen()

---

### pause()

Wait for Enter.

---

### print_banner()

ASCII logo.

---

### safe_input()

Handles invalid input.

---

Expected state

✓ Cleaner code

✓ Shared utilities

---

# MODULE 9

# tests

Purpose

Validation.

SCM demonstration.

---

Files

```text
tests/

test_loader.py

test_quiz.py

test_score.py
```

---

Suggested tests

Question file loads

Score saves

Leaderboard sorts

Invalid file rejected

Wrong answer saved

---

Expected state

✓ Tests execute

✓ Pass successfully

---

# FINAL APPLICATION EXPERIENCE

User opens application.

Sees:

```text
=================================

AUTOMATED QUIZ TERMINAL

=================================

1 Start Quiz

2 Flashcards

3 Review Mistakes

4 Leaderboard

5 Exit
```

---

Quiz

```text
Question 4 / 10

Capital of India?

A Delhi

B Mumbai

C Pune

D Chennai

Time Left : 15

Answer:
```

---

Results

```text
Quiz Finished

Correct : 8

Wrong : 2

Accuracy : 80%

Score : 800
```

---

Leaderboard

```text
LEADERBOARD

1 Akshay 950

2 Basava 920

3 Huzain 900
```

---

Review

```text
Question:

Capital of Japan

Your Answer:

Osaka

Correct Answer:

Tokyo
```

---

Flashcards

```text
Question:

What is recursion?

Press Enter

Answer:

Function calling itself.
```

---
