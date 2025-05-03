#!/usr/bin/env python3
"""
Colors module for Deploid.
Provides color formatting for terminal output.
"""

from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Color definitions
GREEN = Fore.GREEN
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL

def print_message(message):
    """Print a highlighted message."""
    print(f"{GREEN}=== {message} ==={RESET}")

def print_instruction(message):
    """Print an instruction message."""
    print(f"{BLUE}>>> {message}{RESET}")

def print_warning(message):
    """Print a warning message."""
    print(f"{YELLOW}WARNING: {message}{RESET}")

def print_error(message):
    """Print an error message."""
    print(f"{RED}ERROR: {message}{RESET}")
