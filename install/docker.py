#!/usr/bin/env python3
"""
Docker installation module for Deploid.
Handles installation of Docker.
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

def install_docker():
    """Install Docker based on the detected OS."""
    print_message("Installing Docker")
    
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
            print_instruction("Installing Docker using official Docker repository...")
            
            # Update package index
            subprocess.run(["apt", "update", "-y"], check=False)
            
            # Install packages to allow apt to use a repository over HTTPS
            subprocess.run([
                "apt", "install", "-y",
                "apt-transport-https",
                "ca-certificates",
                "curl",
                "gnupg",
                "lsb-release"
            ], check=False)
            
            # Add Docker's official GPG key
            subprocess.run([
                "curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg",
                "|", "gpg", "--dearmor", "-o", "/usr/share/keyrings/docker-archive-keyring.gpg"
            ], shell=True, check=False)
            
            # Set up the stable repository
            arch = subprocess.run(["dpkg", "--print-architecture"], 
                                 capture_output=True, text=True, check=True).stdout.strip()
            
            repo_cmd = f'echo "deb [arch={arch} signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/{distro_id} $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null'
            subprocess.run(repo_cmd, shell=True, check=False)
            
            # Update apt package index again
            subprocess.run(["apt", "update", "-y"], check=False)
            
            # Install Docker Engine
            subprocess.run(["apt", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"], check=False)
        
        elif distro_id in ['fedora', 'rhel', 'centos']:
            print_instruction("Installing Docker using official Docker repository...")
            
            # Install required packages
            if os.path.exists('/usr/bin/dnf'):
                subprocess.run(["dnf", "install", "-y", "dnf-plugins-core"], check=False)
                
                # Add Docker repository
                subprocess.run([
                    "dnf", "config-manager", "--add-repo",
                    "https://download.docker.com/linux/fedora/docker-ce.repo"
                ], check=False)
                
                # Install Docker Engine
                subprocess.run(["dnf", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"], check=False)
            else:
                subprocess.run(["yum", "install", "-y", "yum-utils"], check=False)
                
                # Add Docker repository
                subprocess.run([
                    "yum-config-manager", "--add-repo",
                    "https://download.docker.com/linux/centos/docker-ce.repo"
                ], check=False)
                
                # Install Docker Engine
                subprocess.run(["yum", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"], check=False)
        
        elif distro_id in ['arch', 'manjaro']:
            print_instruction("Installing Docker using pacman...")
            subprocess.run(["pacman", "-S", "--noconfirm", "docker"], check=False)
        
        else:
            print_warning(f"Unsupported Linux distribution: {distro_id}")
            print_instruction("Please install Docker manually")
            return False
        
        # Start and enable Docker service
        print_instruction("Starting Docker service...")
        subprocess.run(["systemctl", "start", "docker"], check=False)
        subprocess.run(["systemctl", "enable", "docker"], check=False)
        
        # Add current user to docker group
        username = os.getenv("SUDO_USER") or os.getenv("USER")
        if username:
            print_instruction(f"Adding user {username} to docker group...")
            subprocess.run(["usermod", "-aG", "docker", username], check=False)
            print_instruction("You may need to log out and log back in for this to take effect")
    
    elif system == "Darwin":  # macOS
        print_instruction("Please install Docker Desktop for Mac manually:")
        print_instruction("1. Download from https://www.docker.com/products/docker-desktop")
        print_instruction("2. Install the application")
        return False
    
    elif system == "Windows":
        print_instruction("Please install Docker Desktop for Windows manually:")
        print_instruction("1. Download from https://www.docker.com/products/docker-desktop")
        print_instruction("2. Install the application")
        return False
    
    else:
        print_warning(f"Unsupported operating system: {system}")
        print_instruction("Please install Docker manually")
        return False
    
    # Verify Docker installation
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        print_instruction(f"Docker installed successfully: {result.stdout.strip()}")
        return True
    except:
        print_error("Docker installation failed or Docker is not in PATH")
        return False
