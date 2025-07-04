"""
Task Manager Application - Password Utilities Module

This module provides secure password input functionality with visual feedback.
It handles cross-platform password input with asterisk masking and supports
both Windows and Unix/Linux systems.

Features:
- Password masking with asterisks (*) for security
- Cross-platform compatibility (Windows, Linux, macOS)
- Backspace support for character deletion
- Escape key support for cancellation (platform dependent)
- Real-time character feedback
- Secure input handling without echoing to terminal

Security Features:
- No password echoing to terminal or command history
- Immediate character masking upon input
- Proper terminal state restoration after input
- Graceful fallback to getpass module if needed

The module automatically detects the operating system and uses the appropriate
implementation for secure password input, ensuring consistent behavior across
different platforms.
"""

import sys
import os
import getpass

# Platform-specific imports with fallbacks
try:
    import msvcrt  # Windows only
except ImportError:
    msvcrt = None

try:
    import termios  # Unix/Linux only
    import tty
except ImportError:
    termios = None
    tty = None

def get_password_with_asterisks(prompt="Password: "):
    """
    Get password input with asterisks displayed for each character typed.
    Works on both Windows and Linux/Unix systems.

    Features:
    - Shows asterisks (*) as characters are typed
    - Supports backspace to delete characters
    - Press Enter to confirm
    - Press Escape to cancel (Windows only)

    Args:
        prompt (str): The prompt to display before password input

    Returns:
        str: The entered password, or None if cancelled
    """
    # Check if we're on Windows
    if os.name == 'nt':
        return _get_password_windows(prompt)
    else:
        return _get_password_unix(prompt)

def _get_password_windows(prompt):
    """Windows implementation using msvcrt"""
    if msvcrt is None:
        # Fallback to getpass if msvcrt is not available
        return getpass.getpass(prompt)

    print(prompt, end='', flush=True)
    password = ""

    while True:
        char = msvcrt.getch()

        # If Enter is pressed (carriage return)
        if char == b'\r':
            print()  # New line
            break

        # If Backspace is pressed
        elif char == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                # Move cursor back, print space, move cursor back again
                sys.stdout.write('\b \b')
                sys.stdout.flush()

        # If Escape is pressed, cancel
        elif char == b'\x1b':
            print("\nPassword input cancelled.")
            return None

        # If it's a printable character
        elif char >= b' ':
            password += char.decode('utf-8', errors='ignore')
            sys.stdout.write('*')
            sys.stdout.flush()

    return password

def _get_password_unix(prompt):
    """Unix/Linux implementation using termios"""
    if termios is None or tty is None:
        # Fallback to getpass if termios is not available
        return getpass.getpass(prompt)

    print(prompt, end='', flush=True)
    password = ""

    # Get the file descriptor for stdin
    fd = sys.stdin.fileno()

    # Save the original terminal settings
    old_settings = termios.tcgetattr(fd)

    try:
        # Set terminal to raw mode
        tty.setraw(fd)

        while True:
            char = sys.stdin.read(1)

            # If Enter is pressed
            if char == '\r' or char == '\n':
                print()  # New line
                break

            # If Backspace is pressed
            elif char == '\x7f' or char == '\b':
                if len(password) > 0:
                    password = password[:-1]
                    # Move cursor back, print space, move cursor back again
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()

            # If Escape is pressed, cancel
            elif char == '\x1b':
                print("\nPassword input cancelled.")
                return None

            # If it's a printable character
            elif ord(char) >= 32 and ord(char) <= 126:
                password += char
                sys.stdout.write('*')
                sys.stdout.flush()

    finally:
        # Restore the original terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password
