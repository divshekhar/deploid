#!/usr/bin/env python3
"""
Dependencies module for Deploid.
Handles checking and installing dependencies.
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

def check_dependency(command):
    """
    Check if a command is available.
    
    Args:
        command (str): Command to check
        
    Returns:
        bool: True if command is available, False otherwise
    """
    try:
        subprocess.run(
            ["which" if platform.system() != "Windows" else "where", command],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.SubprocessError:
        return False

def check_python_dependency(package):
    """
    Check if a Python package is installed.
    
    Args:
        package (str): Package name to check
        
    Returns:
        bool: True if package is installed, False otherwise
    """
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_python_dependency(package):
    """
    Install a Python package using pip.
    
    Args:
        package (str): Package name to install
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
        return True
    except subprocess.SubprocessError:
        return False

def install_system_dependency(dependency, system=None):
    """
    Install a system dependency based on the detected OS.
    
    Args:
        dependency (str): Dependency name to install
        system (str, optional): Override detected system. Defaults to None.
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    if system is None:
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
            print_instruction(f"Installing {dependency} using apt...")
            subprocess.run(["apt", "update", "-y"], check=False)
            subprocess.run(["apt", "install", "-y", dependency], check=False)
        
        elif distro_id in ['fedora', 'rhel', 'centos']:
            print_instruction(f"Installing {dependency} using dnf/yum...")
            if os.path.exists('/usr/bin/dnf'):
                subprocess.run(["dnf", "install", "-y", dependency], check=False)
            else:
                subprocess.run(["yum", "install", "-y", dependency], check=False)
        
        elif distro_id in ['arch', 'manjaro']:
            print_instruction(f"Installing {dependency} using pacman...")
            subprocess.run(["pacman", "-S", "--noconfirm", dependency], check=False)
        
        else:
            print_warning(f"Unsupported Linux distribution: {distro_id}")
            print_instruction(f"Please install {dependency} manually")
            return False
    
    elif system == "Darwin":  # macOS
        # Check if Homebrew is installed
        if subprocess.run(["which", "brew"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            print_instruction(f"Installing {dependency} using Homebrew...")
            subprocess.run(["brew", "install", dependency], check=False)
        else:
            print_warning("Homebrew not found")
            print_instruction(f"Please install Homebrew and then install {dependency} manually")
            return False
    
    elif system == "Windows":
        # Check if Chocolatey is installed
        if subprocess.run(["where", "choco"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            print_instruction(f"Installing {dependency} using Chocolatey...")
            subprocess.run(["choco", "install", "-y", dependency], check=False)
        else:
            print_warning("Chocolatey not found")
            print_instruction(f"Please install Chocolatey and then install {dependency} manually")
            return False
    
    else:
        print_warning(f"Unsupported operating system: {system}")
        print_instruction(f"Please install {dependency} manually")
        return False
    
    # Verify installation
    if check_dependency(dependency):
        print_instruction(f"{dependency} installed successfully")
        return True
    else:
        print_error(f"Failed to install {dependency}")
        return False

def check_required_dependencies(dependencies):
    """
    Check if required dependencies are installed.
    
    Args:
        dependencies (list): List of dependency names to check
        
    Returns:
        tuple: (bool, list) - Success status and list of missing dependencies
    """
    missing = []
    
    for dep in dependencies:
        if not check_dependency(dep):
            missing.append(dep)
    
    return len(missing) == 0, missing

def install_required_dependencies(dependencies):
    """
    Install required dependencies.
    
    Args:
        dependencies (list): List of dependency names to install
        
    Returns:
        bool: True if all dependencies were installed successfully, False otherwise
    """
    success = True
    
    for dep in dependencies:
        print_instruction(f"Installing {dep}...")
        if not install_system_dependency(dep):
            success = False
    
    return success
