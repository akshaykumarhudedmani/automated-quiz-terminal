import os
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform ANSI color support
init(autoreset=True)

# Define color constants for easy usage
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title, color=CYAN):
    """Prints a styled header with a box border."""
    border = "=" * (len(title) + 6)
    print(f"\n{color}{BRIGHT}{border}")
    print(f"{color}{BRIGHT}== {title} ==")
    print(f"{color}{BRIGHT}{border}\n")

def print_divider(char="-", length=40, color=WHITE):
    """Prints a divider line."""
    print(f"{color}{char * length}{RESET}")

def safe_input(prompt, color=WHITE):
    """Wraps input() to handle KeyboardInterrupt gracefully."""
    try:
        user_input = input(f"{color}{prompt}{RESET}")
        return user_input.strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}\nOperation cancelled by user. Returning to main menu...")
        return None
