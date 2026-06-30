import os
import sys
import random

# Ensure parent directory is in python path so imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import (
    clear_screen, print_header, print_divider, safe_input, 
    CYAN, YELLOW, GREEN, RED, MAGENTA, RESET, BRIGHT
)
from src.loader import load_questions, QuestionSchemaError
from src.quiz import run_quiz
from src.flashcards import run_flashcards
from src.review import run_review_mode
from src.score import display_leaderboard

def load_logo() -> str:
    """
    Reads and returns the ASCII logo banner.
    
    Returns:
        str: The ASCII art text loaded from assets, or fallback text.
    """
    logo_path = os.path.join(project_root, "assets", "logo.txt")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            pass
    return "=== AUTOMATED QUIZ TERMINAL ==="

def choose_category(prompt_title: str) -> str:
    """
    Presents the category selection menu.
    Returns the string name of the chosen category (matching filenames), or None if cancelled.
    
    Args:
        prompt_title (str): Header text displayed above categories.
        
    Returns:
        str: Chosen category string (e.g. 'science'), or None if cancelled.
    """
    categories = {
        "1": ("Science", "science"),
        "2": ("Mathematics", "math"),
        "3": ("History", "history"),
        "4": ("Computer Science", "computer_science")
    }
    
    while True:
        clear_screen()
        print_header(prompt_title, MAGENTA)
        for num, (name, _) in categories.items():
            print(f"  {num}. {name}")
        print("  5. Back to Main Menu")
        print_divider("-", 40, MAGENTA)
        
        choice = safe_input("Select an option (1-5): ")
        if choice is None or choice == "5":
            return None
            
        if choice in categories:
            return categories[choice][1]
            
        print(f"\n{RED}Invalid selection. Please choose 1-5.{RESET}")
        time_sleep_msg()

def choose_timer():
    """
    Presents the timer option selection.
    Returns the number of seconds per question, or None for no limit, or -1 if cancelled.
    """
    timer_options = {
        "1": ("No time limit", None),
        "2": ("10 seconds per question", 10),
        "3": ("20 seconds per question", 20),
        "4": ("30 seconds per question", 30)
    }
    
    while True:
        clear_screen()
        print_header("SELECT QUESTION TIMER", MAGENTA)
        for num, (desc, _) in timer_options.items():
            print(f"  {num}. {desc}")
        print("  5. Cancel and return")
        print_divider("-", 40, MAGENTA)
        
        choice = safe_input("Select an option (1-5): ")
        if choice is None or choice == "5":
            return -1
            
        if choice in timer_options:
            return timer_options[choice][1]
            
        print(f"\n{RED}Invalid selection. Please choose 1-5.{RESET}")
        time_sleep_msg()

def time_sleep_msg():
    import time
    time.sleep(1)

def main():
    """Main execution loop of the Automated Quiz Terminal."""
    logo = load_logo()
    
    while True:
        clear_screen()
        # Print Logo and Main Options
        print(f"{CYAN}{BRIGHT}{logo}{RESET}")
        print_header("MAIN MENU", CYAN)
        print(f"  {BRIGHT}1.{RESET} Take a Quiz")
        print(f"  {BRIGHT}2.{RESET} Flashcards Study Mode")
        print(f"  {BRIGHT}3.{RESET} Review Incorrect Answers")
        print(f"  {BRIGHT}4.{RESET} View Leaderboards")
        print(f"  {BRIGHT}5.{RESET} Exit Game")
        print_divider("=", 60, CYAN)
        
        choice = safe_input("Select option (1-5): ")
        if choice is None or choice == "5":
            print(f"\n{GREEN}Thank you for playing Automated Quiz Terminal! Goodbye!{RESET}")
            sys.exit(0)
            
        if choice == "1":
            # Quiz Mode
            category = choose_category("SELECT QUIZ CATEGORY")
            if not category:
                continue
                
            timer_limit = choose_timer()
            if timer_limit == -1:
                continue
                
            try:
                questions = load_questions(category)
                # Shuffle the questions for variety
                shuffled_questions = list(questions)
                random.shuffle(shuffled_questions)
                
                # Start quiz
                run_quiz(category, shuffled_questions, timer_limit)
            except Exception as e:
                print(f"\n{RED}Error starting quiz: {str(e)}{RESET}")
                safe_input("\nPress Enter to return to main menu...")
                
        elif choice == "2":
            # Flashcards Mode
            category = choose_category("SELECT STUDY CATEGORY")
            if not category:
                continue
                
            try:
                questions = load_questions(category)
                run_flashcards(category, questions)
            except Exception as e:
                print(f"\n{RED}Error starting flashcards: {str(e)}{RESET}")
                safe_input("\nPress Enter to return to main menu...")
                
        elif choice == "3":
            # Review Incorrect Answers
            try:
                run_review_mode()
            except Exception as e:
                print(f"\n{RED}Error running review: {str(e)}{RESET}")
                safe_input("\nPress Enter to return to main menu...")
                
        elif choice == "4":
            # Leaderboards
            display_leaderboard()
            safe_input("\nPress Enter to return to main menu...")
            
        else:
            print(f"\n{RED}Invalid option '{choice}'. Please select 1-5.{RESET}")
            time_sleep_msg()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
