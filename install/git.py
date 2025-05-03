#!/usr/bin/env python3
"""
Git installation module for Deploid.
Handles installation of Git.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error

def install_git():
    """Install Git based on the detected OS."""
    print_message("Installing Git")
    
    system = platform.system()
    
    if system == "Linux":
        # Detect Linux distribution
        try:
            import distro
            distro_id = distro.id().lower()
        except ImportError:
            # Fallback if distro module is not available
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('ID='):
                            distro_id = line.split('=')[1].strip().strip('"').lower()
                            break
                    else:
                        distro_id = ""
            except:
                distro_id = ""
        
        if distro_id in ['ubuntu', 'debian', 'linuxmint']:
            print_instruction("Installing Git using apt...")
            subprocess.run(["apt", "update", "-y"], check=False)
            subprocess.run(["apt", "install", "-y", "git"], check=False)
        
        elif distro_id in ['fedora', 'rhel', 'centos']:
            print_instruction("Installing Git using dnf/yum...")
            if os.path.exists('/usr/bin/dnf'):
                subprocess.run(["dnf", "install", "-y", "git"], check=False)
            else:
                subprocess.run(["yum", "install", "-y", "git"], check=False)
        
        elif distro_id in ['arch', 'manjaro']:
            print_instruction("Installing Git using pacman...")
            subprocess.run(["pacman", "-S", "--noconfirm", "git"], check=False)
        
        else:
            print_warning(f"Unsupported Linux distribution: {distro_id}")
            print_instruction("Please install Git manually")
            return False
    
    elif system == "Darwin":  # macOS
        # Check if Homebrew is installed
        if subprocess.run(["which", "brew"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            print_instruction("Installing Git using Homebrew...")
            subprocess.run(["brew", "install", "git"], check=False)
        else:
            print_warning("Homebrew not found")
            print_instruction("Installing Homebrew first...")
            
            # Install Homebrew
            homebrew_install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(homebrew_install_cmd, shell=True, check=False)
            
            # Try installing Git again
            print_instruction("Installing Git using Homebrew...")
            subprocess.run(["brew", "install", "git"], check=False)
    
    elif system == "Windows":
        print_instruction("Please install Git for Windows manually:")
        print_instruction("1. Download from https://git-scm.com/download/win")
        print_instruction("2. Run the installer and follow the instructions")
        return False
    
    else:
        print_warning(f"Unsupported operating system: {system}")
        print_instruction("Please install Git manually")
        return False
    
    # Verify Git installation
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        print_instruction(f"Git installed successfully: {result.stdout.strip()}")
        return True
    except:
        print_error("Git installation failed or Git is not in PATH")
        return False
