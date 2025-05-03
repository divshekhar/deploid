#!/usr/bin/env python3
"""
Node.js utilities module for deployments.
Provides utility functions for Node.js deployments.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error

def get_node_version():
    """
    Get Node.js version.
    
    Returns:
        str: Node.js version or None if Node.js is not available
    """
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return None

def get_npm_version():
    """
    Get npm version.
    
    Returns:
        str: npm version or None if npm is not available
    """
    try:
        result = subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return None

def install_node_dependencies(repo_path):
    """
    Install Node.js dependencies.
    
    Args:
        repo_path (str): Path to the repository with package.json
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print_instruction("Installing Node.js dependencies...")
        subprocess.run(["npm", "install"], cwd=repo_path, check=True)
        return True
    except subprocess.SubprocessError:
        print_error("Failed to install Node.js dependencies")
        return False

def build_node_project(repo_path):
    """
    Build Node.js project.
    
    Args:
        repo_path (str): Path to the repository with package.json
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if build script exists in package.json
        package_json_path = os.path.join(repo_path, 'package.json')
        
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            if 'scripts' in package_data and 'build' in package_data['scripts']:
                print_instruction("Building Node.js project...")
                subprocess.run(["npm", "run", "build"], cwd=repo_path, check=True)
                return True
            else:
                print_instruction("No build script found in package.json")
                return True
        else:
            print_warning("No package.json found")
            return False
    except (subprocess.SubprocessError, json.JSONDecodeError):
        print_error("Failed to build Node.js project")
        return False

def start_node_project(repo_path):
    """
    Start Node.js project.
    
    Args:
        repo_path (str): Path to the repository with package.json
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if start script exists in package.json
        package_json_path = os.path.join(repo_path, 'package.json')
        
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            if 'scripts' in package_data and 'start' in package_data['scripts']:
                print_instruction("Starting Node.js project...")
                
                # Ask if should run in background
                background = input("Run in background? (Y/n) ").lower()
                
                if background == 'y' or background == '':
                    # Run in background with nohup
                    subprocess.Popen(
                        ["nohup", "npm", "run", "start"],
                        cwd=repo_path,
                        stdout=open(os.path.join(repo_path, 'nohup.out'), 'w'),
                        stderr=subprocess.STDOUT,
                        preexec_fn=os.setpgrp
                    )
                    print_instruction("Node.js project started in background")
                    print_instruction(f"Check logs at: {os.path.join(repo_path, 'nohup.out')}")
                else:
                    # Run in foreground
                    subprocess.run(["npm", "run", "start"], cwd=repo_path, check=True)
                
                return True
            else:
                print_warning("No start script found in package.json")
                return False
        else:
            print_warning("No package.json found")
            return False
    except subprocess.SubprocessError:
        print_error("Failed to start Node.js project")
        return False
