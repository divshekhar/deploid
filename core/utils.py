#!/usr/bin/env python3
"""
Utils module for Deploid.
Provides utility functions for repository management and deployment.
"""

import os
import sys
import subprocess
import re
import json
from pathlib import Path
import getpass
from .colors import print_message, print_instruction, print_warning, print_error

def validate_repo(repo_path):
    """
    Validate if the given path is a git repository.
    
    Args:
        repo_path (str): Path to the repository
        
    Returns:
        bool: True if valid git repository, False otherwise
    """
    repo_path = Path(repo_path)
    
    if not repo_path.exists():
        print_error(f"Directory does not exist: {repo_path}")
        return False
    
    if not (repo_path / '.git').is_dir():
        print_error(f"Not a git repository: {repo_path}")
        return False
    
    return True

def get_deployment_type(repo_path=None):
    """
    Detect deployment type based on repository content.
    
    Args:
        repo_path (str, optional): Path to the repository. Defaults to current directory.
        
    Returns:
        str: Detected deployment type ('docker', 'node', 'python', or 'basic')
    """
    if repo_path is None:
        repo_path = os.getcwd()
    
    repo_path = Path(repo_path)
    
    # Check for Docker deployment
    if (repo_path / 'Dockerfile').exists() or list(repo_path.glob('Dockerfile*')):
        return "docker"
    
    # Check for Node.js deployment
    if (repo_path / 'package.json').exists():
        return "node"
    
    # Check for Python deployment
    if (repo_path / 'requirements.txt').exists() or (repo_path / 'setup.py').exists():
        return "python"
    
    # Default to basic deployment
    return "basic"

def get_required_version(deployment_type, repo_path=None):
    """
    Get required version for specific deployment type.
    
    Args:
        deployment_type (str): Type of deployment ('node', 'python', etc.)
        repo_path (str, optional): Path to the repository. Defaults to current directory.
        
    Returns:
        str: Required version for the deployment
    """
    if repo_path is None:
        repo_path = os.getcwd()
    
    repo_path = Path(repo_path)
    
    if deployment_type == "node":
        if (repo_path / 'package.json').exists():
            try:
                with open(repo_path / 'package.json', 'r') as f:
                    package_data = json.load(f)
                    if 'engines' in package_data and 'node' in package_data['engines']:
                        return package_data['engines']['node'].replace('^', '').replace('~', '')
            except (json.JSONDecodeError, FileNotFoundError):
                pass
            return "22"  # Default to Node.js 22
    
    elif deployment_type == "python":
        if (repo_path / 'runtime.txt').exists():
            try:
                with open(repo_path / 'runtime.txt', 'r') as f:
                    content = f.read().strip()
                    match = re.search(r'(\d+\.\d+)', content)
                    if match:
                        return match.group(1)
            except FileNotFoundError:
                pass
            return "3.11"  # Default to Python 3.11
    
    # Return default version if not found
    return "latest"

def setup_repository():
    """
    Handle repository setup process.
    
    Returns:
        str: Path to the cloned repository
    """
    print_message("Repository Access")
    repo_url = ""
    
    # Check if private repository
    while True:
        is_private = input("Is this a private repository? (Y/n) ").lower()
        if is_private in ['y', 'n']:
            break
        else:
            print_instruction("Please enter Y or n")
    
    if is_private == 'y':
        setup_ssh_key()
        repo_url = input("Enter the GitHub repository SSH URL (git@github.com:username/repo.git): ")
    else:
        repo_url = input("Enter the GitHub repository HTTPS URL (https://github.com/username/repo.git): ")
    
    return clone_repository(repo_url)

def setup_ssh_key():
    """Setup SSH key for GitHub access."""
    print_message("Checking SSH configuration")
    ssh_key_path = Path.home() / '.ssh' / 'id_rsa'
    
    if not ssh_key_path.exists():
        print_instruction("No SSH key found. Creating new SSH key...")
        subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-f', str(ssh_key_path), '-N', ''])
        
        print_message("GitHub SSH Key Setup")
        print("Here's your public SSH key:")
        print("----------------------------------------------------------------")
        with open(f"{ssh_key_path}.pub", 'r') as f:
            print(f.read())
        print("----------------------------------------------------------------")
        
        print_instruction("1. Copy the above public key")
        print_instruction("2. Go to GitHub -> Settings -> SSH and GPG keys -> New SSH key")
        print_instruction("3. Paste the key and save")
        
        while True:
            response = input("Have you added the SSH key to GitHub? (Y/n) ").lower()
            if response == 'y':
                break
            else:
                print_instruction("Please add the SSH key to GitHub before continuing")
    else:
        print_instruction("Existing SSH key found")
    
    print_message("Testing GitHub connection")
    subprocess.run(['ssh', '-T', 'git@github.com', '-o', 'StrictHostKeyChecking=no'], 
                  stderr=subprocess.STDOUT)

def clone_repository(repo_url):
    """
    Clone a git repository.
    
    Args:
        repo_url (str): URL of the repository to clone
        
    Returns:
        str: Path to the cloned repository
    """
    print_message("Clone Directory Setup")
    current_dir = os.getcwd()
    print_instruction(f"Current directory: {current_dir}")
    
    clone_dir = input("Where would you like to clone the repository? (Press Enter for current directory or provide path): ")
    clone_dir = clone_dir or current_dir
    clone_dir = os.path.expanduser(clone_dir)
    
    if not os.path.exists(clone_dir):
        print_instruction(f"Creating directory: {clone_dir}")
        os.makedirs(clone_dir)
    
    os.chdir(clone_dir)
    print_instruction(f"Using directory: {os.getcwd()}")
    
    repo_name = os.path.basename(repo_url)
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]
    
    if os.path.exists(repo_name):
        print_instruction(f"Repository {repo_name} already exists in {os.path.join(os.getcwd(), repo_name)}")
        reclone = input("Do you want to remove it and clone again? (Y/n) ").lower()
        
        if reclone == 'y':
            import shutil
            shutil.rmtree(repo_name)
            subprocess.run(['git', 'clone', repo_url])
    else:
        subprocess.run(['git', 'clone', repo_url])
    
    return os.path.join(clone_dir, repo_name)

def setup_env_file(repo_path):
    """
    Setup environment file for the repository.
    
    Args:
        repo_path (str): Path to the repository
    """
    print_message("Checking environment file")
    env_file = os.path.join(repo_path, '.env')
    
    if not os.path.exists(env_file):
        create_env = input("No .env file found. Would you like to create one? (Y/n): ").lower()
        
        if create_env == 'y':
            print_message("Please paste your .env content (press Ctrl+D when done):")
            env_content = sys.stdin.read()
            
            with open(env_file, 'w') as f:
                f.write(env_content)
        else:
            print_warning("Proceeding without .env file")
    
    elif os.path.getsize(env_file) == 0:
        print_warning(".env file is empty")
        proceed_empty = input("Do you want to proceed with empty .env? (Y/n): ").lower()
        
        if proceed_empty != 'y':
            print_message("Please paste your .env content (press Ctrl+D when done):")
            env_content = sys.stdin.read()
            
            with open(env_file, 'w') as f:
                f.write(env_content)

def detect_submodules(repo_path):
    """
    Detect if repository has submodules.
    
    Args:
        repo_path (str): Path to the repository
        
    Returns:
        bool: True if repository has submodules, False otherwise
    """
    return os.path.exists(os.path.join(repo_path, '.gitmodules'))

def update_submodules(repo_path, specific_module=None):
    """
    Update git submodules with enhanced error handling.
    
    Args:
        repo_path (str): Path to the repository
        specific_module (str, optional): Specific submodule to update. Defaults to None.
        
    Returns:
        bool: True if successful, False otherwise
    """
    if os.path.exists(os.path.join(repo_path, '.gitmodules')):
        print_message("Updating submodules")
        
        # Save current directory
        original_dir = os.getcwd()
        os.chdir(repo_path)
        
        try:
            # Initialize submodules if not already initialized
            result = subprocess.run(['git', 'submodule', 'init'], 
                                   check=True, capture_output=True)
            if result.returncode != 0:
                print_warning("Failed to initialize submodules")
                os.chdir(original_dir)
                return False
            
            # Fetch updates for all submodules
            result = subprocess.run(['git', 'fetch', '--recurse-submodules'], 
                                   check=True, capture_output=True)
            if result.returncode != 0:
                print_warning("Failed to fetch submodule updates")
                os.chdir(original_dir)
                return False
            
            if specific_module:
                # Update specific submodule
                module_path = os.path.join(repo_path, specific_module)
                os.chdir(module_path)
                
                try:
                    subprocess.run(['git', 'checkout', 'master'], 
                                  check=False, capture_output=True)
                    result = subprocess.run(['git', 'pull', 'origin', 'master'], 
                                           check=True, capture_output=True)
                    if result.returncode != 0:
                        print_warning(f"Failed to update specific submodule: {specific_module}")
                        os.chdir(original_dir)
                        return False
                finally:
                    os.chdir(repo_path)
            else:
                # Update all submodules
                try:
                    result = subprocess.run(['git', 'submodule', 'update', '--init', '--recursive', '--force'], 
                                           check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    print_warning("Some submodules might be out of sync, attempting alternative update")
                    subprocess.run(['git', 'submodule', 'foreach', 'git', 'checkout', 'master'], 
                                  check=False, capture_output=True)
                    subprocess.run(['git', 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'], 
                                  check=False, capture_output=True)
            
            print_message("Submodule update completed")
            os.chdir(original_dir)
            return True
            
        except Exception as e:
            print_error(f"Error updating submodules: {str(e)}")
            os.chdir(original_dir)
            return False
    
    return True
