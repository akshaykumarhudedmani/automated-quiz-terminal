from src.utils import GREEN, YELLOW, CYAN, RESET, BRIGHT, print_header, print_divider, safe_input

def run_flashcards(category: str, questions: list) -> None:
    """
    Runs the Flashcard study mode for a given category.
    Allows user to cycle through questions, reveal answers, and read explanations.
    
    Args:
        category (str): The subject category name.
        questions (list): The list of question dictionaries.
    """
    if not questions:
        print(f"\n{YELLOW}No questions found in this category.{RESET}")
        safe_input("\nPress Enter to return to main menu...")
        return
        
    category_title = category.replace("_", " ").title()
    print_header(f"FLASHCARDS: {category_title}", YELLOW)
    print("Study mode: review questions, press Enter to reveal the correct answer and explanation.\n")
    
    total_cards = len(questions)
    
    for idx, q in enumerate(questions, 1):
        print_divider("=", 60, YELLOW)
        print(f"{YELLOW}{BRIGHT}Card {idx} of {total_cards}{RESET}")
        print(f"\n{BRIGHT}Question: {q['question']}{RESET}")
        print("\nOptions:")
        for opt in q['options']:
            print(f"  {opt}")
            
        print_divider("-", 40, YELLOW)
        
        # Wait for user to reveal
        reveal = safe_input("Press Enter to reveal the correct answer... (or type 'q' to quit) ")
        if reveal is not None and reveal.lower() == 'q':
            print(f"\n{YELLOW}Exiting flashcard study session.{RESET}")
            break
            
        print(f"\n{GREEN}{BRIGHT}Correct Answer: {q['answer']}{RESET}")
        print(f"{CYAN}{BRIGHT}Explanation: {q['explanation']}{RESET}")
        print_divider("=", 60, YELLOW)
        
        if idx < total_cards:
            next_card = safe_input("Press Enter for the next card... (or type 'q' to quit) ")
            if next_card is not None and next_card.lower() == 'q':
                print(f"\n{YELLOW}Exiting flashcard study session.{RESET}")
                break
        else:
            print(f"\n{GREEN}You have reviewed all flashcards in this category!{RESET}")
            safe_input("\nPress Enter to return to the main menu...")
