#!/usr/bin/env python3
"""
System module for Deploid.
Provides system-related functions.
"""

import os
import sys
import platform
import subprocess
from .colors import print_message, print_instruction, print_warning, print_error

def check_root():
    """
    Check if the script is running with root/admin privileges.
    
    Returns:
        bool: True if running as root/admin, False otherwise
    """
    if platform.system() == 'Windows':
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        return os.geteuid() == 0

def require_root():
    """
    Require root/admin privileges to run the script.
    Exits if not running as root/admin.
    """
    if not check_root():
        print_error("This script must be run as root or with sudo")
        print_instruction(f"Please run: sudo {sys.argv[0]}")
        sys.exit(1)

def setup_error_handling():
    """Setup error handling for the script."""
    # This is a placeholder for more complex error handling
    # In Python, we typically use try/except blocks instead
    pass

def get_os_info():
    """
    Get operating system information.
    
    Returns:
        dict: Dictionary containing OS information
    """
    system = platform.system()
    info = {
        'system': system,
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
    }
    
    if system == 'Linux':
        try:
            # Try to get distribution info
            import distro
            info['distribution'] = distro.name(pretty=True)
            info['distribution_id'] = distro.id()
        except ImportError:
            # Fallback if distro module is not available
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            info['distribution'] = line.split('=')[1].strip().strip('"')
                            break
            except:
                info['distribution'] = 'Unknown Linux'
    
    return info

def update_system():
    """Update the system packages based on the detected OS."""
    os_info = get_os_info()
    system = os_info['system']
    
    print_message(f"Updating system packages for {system}")
    
    if system == 'Linux':
        distro_id = os_info.get('distribution_id', '').lower()
        
        if distro_id in ['ubuntu', 'debian', 'linuxmint']:
            print_instruction("Updating apt packages...")
            subprocess.run(['apt', 'update', '-y'], check=False)
            subprocess.run(['apt', 'upgrade', '-y'], check=False)
        
        elif distro_id in ['fedora', 'rhel', 'centos']:
            print_instruction("Updating dnf/yum packages...")
            if os.path.exists('/usr/bin/dnf'):
                subprocess.run(['dnf', 'update', '-y'], check=False)
            else:
                subprocess.run(['yum', 'update', '-y'], check=False)
        
        elif distro_id in ['arch', 'manjaro']:
            print_instruction("Updating pacman packages...")
            subprocess.run(['pacman', '-Syu', '--noconfirm'], check=False)
        
        else:
            print_warning(f"Unsupported Linux distribution: {os_info.get('distribution', 'Unknown')}")
            print_instruction("Please update your system packages manually")
    
    elif system == 'Darwin':  # macOS
        print_instruction("Updating Homebrew packages...")
        # Check if Homebrew is installed
        if subprocess.run(['which', 'brew'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            subprocess.run(['brew', 'update'], check=False)
            subprocess.run(['brew', 'upgrade'], check=False)
        else:
            print_warning("Homebrew not found. Please install Homebrew or update packages manually")
    
    elif system == 'Windows':
        print_instruction("Windows package management is not directly supported")
        print_instruction("Please use Windows Update or a package manager like Chocolatey manually")
    
    else:
        print_warning(f"Unsupported operating system: {system}")
        print_instruction("Please update your system packages manually")
    
    print_message("System update completed")
