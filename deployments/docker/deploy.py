#!/usr/bin/env python3
"""
Docker deployment module for Deploid.
Handles Docker-based deployments.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error

def deploy_docker(repo_path):
    """
    Deploy a Docker-based project.
    
    Args:
        repo_path (str): Path to the repository
    """
    print_message("Deploying Docker project")
    
    # Change to repository directory
    os.chdir(repo_path)
    
    # Check if docker-compose.yml exists
    if os.path.exists('docker-compose.yml'):
        print_instruction("Found docker-compose.yml, using Docker Compose")
        
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
        
        # Build and start containers
        print_instruction("Building and starting containers with Docker Compose")
        subprocess.run(["docker-compose", "up", "-d", "--build"], check=False)
        
        # Show running containers
        print_message("Docker Compose deployment completed")
        print_instruction("Running containers:")
        subprocess.run(["docker-compose", "ps"], check=False)
    
    else:
        print_instruction("No docker-compose.yml found, using Docker")
        
        # Check if Dockerfile exists
        if not os.path.exists('Dockerfile'):
            print_error("No Dockerfile found in the repository")
            print_instruction("Please create a Dockerfile and try again")
            return False
        
        # Get repository name for image tag
        repo_name = os.path.basename(repo_path)
        
        # Build Docker image
        print_instruction(f"Building Docker image: {repo_name}")
        subprocess.run(["docker", "build", "-t", repo_name, "."], check=False)
        
        # Ask if container should be run
        run_container = input("Do you want to run the container? (Y/n) ").lower()
        if run_container == 'y' or run_container == '':
            # Check if container is already running
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={repo_name}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            
            if repo_name in result.stdout:
                print_instruction(f"Container {repo_name} is already running")
                restart = input("Do you want to stop and restart it? (Y/n) ").lower()
                
                if restart == 'y' or restart == '':
                    print_instruction(f"Stopping container: {repo_name}")
                    subprocess.run(["docker", "stop", repo_name], check=False)
                    subprocess.run(["docker", "rm", repo_name], check=False)
                else:
                    return True
            
            # Get container ports
            ports = input("Enter port mappings (e.g., 8080:80 3000:3000): ")
            port_args = []
            
            if ports:
                for port_mapping in ports.split():
                    port_args.extend(["-p", port_mapping])
            
            # Get container environment variables
            env_vars = []
            add_env = input("Do you want to add environment variables? (Y/n) ").lower()
            
            if add_env == 'y' or add_env == '':
                print_instruction("Enter environment variables (one per line, format: KEY=VALUE)")
                print_instruction("Press Ctrl+D when done (Ctrl+Z then Enter on Windows)")
                
                env_input = sys.stdin.read().strip()
                for line in env_input.splitlines():
                    if '=' in line:
                        env_vars.extend(["-e", line])
            
            # Run container
            print_instruction(f"Running container: {repo_name}")
            
            cmd = ["docker", "run", "-d", "--name", repo_name]
            cmd.extend(port_args)
            cmd.extend(env_vars)
            cmd.append(repo_name)
            
            subprocess.run(cmd, check=False)
            
            # Show running container
            print_message("Docker deployment completed")
            print_instruction("Running container:")
            subprocess.run(["docker", "ps", "--filter", f"name={repo_name}"], check=False)
    
    return True
