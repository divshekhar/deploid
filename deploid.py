#!/usr/bin/env python3
"""
Deploid - Your AI Buddy for Quick and Easy Deployment!
Main entry point for the Deploid application.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.colors import print_message, print_instruction, print_error
from core.menu import Menu
from core.utils import setup_repository, setup_env_file, detect_submodules, update_submodules
from core.system import require_root, get_os_info, update_system

# Import setup modules
from setup.ssh import setup_github_ssh

# Global menu instance
menu = Menu()

def handle_install_menu():
    """Handle the installation menu options."""
    menu.update_breadcrumb("Install")
    main_dir = Path(__file__).parent.absolute()
    
    choice = menu.show_menu("What do you want to install?", "Sudo", "Git", "Docker", "OpenSSH")
    
    if choice == 255:  # Back
        menu.remove_last_breadcrumb()
        return
    
    if choice == 0:  # Sudo
        menu.update_breadcrumb("Sudo")
        menu.show_menu("Installing Sudo", "Continue")
        
        # Import and run sudo installation
        from install.sudo import install_sudo
        install_sudo()
        
        # Get sudo version
        try:
            result = subprocess.run(['sudo', '-V'], capture_output=True, text=True, check=True)
            sudo_version = result.stdout.splitlines()[0]
        except:
            sudo_version = "unknown"
        
        print_message(f"Yayy! Sudo is installed! ({sudo_version})")
        print()
        print_instruction("Next steps:")
        print_instruction("1. You may need to log out and log back in for sudo permissions to take effect")
        print_instruction("2. Run ./deploid.py again to install other tools or proceed with setup")
        print()
        input("Press Enter to exit...")
        sys.exit(0)
    
    elif choice == 1:  # Git
        menu.update_breadcrumb("Git")
        menu.show_menu("Installing Git", "Continue")
        
        # Import and run git installation
        from install.git import install_git
        install_git()
        
        # Get git version
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
            git_version = result.stdout.strip()
        except:
            git_version = "unknown"
        
        print_message(f"Yayy! Git is installed! ({git_version})")
        print()
        print_instruction("Next steps:")
        print_instruction("1. Run ./deploid.py and choose 'Setup' > 'Git + SSH' to configure Git")
        print_instruction("2. Or install other tools by running ./deploid.py again")
        print()
        input("Press Enter to exit...")
        sys.exit(0)
    
    elif choice == 2:  # Docker
        menu.update_breadcrumb("Docker")
        menu.show_menu("Installing Docker", "Continue")
        
        # Import and run docker installation
        from install.docker import install_docker
        install_docker()
        
        # Get docker version
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, check=True)
            docker_version = result.stdout.strip()
        except:
            docker_version = "unknown"
        
        print_message(f"Yayy! Docker is installed! ({docker_version})")
        print()
        print_instruction("Next steps:")
        print_instruction("1. Log out and log back in for Docker permissions to take effect")
        print_instruction("2. Run ./deploid.py and choose 'Setup' > 'Docker' to configure your Docker environment")
        print_instruction("3. Or install other tools by running ./deploid.py again")
        print()
        input("Press Enter to exit...")
        sys.exit(0)
    
    elif choice == 3:  # OpenSSH
        menu.update_breadcrumb("OpenSSH")
        menu.show_menu("Installing OpenSSH", "Continue")
        
        # Import and run openssh installation
        from install.openssh import install_openssh
        install_openssh()
        
        # Get ssh version
        try:
            result = subprocess.run(['ssh', '-V'], capture_output=True, text=True, stderr=subprocess.STDOUT, check=True)
            ssh_version = result.stdout.strip()
        except:
            ssh_version = "unknown"
        
        print_message(f"Yayy! OpenSSH is installed! ({ssh_version})")
        print()
        print_instruction("Next steps:")
        print_instruction("1. Run ./deploid.py and choose 'Setup' > 'SSH' to configure SSH keys")
        print_instruction("2. Or install other tools by running ./deploid.py again")
        print()
        input("Press Enter to exit...")
        sys.exit(0)

def handle_ssh_setup_menu():
    """Handle SSH setup menu options."""
    choice = menu.show_menu("Setup SSH for:", "GitHub")
    
    if choice == 255:  # Back
        return
    
    if choice == 0:  # GitHub
        menu.update_breadcrumb("GitHub")
        menu.show_menu("GitHub SSH Setup", "Continue")
        
        # Run GitHub SSH setup
        setup_github_ssh()
        
        print_message("GitHub SSH setup completed!")
        print()
        input("Press Enter to continue...")
        menu.remove_last_breadcrumb()
        sys.exit(0)

def handle_setup_menu():
    """Handle setup menu options."""
    menu.update_breadcrumb("Setup")
    
    while True:
        choice = menu.show_menu("What kind of setup do you want?", "SSH")
        
        if choice == 255:  # Back
            menu.remove_last_breadcrumb()
            return
        
        if choice == 0:  # SSH
            menu.update_breadcrumb("SSH")
            handle_ssh_setup_menu()
            menu.remove_last_breadcrumb()
        else:
            print_error("Invalid choice")

def handle_update_menu():
    """Handle update menu options."""
    menu.update_breadcrumb("Update")
    menu.show_menu("Update Setup", "Continue")
    
    # Import and run update script
    from update import run_update
    run_update()
    
    menu.remove_last_breadcrumb()

def main():
    """Main function to run the Deploid application."""
    # Check if running as root
    require_root()
    
    # Main menu loop
    while True:
        choice = menu.show_menu("What do you want to perform?", "Install", "Setup", "Update")
        
        # Handle Back/Exit
        if choice == 255:  # Back or Exit from main menu
            menu.clear_screen()
            sys.exit(0)
        
        if choice == 0:  # Install
            handle_install_menu()
        elif choice == 1:  # Setup
            handle_setup_menu()
        elif choice == 2:  # Update
            handle_update_menu()

if __name__ == "__main__":
    main()
