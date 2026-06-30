import os
import json
from datetime import datetime
from src.utils import GREEN, YELLOW, CYAN, RESET, BRIGHT, print_header, print_divider

def get_highscores_path() -> str:
    """
    Gets the absolute path to highscores.json.
    
    Returns:
        str: Absolute system path to highscores file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "highscores.json")

def load_highscores() -> dict:
    """
    Loads highscores from highscores.json, returning a dictionary structure.
    
    Returns:
        dict: Highscore listings grouped by category keys.
    """
    path = get_highscores_path()
    if not os.path.exists(path):
        return {"science": [], "math": [], "history": [], "computer_science": []}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {"science": [], "math": [], "history": [], "computer_science": []}

def calculate_score(correct: bool, time_remaining: float, total_time: float, streak: int) -> int:
    """
    Calculates the score for a single question.
    - Base points for correct answer: 100
    - Speed bonus: proportional to remaining time (up to 50 points)
    - Streak multiplier: +10% per consecutive correct answer (e.g., streak of 2 gives 1.1x)
    
    Args:
        correct (bool): True if answer was correct.
        time_remaining (float): Remaining seconds on the question countdown timer.
        total_time (float): Total timer limit allowed for the question.
        streak (int): Current streak of correct answers.
        
    Returns:
        int: Total points earned for the question.
    """
    if not correct:
        return 0
        
    base_points = 100
    
    # Speed bonus
    speed_bonus = 0
    if total_time and total_time > 0 and time_remaining and time_remaining > 0:
        speed_ratio = time_remaining / total_time
        speed_bonus = int(speed_ratio * 50)
        
    # Streak multiplier
    streak_multiplier = 1.0 + max(0, (streak - 1) * 0.1)
    
    total = int((base_points + speed_bonus) * streak_multiplier)
    return total

def save_highscore(category: str, name: str, score: int, max_streak: int) -> None:
    """
    Saves a player's score to the leaderboard.
    Sorts highscores in descending order and keeps top 5.
    """
    highscores = load_highscores()
    
    # Ensure category list exists
    if category not in highscores:
        highscores[category] = []
        
    entry = {
        "name": name,
        "score": score,
        "max_streak": max_streak,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    highscores[category].append(entry)
    # Sort descending by score, then max_streak
    highscores[category].sort(key=lambda x: (x["score"], x["max_streak"]), reverse=True)
    # Keep top 5
    highscores[category] = highscores[category][:5]
    
    path = get_highscores_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(highscores, f, indent=2)

def display_leaderboard(category: str = None) -> None:
    """
    Displays the leaderboard table.
    If category is provided, displays only that category. Otherwise, displays all.
    
    Args:
        category (str, optional): The category to filter by (e.g. 'math'). Defaults to None.
    """
    highscores = load_highscores()
    
    categories = [category] if category else list(highscores.keys())
    
    print_header("LEADERBOARDS")
    
    for cat in categories:
        cat_title = cat.replace("_", " ").title()
        print(f"\n{YELLOW}{BRIGHT}Category: {cat_title}{RESET}")
        print_divider("=", 60, CYAN)
        print(f"{BRIGHT}{'Rank':<6}{'Name':<15}{'Score':<10}{'Max Streak':<12}{'Date':<20}{RESET}")
        print_divider("-", 60, CYAN)
        
        entries = highscores.get(cat, [])
        if not entries:
            print(f"  No high scores yet! Be the first to play.")
        else:
            for rank, entry in enumerate(entries, 1):
                name = entry.get("name", "Unknown")
                score = entry.get("score", 0)
                streak = entry.get("max_streak", 0)
                date_str = entry.get("date", "N/A")
                print(f"  #{rank:<4}{name:<15}{score:<10}{streak:<12}{date_str:<20}")
        print_divider("=", 60, CYAN)
