#!/usr/bin/env python3
"""
Update script for Deploid.
Handles updating and deploying projects.
"""

import os
import sys
import importlib.util
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.colors import print_message, print_instruction, print_error, print_warning
from core.utils import validate_repo, get_deployment_type, update_submodules

def run_update():
    """Run the update process for Deploid."""
    print_message("Deploid Update")
    
    # Get repository path
    current_dir = os.getcwd()
    print_instruction(f"Current directory: {current_dir}")
    
    repo_path = input("Enter the path to your repository (press Enter for current directory): ")
    repo_path = repo_path or current_dir
    repo_path = os.path.expanduser(repo_path)
    
    # Validate repository
    if not validate_repo(repo_path):
        print_error(f"Invalid repository path: {repo_path}")
        return
    
    # Update repository
    print_message("Updating repository")
    os.chdir(repo_path)
    
    import subprocess
    try:
        # Fetch latest changes
        subprocess.run(["git", "fetch", "--all"], check=True)
        
        # Get current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = result.stdout.strip()
        
        # Pull latest changes
        print_instruction(f"Pulling latest changes from {current_branch}")
        subprocess.run(["git", "pull", "origin", current_branch], check=True)
        
        # Update submodules if present
        if os.path.exists(os.path.join(repo_path, ".gitmodules")):
            print_instruction("Updating submodules")
            update_submodules(repo_path)
    
    except subprocess.SubprocessError as e:
        print_error(f"Failed to update repository: {str(e)}")
        return
    
    # Get deployment type
    deployment_type = get_deployment_type(repo_path)
    print_message(f"Detected deployment type: {deployment_type}")
    
    # Source deployment-specific deploy script
    script_dir = Path(__file__).parent.absolute()
    deploy_module_path = script_dir / "deployments" / deployment_type / "deploy.py"
    
    if deploy_module_path.exists():
        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(
            f"deployments.{deployment_type}.deploy", 
            deploy_module_path
        )
        deploy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(deploy_module)
        
        # Check if the deployment function exists
        deploy_func_name = f"deploy_{deployment_type}"
        if hasattr(deploy_module, deploy_func_name):
            deploy_func = getattr(deploy_module, deploy_func_name)
            deploy_func(repo_path)
        else:
            print_error(f"Deployment function not found for {deployment_type}")
            return
    else:
        print_error(f"Deployment script not found for {deployment_type}")
        return
    
    print_message("Update completed successfully!")

if __name__ == "__main__":
    run_update()
