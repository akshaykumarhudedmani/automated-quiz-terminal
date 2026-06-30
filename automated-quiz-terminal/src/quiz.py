import time
from src.utils import GREEN, RED, YELLOW, CYAN, RESET, BRIGHT, print_header, print_divider, safe_input
from src.timer import get_choice_with_timeout
from src.score import calculate_score, save_highscore, display_leaderboard
from src.review import log_incorrect_answer

def run_quiz(category, questions, time_limit):
    """
    Executes the interactive quiz session.
    - Prompts the user for their name.
    - Loops through questions, managing timer and scoring.
    - Logs incorrect answers for review.
    - Saves high score.
    """
    category_title = category.replace("_", " ").title()
    print_header(f"STARTING QUIZ: {category_title}", CYAN)
    
    # Prompt for user name
    name = safe_input("Enter your name for the leaderboard (default: Player): ")
    if name is None:
        return
    name = name.strip() or "Player"
    
    # Explain timer setting
    if time_limit and time_limit > 0:
        print(f"\n{YELLOW}You have chosen a {time_limit} second time limit per question.{RESET}")
    else:
        print(f"\n{YELLOW}No time limit. Take your time!{RESET}")
        
    safe_input("Press Enter to begin the quiz...")
    
    score = 0
    streak = 0
    max_streak = 0
    correct_count = 0
    total_questions = len(questions)
    
    for idx, q in enumerate(questions, 1):
        print_header(f"Question {idx} of {total_questions} | Current Score: {score} | Streak: {streak}", CYAN)
        print(f"{BRIGHT}{q['question']}{RESET}\n")
        
        for option in q['options']:
            print(f"  {option}")
        print()
        
        # Start question timing
        start_time = time.time()
        choice = get_choice_with_timeout(time_limit)
        elapsed_time = time.time() - start_time
        
        if choice is None:
            # Timed out
            streak = 0
            print(f"\n{RED}{BRIGHT}Time's Up!{RESET}")
            print(f"{YELLOW}The correct answer was: {q['answer']}{RESET}")
            print(f"{CYAN}Explanation: {q['explanation']}{RESET}")
            log_incorrect_answer(category, q)
        elif choice == q['answer']:
            # Correct answer
            streak += 1
            max_streak = max(max_streak, streak)
            correct_count += 1
            
            # Calculate score with remaining time bonus
            time_remaining = max(0.0, time_limit - elapsed_time) if time_limit else 0.0
            points_gained = calculate_score(True, time_remaining, time_limit, streak)
            score += points_gained
            
            print(f"\n{GREEN}{BRIGHT}[CORRECT] (+{points_gained} points){RESET}")
            if streak > 1:
                print(f"{YELLOW}{BRIGHT}Streak multiplier active! {streak} in a row!{RESET}")
        else:
            # Incorrect answer
            streak = 0
            print(f"\n{RED}{BRIGHT}[INCORRECT]{RESET}")
            print(f"{YELLOW}The correct answer was: {q['answer']}{RESET}")
            print(f"{CYAN}Explanation: {q['explanation']}{RESET}")
            log_incorrect_answer(category, q)
            
        print_divider("=", 60, CYAN)
        
        # Wait a moment between questions unless it's the last one
        if idx < total_questions:
            nxt = safe_input("Press Enter to continue to next question... (or type 'q' to quit) ")
            if nxt is not None and nxt.lower() == 'q':
                print(f"\n{YELLOW}Quiz terminated early. Saving progress...{RESET}")
                break
                
    # Final Summary Screen
    print_header("QUIZ OVER - SUMMARY", GREEN)
    print(f"Player: {BRIGHT}{name}{RESET}")
    print(f"Final Score: {BRIGHT}{score}{RESET}")
    print(f"Accuracy: {BRIGHT}{correct_count}/{total_questions}{RESET} ({int((correct_count/total_questions)*100)}%)")
    print(f"Max Streak: {BRIGHT}{max_streak}{RESET}")
    
    # Save highscore
    save_highscore(category, name, score, max_streak)
    print(f"\n{GREEN}High score saved to leaderboard!{RESET}")
    
    # Ask if user wants to see the leaderboard
    view_leader = safe_input("\nWould you like to view the leaderboard? (Y/N): ")
    if view_leader is not None and view_leader.lower() == 'y':
        display_leaderboard(category)
        safe_input("\nPress Enter to return to main menu...")
