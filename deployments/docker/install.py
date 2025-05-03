#!/usr/bin/env python3
"""
Docker installation module for deployments.
Handles Docker-specific installation for deployments.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error

def install_docker(repo_path, version="latest"):
    """
    Install Docker dependencies for a Docker-based project.
    
    Args:
        repo_path (str): Path to the repository
        version (str): Docker version to install (default: "latest")
    """
    print_message("Setting up Docker deployment")
    
    # Check if Docker is installed
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_warning("Docker is not installed")
        print_instruction("Installing Docker first...")
        
        # Import and run Docker installation
        from install.docker import install_docker as install_docker_engine
        if not install_docker_engine():
            print_error("Failed to install Docker")
            print_instruction("Please install Docker manually and try again")
            return False
    
    # Check if docker-compose.yml exists
    if os.path.exists(os.path.join(repo_path, 'docker-compose.yml')):
        print_instruction("Found docker-compose.yml, checking Docker Compose")
        
        # Check if Docker Compose is installed
        try:
            subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.PIPE)
        except (subprocess.SubprocessError, FileNotFoundError):
            print_warning("Docker Compose not found, attempting to install")
            
            # Install Docker Compose
            try:
                subprocess.run([
                    "curl", "-L", "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)",
                    "-o", "/usr/local/bin/docker-compose"
                ], check=True, shell=True)
                
                subprocess.run(["chmod", "+x", "/usr/local/bin/docker-compose"], check=True)
                print_instruction("Docker Compose installed successfully")
            except subprocess.SubprocessError:
                print_error("Failed to install Docker Compose")
                print_instruction("Please install Docker Compose manually and try again")
                return False
    
    print_message("Docker deployment setup completed")
    return True
