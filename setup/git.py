#!/usr/bin/env python3
"""
Git setup module for Deploid.
Handles Git configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning

def setup_git_config():
    """Setup Git global configuration."""
    print_message("Setting up Git configuration")
    
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_warning("Git is not installed. Please install Git first.")
        print_instruction("You can install Git by running: python deploid.py and selecting 'Install' > 'Git'")
        return False
    
    # Get user name and email
    name = input("Enter your name for Git commits: ")
    email = input("Enter your email for Git commits: ")
    
    # Set Git configuration
    if name:
        subprocess.run(["git", "config", "--global", "user.name", name])
    
    if email:
        subprocess.run(["git", "config", "--global", "user.email", email])
    
    # Set default branch name
    subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])
    
    # Set pull strategy
    subprocess.run(["git", "config", "--global", "pull.rebase", "false"])
    
    # Display Git configuration
    print_message("Git configuration completed")
    print_instruction("Current Git configuration:")
    
    result = subprocess.run(
        ["git", "config", "--global", "--list"],
        capture_output=True,
        text=True,
        check=True
    )
    
    for line in result.stdout.splitlines():
        print(f"  {line}")
    
    return True
