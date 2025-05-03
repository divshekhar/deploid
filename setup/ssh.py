#!/usr/bin/env python3
"""
SSH setup module for Deploid.
Handles SSH key generation and configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning

def setup_github_ssh():
    """Setup SSH key for GitHub access."""
    print_message("Setting up SSH for GitHub")
    
    # Check for existing SSH key
    ssh_dir = Path.home() / ".ssh"
    ssh_key_path = ssh_dir / "id_rsa"
    
    if not ssh_dir.exists():
        print_instruction("Creating .ssh directory")
        ssh_dir.mkdir(mode=0o700)
    
    if not ssh_key_path.exists():
        print_instruction("No SSH key found. Creating new SSH key...")
        
        # Get user email for SSH key
        email = input("Enter your GitHub email address: ")
        
        # Generate SSH key
        subprocess.run([
            "ssh-keygen", 
            "-t", "rsa", 
            "-b", "4096", 
            "-C", email, 
            "-f", str(ssh_key_path),
            "-N", ""  # Empty passphrase
        ])
        
        # Start SSH agent
        print_instruction("Starting SSH agent")
        subprocess.run(["eval", "$(ssh-agent -s)"], shell=True)
        
        # Add key to SSH agent
        print_instruction("Adding key to SSH agent")
        subprocess.run(["ssh-add", str(ssh_key_path)])
        
        # Display public key
        print_message("GitHub SSH Key Setup")
        print("Here's your public SSH key:")
        print("----------------------------------------------------------------")
        with open(f"{ssh_key_path}.pub", "r") as f:
            public_key = f.read().strip()
            print(public_key)
        print("----------------------------------------------------------------")
        
        print_instruction("1. Copy the above public key")
        print_instruction("2. Go to GitHub -> Settings -> SSH and GPG keys -> New SSH key")
        print_instruction("3. Paste the key and save")
        
        # Ask user to confirm key has been added to GitHub
        while True:
            response = input("Have you added the SSH key to GitHub? (Y/n) ").lower()
            if response == "y" or response == "":
                break
            else:
                print_instruction("Please add the SSH key to GitHub before continuing")
    else:
        print_instruction("Existing SSH key found")
    
    # Test GitHub connection
    print_message("Testing GitHub connection")
    result = subprocess.run(
        ["ssh", "-T", "git@github.com", "-o", "StrictHostKeyChecking=no"],
        capture_output=True,
        text=True
    )
    
    # Check if connection was successful
    if "successfully authenticated" in result.stderr:
        print_instruction("GitHub connection successful!")
    else:
        print_warning("GitHub connection test returned: " + result.stderr.strip())
        print_instruction("This might be normal if this is your first connection to GitHub")
    
    return True
