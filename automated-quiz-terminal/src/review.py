import os
import json
from src.utils import GREEN, RED, YELLOW, CYAN, RESET, BRIGHT, print_header, print_divider, safe_input
from src.timer import get_choice_with_timeout

def get_incorrect_answers_path():
    """Gets the absolute path to incorrect_answers.json."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "incorrect_answers.json")

def load_incorrect_answers():
    """Loads incorrect answers from incorrect_answers.json."""
    path = get_incorrect_answers_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def save_incorrect_answers_list(answers_list):
    """Saves the entire list of incorrect answers to incorrect_answers.json."""
    path = get_incorrect_answers_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(answers_list, f, indent=2)

def log_incorrect_answer(category, question_obj):
    """
    Saves a specific incorrect question.
    Avoids duplicate entries by checking category and question text.
    """
    incorrect_list = load_incorrect_answers()
    
    # Check if already present
    exists = any(
        item.get("category") == category and item.get("question") == question_obj["question"]
        for item in incorrect_list
    )
    
    if not exists:
        entry = {
            "category": category,
            "id": question_obj["id"],
            "question": question_obj["question"],
            "options": question_obj["options"],
            "answer": question_obj["answer"],
            "explanation": question_obj["explanation"]
        }
        incorrect_list.append(entry)
        save_incorrect_answers_list(incorrect_list)

def run_review_mode():
    """
    Runs the Review Mode session.
    Presents incorrect questions. If answered correctly, removes them from the list.
    """
    incorrect_list = load_incorrect_answers()
    
    if not incorrect_list:
        print_header("REVIEW MODE", RED)
        print(f"{YELLOW}No incorrect answers logged! You are doing great!{RESET}")
        safe_input("\nPress Enter to return to main menu...")
        return
        
    print_header(f"REVIEW MODE ({len(incorrect_list)} Questions)", RED)
    print("Welcome to Review Mode. Answer correctly to remove questions from your review list.")
    print("No timers are active here. Take your time!\n")
    
    # Copy list to iterate safely
    remaining_incorrect = list(incorrect_list)
    resolved_count = 0
    
    for item in incorrect_list:
        category_title = item["category"].replace("_", " ").title()
        print(f"\n{CYAN}{BRIGHT}Category: {category_title}{RESET}")
        print(f"{BRIGHT}Question: {item['question']}{RESET}")
        for option in item["options"]:
            print(f"  {option}")
            
        print_divider("-", 40)
        
        # Get answer without timer
        choice = get_choice_with_timeout(timeout_seconds=None)
        
        if choice is None:
            # User aborted (or similar), wait
            break
            
        correct_answer = item["answer"].upper()
        if choice == correct_answer:
            print(f"{GREEN}{BRIGHT}Correct! Nice job!{RESET}")
            print(f"{YELLOW}Explanation: {item['explanation']}{RESET}")
            # Remove from the list
            remaining_incorrect.remove(item)
            resolved_count += 1
        else:
            print(f"{RED}{BRIGHT}Incorrect. The correct answer was {correct_answer}.{RESET}")
            print(f"{YELLOW}Explanation: {item['explanation']}{RESET}")
            
        print_divider("=", 40)
        
    # Save the updated list
    save_incorrect_answers_list(remaining_incorrect)
    
    print(f"\n{GREEN}{BRIGHT}Review session completed!{RESET}")
    print(f"You resolved {resolved_count} incorrect question(s).")
    print(f"{YELLOW}{len(remaining_incorrect)} question(s) remain in your review list.{RESET}")
    safe_input("\nPress Enter to return to main menu...")
