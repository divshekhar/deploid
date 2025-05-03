#!/usr/bin/env python3
"""
Sudo installation module for Deploid.
Handles installation of sudo package.
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

def install_sudo():
    """Install sudo package based on the detected OS."""
    print_message("Installing sudo")
    
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
            print_instruction("Installing sudo using apt...")
            subprocess.run(["apt", "update", "-y"], check=False)
            subprocess.run(["apt", "install", "-y", "sudo"], check=False)
        
        elif distro_id in ['fedora', 'rhel', 'centos']:
            print_instruction("Installing sudo using dnf/yum...")
            if os.path.exists('/usr/bin/dnf'):
                subprocess.run(["dnf", "install", "-y", "sudo"], check=False)
            else:
                subprocess.run(["yum", "install", "-y", "sudo"], check=False)
        
        elif distro_id in ['arch', 'manjaro']:
            print_instruction("Installing sudo using pacman...")
            subprocess.run(["pacman", "-S", "--noconfirm", "sudo"], check=False)
        
        else:
            print_warning(f"Unsupported Linux distribution: {distro_id}")
            print_instruction("Please install sudo manually")
            return False
        
        # Add current user to sudo group
        username = os.getenv("SUDO_USER") or os.getenv("USER")
        if username:
            print_instruction(f"Adding user {username} to sudo group...")
            subprocess.run(["usermod", "-aG", "sudo", username], check=False)
        
        return True
    
    elif system == "Darwin":  # macOS
        print_instruction("sudo is already installed on macOS")
        return True
    
    elif system == "Windows":
        print_instruction("sudo is not applicable on Windows")
        return True
    
    else:
        print_warning(f"Unsupported operating system: {system}")
        print_instruction("Please install sudo manually if applicable")
        return False
