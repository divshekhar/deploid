#!/usr/bin/env python3
"""
OpenSSH installation module for Deploid.
Handles installation of OpenSSH client and server.
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

def install_openssh():
    """Install OpenSSH based on the detected OS."""
    print_message("Installing OpenSSH")
    
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
            print_instruction("Installing OpenSSH using apt...")
            subprocess.run(["apt", "update", "-y"], check=False)
            
            # Install SSH client and server
            print_instruction("Installing OpenSSH client...")
            subprocess.run(["apt", "install", "-y", "openssh-client"], check=False)
            
            # Ask if server should be installed
            install_server = input("Do you want to install OpenSSH server? (Y/n) ").lower()
            if install_server == 'y' or install_server == '':
                print_instruction("Installing OpenSSH server...")
                subprocess.run(["apt", "install", "-y", "openssh-server"], check=False)
                
                # Start and enable SSH service
                print_instruction("Starting SSH service...")
                subprocess.run(["systemctl", "start", "ssh"], check=False)
                subprocess.run(["systemctl", "enable", "ssh"], check=False)
        
        elif distro_id in ['fedora', 'rhel', 'centos']:
            print_instruction("Installing OpenSSH using dnf/yum...")
            
            # Install SSH client and server
            if os.path.exists('/usr/bin/dnf'):
                print_instruction("Installing OpenSSH client...")
                subprocess.run(["dnf", "install", "-y", "openssh-clients"], check=False)
                
                # Ask if server should be installed
                install_server = input("Do you want to install OpenSSH server? (Y/n) ").lower()
                if install_server == 'y' or install_server == '':
                    print_instruction("Installing OpenSSH server...")
                    subprocess.run(["dnf", "install", "-y", "openssh-server"], check=False)
                    
                    # Start and enable SSH service
                    print_instruction("Starting SSH service...")
                    subprocess.run(["systemctl", "start", "sshd"], check=False)
                    subprocess.run(["systemctl", "enable", "sshd"], check=False)
            else:
                print_instruction("Installing OpenSSH client...")
                subprocess.run(["yum", "install", "-y", "openssh-clients"], check=False)
                
                # Ask if server should be installed
                install_server = input("Do you want to install OpenSSH server? (Y/n) ").lower()
                if install_server == 'y' or install_server == '':
                    print_instruction("Installing OpenSSH server...")
                    subprocess.run(["yum", "install", "-y", "openssh-server"], check=False)
                    
                    # Start and enable SSH service
                    print_instruction("Starting SSH service...")
                    subprocess.run(["systemctl", "start", "sshd"], check=False)
                    subprocess.run(["systemctl", "enable", "sshd"], check=False)
        
        elif distro_id in ['arch', 'manjaro']:
            print_instruction("Installing OpenSSH using pacman...")
            subprocess.run(["pacman", "-S", "--noconfirm", "openssh"], check=False)
            
            # Ask if server should be started
            start_server = input("Do you want to start and enable the SSH server? (Y/n) ").lower()
            if start_server == 'y' or start_server == '':
                print_instruction("Starting SSH service...")
                subprocess.run(["systemctl", "start", "sshd"], check=False)
                subprocess.run(["systemctl", "enable", "sshd"], check=False)
        
        else:
            print_warning(f"Unsupported Linux distribution: {distro_id}")
            print_instruction("Please install OpenSSH manually")
            return False
    
    elif system == "Darwin":  # macOS
        print_instruction("OpenSSH client is already installed on macOS")
        
        # Ask if server should be enabled
        enable_server = input("Do you want to enable the SSH server? (Y/n) ").lower()
        if enable_server == 'y' or enable_server == '':
            print_instruction("Enabling SSH server...")
            subprocess.run(["sudo", "systemsetup", "-setremotelogin", "on"], check=False)
            print_instruction("SSH server enabled")
    
    elif system == "Windows":
        print_instruction("Installing OpenSSH on Windows...")
        print_instruction("This requires PowerShell with administrator privileges")
        
        # Check if OpenSSH is already installed
        ps_check_cmd = 'powershell.exe "Get-WindowsCapability -Online | Where-Object Name -like \'OpenSSH*\'"'
        result = subprocess.run(ps_check_cmd, shell=True, capture_output=True, text=True)
        
        if "OpenSSH.Client" in result.stdout and "State : Installed" in result.stdout:
            print_instruction("OpenSSH client is already installed")
        else:
            print_instruction("Installing OpenSSH client...")
            ps_install_cmd = 'powershell.exe "Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"'
            subprocess.run(ps_install_cmd, shell=True, check=False)
        
        # Ask if server should be installed
        install_server = input("Do you want to install OpenSSH server? (Y/n) ").lower()
        if install_server == 'y' or install_server == '':
            if "OpenSSH.Server" in result.stdout and "State : Installed" in result.stdout:
                print_instruction("OpenSSH server is already installed")
            else:
                print_instruction("Installing OpenSSH server...")
                ps_install_server_cmd = 'powershell.exe "Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0"'
                subprocess.run(ps_install_server_cmd, shell=True, check=False)
            
            # Start and set to automatic startup
            print_instruction("Starting OpenSSH server and setting to automatic startup...")
            ps_start_cmd = 'powershell.exe "Start-Service sshd; Set-Service -Name sshd -StartupType Automatic"'
            subprocess.run(ps_start_cmd, shell=True, check=False)
            
            # Configure firewall
            print_instruction("Configuring firewall...")
            ps_firewall_cmd = 'powershell.exe "if (!(Get-NetFirewallRule -Name \"OpenSSH-Server-In-TCP\" -ErrorAction SilentlyContinue | Select-Object Name, Enabled)) { New-NetFirewallRule -Name \'OpenSSH-Server-In-TCP\' -DisplayName \'OpenSSH Server (sshd)\' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 }"'
            subprocess.run(ps_firewall_cmd, shell=True, check=False)
    
    else:
        print_warning(f"Unsupported operating system: {system}")
        print_instruction("Please install OpenSSH manually")
        return False
    
    # Verify SSH installation
    try:
        result = subprocess.run(["ssh", "-V"], capture_output=True, text=True, stderr=subprocess.STDOUT)
        print_instruction(f"OpenSSH installed successfully: {result.stdout.strip()}")
        return True
    except:
        print_error("OpenSSH installation failed or SSH is not in PATH")
        return False
