#!/usr/bin/env python3
"""
Test runner for Deploid.
Runs the Deploid application without requiring root privileges for testing.
Can be run both inside and outside of Docker.
"""

import os
import sys
import importlib.util
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error
from core.menu import Menu

# Check if running in Docker
def is_running_in_docker():
    """
    Check if the script is running inside a Docker container.

    Returns:
        bool: True if running in Docker, False otherwise
    """
    # Check for .dockerenv file
    if os.path.exists('/.dockerenv'):
        return True

    # Check for cgroup
    try:
        with open('/proc/1/cgroup', 'r') as f:
            return 'docker' in f.read()
    except:
        pass

    return False

# Monkey patch the require_root function to bypass the root check
import core.system
core.system.require_root = lambda: None

# Import the main module
import deploid

def main():
    """Run the Deploid application in test mode."""
    if is_running_in_docker():
        print_message("Running Deploid in DOCKER TEST MODE")
        print_instruction("Using globally installed Python packages")
    else:
        print_message("Running Deploid in TEST MODE")

    print_warning("Root privileges check bypassed for testing")
    print_instruction("Some features may not work without actual root privileges")
    print()

    # Run the main function from deploid.py
    deploid.main()

if __name__ == "__main__":
    main()
