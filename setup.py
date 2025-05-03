#!/usr/bin/env python3
"""
Setup script for Deploid.
Handles repository setup and deployment configuration.
"""

import os
import sys
import importlib.util
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.colors import print_message, print_instruction, print_error, print_warning
from core.system import setup_error_handling, update_system
from core.utils import (
    setup_repository, get_deployment_type, get_required_version,
    setup_env_file, detect_submodules, update_submodules
)

def run_setup():
    """Run the setup process for Deploid."""
    # Setup error handling
    setup_error_handling()
    
    # Update system
    update_system()
    
    # Setup repository
    repo_path = setup_repository()
    
    # Get deployment type
    deployment_type = get_deployment_type(repo_path)
    required_version = get_required_version(deployment_type, repo_path)
    
    # Source deployment-specific install script
    script_dir = Path(__file__).parent.absolute()
    install_module_path = script_dir / "deployments" / deployment_type / "install.py"
    
    if install_module_path.exists():
        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(
            f"deployments.{deployment_type}.install", 
            install_module_path
        )
        install_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(install_module)
        
        # Check if the installation function exists
        install_func_name = f"install_{deployment_type}"
        if hasattr(install_module, install_func_name):
            install_func = getattr(install_module, install_func_name)
            install_func(repo_path, required_version)
        else:
            print_error(f"Installation function not found for {deployment_type}")
            sys.exit(1)
    else:
        print_error(f"Installation script not found for {deployment_type}")
        sys.exit(1)
    
    # Setup environment file
    setup_env_file(repo_path)
    
    # Handle submodules if present
    if detect_submodules(repo_path):
        print_message("Submodule Management")
        print("1. Update all submodules")
        print("2. Update specific submodule")
        print("3. Skip submodule updates")
        
        sub_choice = input("Choose an option (1-3): ")
        
        if sub_choice == "1":
            update_submodules(repo_path)
        elif sub_choice == "2":
            # Get list of submodules
            import subprocess
            result = subprocess.run(
                ["git", "submodule", "status"], 
                cwd=repo_path,
                capture_output=True, 
                text=True,
                check=True
            )
            
            # Display submodules
            submodules = []
            for line in result.stdout.splitlines():
                parts = line.strip().split()
                if len(parts) >= 2:
                    submodule_path = parts[1]
                    submodules.append(submodule_path)
                    print(f"- {submodule_path}")
            
            # Get user choice
            submodule_path = input("Enter submodule path: ")
            if submodule_path in submodules:
                update_submodules(repo_path, submodule_path)
            else:
                print_warning(f"Invalid submodule path: {submodule_path}")
        elif sub_choice == "3":
            print_instruction("Skipping submodule updates")
        else:
            print_warning("Invalid choice, skipping submodule updates")
    
    # Final instructions
    print_message("Setup completed successfully!")
    print()
    print_instruction("Next steps:")
    print_instruction(f"1. cd into your repository: cd {repo_path}")
    print_instruction("2. Review your .env file if needed")
    print_instruction("3. Run python update.py to build and start the project")
    print()
    print_instruction("Note: You may need to log out and log back in for some permission changes to take effect")

if __name__ == "__main__":
    run_setup()
