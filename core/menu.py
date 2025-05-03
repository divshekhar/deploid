#!/usr/bin/env python3
"""
Menu module for Deploid.
Provides interactive menu functionality with arrow key navigation.
"""

import os
import sys
import time
import readchar
from .colors import print_message, BLUE, RESET, GREEN, YELLOW

class Menu:
    """Interactive menu class for Deploid."""

    def __init__(self):
        """Initialize the menu system."""
        self.breadcrumb = "Deploid"

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print the application header."""
        self.clear_screen()
        print_message("Welcome to Deploid! Your AI Buddy for Quick and Easy Deployment!")
        print()

        # Show navigation breadcrumb if it exists
        if self.breadcrumb:
            print(f"{BLUE}{self.breadcrumb}{RESET}")
            print()

    def select_option(self, options, title):
        """
        Display an interactive menu with arrow key navigation and get user selection.

        Args:
            options (list): List of menu options
            title (str): Menu title

        Returns:
            int: Selected option index or special code
        """
        # Add Back/Exit options based on breadcrumb
        if self.breadcrumb == "Deploid":
            display_options = options + ["Exit"]
        else:
            display_options = options + ["Back", "Exit"]

        selected_index = 0

        while True:
            # Clear screen and print header
            self.print_header()
            print(title)
            print()

            # Display menu options with highlighting for the selected option
            for i, option in enumerate(display_options):
                if i == selected_index:
                    print(f"{GREEN}▶ {option}{RESET}")
                else:
                    print(f"  {option}")

            # Display navigation instructions
            print()
            print(f"{YELLOW}Navigation: {RESET}↑/↓ or j/k to move, Enter to select, Esc to exit")

            # Wait for key press
            key = readchar.readkey()

            # Handle arrow keys and enter
            if key == readchar.key.UP or key == 'k':
                selected_index = (selected_index - 1) % len(display_options)
            elif key == readchar.key.DOWN or key == 'j':
                selected_index = (selected_index + 1) % len(display_options)
            elif key == readchar.key.ENTER:
                selected = display_options[selected_index]

                if selected == "Exit":
                    self.clear_screen()
                    sys.exit(0)
                elif selected == "Back":
                    return 255  # Special return code for Back
                else:
                    return selected_index
            elif key == readchar.key.CTRL_C or key == readchar.key.ESC:
                self.clear_screen()
                sys.exit(0)

    def show_menu(self, title, *options):
        """
        Helper function to display menu and get selection.

        Args:
            title (str): Menu title
            *options: Variable list of menu options

        Returns:
            int: Selected option index
        """
        return self.select_option(list(options), title)

    def update_breadcrumb(self, new_item):
        """
        Update the breadcrumb trail.

        Args:
            new_item (str): New breadcrumb item to add
        """
        if self.breadcrumb == "Deploid":
            self.breadcrumb = f"Deploid > {new_item}"
        else:
            self.breadcrumb = f"{self.breadcrumb} > {new_item}"

    def remove_last_breadcrumb(self):
        """Remove the last item from the breadcrumb trail."""
        if self.breadcrumb != "Deploid":
            # Remove everything after and including the last ">"
            parts = self.breadcrumb.split(" > ")
            if len(parts) > 1:
                self.breadcrumb = " > ".join(parts[:-1])
            else:
                self.breadcrumb = "Deploid"
