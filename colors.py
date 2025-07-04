"""
Color utilities for the task manager system.
Provides ANSI color codes and formatting functions.
"""

class Colors:
    """ANSI color codes and formatting constants."""
    # Basic Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Reset
    RESET = '\033[0m'

    # Semantic Colors
    SUCCESS = GREEN
    ERROR = RED
    WARNING = YELLOW
    INFO = CYAN
    TITLE = YELLOW + BOLD
    BORDER = CYAN + BOLD
    PROMPT = CYAN + BOLD

def colorize(text, color):
    """
    Apply color to text and automatically reset.

    Args:
        text (str): Text to colorize
        color (str): Color code to apply

    Returns:
        str: Colorized text with reset at the end
    """
    return f"{color}{text}{Colors.RESET}"

def success(text):
    """Green text for success messages."""
    return colorize(text, Colors.SUCCESS)

def error(text):
    """Red text for error messages."""
    return colorize(text, Colors.ERROR)

def warning(text):
    """Yellow text for warning messages."""
    return colorize(text, Colors.WARNING)

def info(text):
    """Cyan text for info messages."""
    return colorize(text, Colors.INFO)

def title(text):
    """Yellow bold text for titles."""
    return colorize(text, Colors.TITLE)

def border(text):
    """Cyan bold text for borders."""
    return colorize(text, Colors.BORDER)

def prompt(text):
    """Cyan bold text for prompts."""
    return colorize(text, Colors.PROMPT)
