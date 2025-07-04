"""
Screen utility functions for clearing screen and managing display.

This module provides utilities for screen management and display control.
"""

import os
import re
import shutil
import sys

from colors import Colors, info, title, border


def clear_screen():
    """
    Clear the screen completely for full screen display.

    Uses multiple methods to ensure complete screen clearing:
    - System clear command
    - ANSI escape sequences for thorough cleaning
    - Multiple newlines for buffer clearing
    """
    # Clear screen using system command
    os.system('cls' if os.name == 'nt' else 'clear')

    # Additional ANSI escape sequences for complete clearing
    print('\033[H\033[J', end='')  # Move cursor to top-left and clear screen
    print('\033[2J', end='')       # Clear entire screen
    print('\033[3J', end='')       # Clear scrollback buffer (if supported)
    print('\033[H', end='')        # Move cursor to home position

    # Force flush to ensure immediate clearing
    sys.stdout.flush()

    # Add some space to ensure clean display
    print('\n' * 2, end='')


def display_last_action(command, result):
    """
    Display the last command and its result with colors.

    Args:
        command (str): The last command executed.
        result (str): The result of the last command.
    """
    if command and result:
        print(f"\n{info('Last action:')} {command}")
        print(f"{info('Result:')} {result}")
        print(border("-" * 50))


def wait_for_user():
    """
    Wait for user to press Enter before continuing.
    """
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")


def clear_and_show_header(header_title="Task Manager"):
    """
    Clear screen and show a formatted header with colors.

    Args:
        header_title (str): The title to display in the header.
    """
    clear_screen()
    print(border("=" * 50))
    print(title(f"        {header_title}"))
    print(border("=" * 50))


def display_full_screen_header(title_text, subtitle=None):
    """
    Display a full screen header with title and optional subtitle.

    Args:
        title_text (str): Main title to display
        subtitle (str, optional): Subtitle to display below main title
    """
    # Get terminal width, default to 80 if not available
    try:
        width = shutil.get_terminal_size().columns
    except (OSError, AttributeError):
        width = 80

    # Ensure minimum width
    width = max(width, 60)

    # Create top border
    top_border = "═" * width

    # Create title line centered
    title_line = f"║ {title_text.center(width-4)} ║"

    # Create subtitle line if provided
    if subtitle:
        subtitle_line = f"║ {subtitle.center(width-4)} ║"
    else:
        subtitle_line = f"║ {' ' * (width-4)} ║"

    # Create bottom border
    bottom_border = "═" * width

    # Display the header
    print(f"{Colors.CYAN}{top_border}")
    print(f"{Colors.YELLOW}{title_line}")
    print(f"{Colors.WHITE}{subtitle_line}")
    print(f"{Colors.CYAN}{bottom_border}{Colors.RESET}")
    print()


def display_full_screen_menu(menu_items, title_text, subtitle=None):
    """
    Display a full screen menu with centered items.

    Args:
        menu_items (list): List of menu items to display
        title_text (str): Main title for the menu
        subtitle (str, optional): Subtitle for the menu
    """
    clear_screen()
    display_full_screen_header(title_text, subtitle)

    # Get terminal width for centering
    try:
        width = shutil.get_terminal_size().columns
    except (OSError, AttributeError):
        width = 80

    # Ensure minimum width
    width = max(width, 60)

    # Display menu items centered
    for item in menu_items:
        # Remove ANSI color codes to calculate actual text length
        clean_item = re.sub(r'\x1b\[[0-9;]*m', '', item)

        # Calculate padding for centering
        padding = (width - len(clean_item.strip())) // 2
        centered_line = " " * padding + item

        print(centered_line)

    print()  # Extra spacing before input


def centered_input(prompt_text, width=None):
    """
    Display a centered input prompt.

    Args:
        prompt_text (str): The prompt text to display
        width (int, optional): Terminal width (auto-detected if None)

    Returns:
        str: User input
    """
    if width is None:
        try:
            width = shutil.get_terminal_size().columns
        except (OSError, AttributeError):
            width = 80

    # Ensure minimum width
    width = max(width, 60)

    # Center the prompt
    padding = (width - len(prompt_text)) // 2
    centered_prompt = " " * padding + prompt_text

    return input(centered_prompt)
