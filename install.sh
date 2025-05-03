#!/bin/bash
# Deploid Installer Script
# This script downloads and installs Deploid, an AI agent for DevOps

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_message() {
    echo -e "${GREEN}[+] $1${NC}"
}

print_instruction() {
    echo -e "${BLUE}[*] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Default installation directory
DEFAULT_INSTALL_DIR="$HOME/.deploid"
INSTALL_DIR="$DEFAULT_INSTALL_DIR"

# Check if Python 3 is installed
check_python() {
    print_message "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 and try again."
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_instruction "Found Python $PYTHON_VERSION"
}

# Check if pip is installed
check_pip() {
    print_message "Checking pip installation..."
    if ! command -v pip3 &> /dev/null; then
        print_warning "pip3 is not installed. Attempting to install pip..."

        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3-pip
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pip
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python-pip
        elif command -v brew &> /dev/null; then
            brew install python # This includes pip
        else
            print_error "Could not install pip. Please install pip manually and try again."
            exit 1
        fi
    fi

    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    print_instruction "Found pip $PIP_VERSION"
}

# Download Deploid
download_deploid() {
    print_message "Downloading Deploid..."

    # Get the latest release version if not specified
    if [ -z "$VERSION" ]; then
        print_instruction "Determining latest release version..."

        if command -v curl &> /dev/null; then
            VERSION=$(curl -s https://api.github.com/repos/divshekhar/deploid/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
        elif command -v wget &> /dev/null; then
            VERSION=$(wget -qO- https://api.github.com/repos/divshekhar/deploid/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
        else
            print_error "Neither curl nor wget is installed. Please install one of them and try again."
            exit 1
        fi

        if [ -z "$VERSION" ]; then
            print_warning "Could not determine latest version. Using default."
            VERSION="main"
        else
            print_instruction "Latest version: $VERSION"
        fi
    fi

    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    # Set download URL based on version
    if [ "$VERSION" = "main" ]; then
        DOWNLOAD_URL="https://github.com/divshekhar/deploid/archive/main.zip"
        EXTRACT_DIR="deploid-main"
    else
        DOWNLOAD_URL="https://github.com/divshekhar/deploid/releases/download/${VERSION}/deploid-${VERSION}.zip"
        EXTRACT_DIR="deploid-${VERSION}"
    fi

    print_instruction "Downloading from: $DOWNLOAD_URL"

    # Download the specified version
    if command -v curl &> /dev/null; then
        curl -L -o deploid.zip "$DOWNLOAD_URL"
    elif command -v wget &> /dev/null; then
        wget -O deploid.zip "$DOWNLOAD_URL"
    else
        print_error "Neither curl nor wget is installed. Please install one of them and try again."
        exit 1
    fi

    # Extract the archive
    if command -v unzip &> /dev/null; then
        unzip deploid.zip
        mv "$EXTRACT_DIR"/* .
        rm -rf "$EXTRACT_DIR"
    else
        print_error "unzip is not installed. Please install unzip and try again."
        exit 1
    fi

    # Create installation directory if it doesn't exist
    mkdir -p "$INSTALL_DIR"

    # Copy files to installation directory
    cp -r * "$INSTALL_DIR"

    # Clean up
    cd - > /dev/null
    rm -rf "$TEMP_DIR"

    print_instruction "Deploid $VERSION downloaded and extracted to $INSTALL_DIR"
}

# Set up virtual environment
setup_venv() {
    print_message "Setting up virtual environment..."

    cd "$INSTALL_DIR"

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate

    print_instruction "Virtual environment set up successfully"
}

# Create executable wrapper
create_wrapper() {
    print_message "Creating executable wrapper..."

    # Determine bin directory
    if [ -d "$HOME/.local/bin" ] && [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        BIN_DIR="$HOME/.local/bin"
    elif [ -d "/usr/local/bin" ]; then
        BIN_DIR="/usr/local/bin"
        # Check if we have write permissions, if not use sudo
        if [ ! -w "$BIN_DIR" ]; then
            print_warning "Need sudo access to write to $BIN_DIR"
            SUDO_REQUIRED=true
        fi
    else
        BIN_DIR="$HOME/bin"
        mkdir -p "$BIN_DIR"

        # Add to PATH if not already there
        if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
            print_warning "$BIN_DIR is not in your PATH. Adding it to your shell profile."

            # Determine shell profile file
            if [ -n "$BASH_VERSION" ]; then
                PROFILE_FILE="$HOME/.bashrc"
            elif [ -n "$ZSH_VERSION" ]; then
                PROFILE_FILE="$HOME/.zshrc"
            else
                PROFILE_FILE="$HOME/.profile"
            fi

            echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$PROFILE_FILE"
            print_instruction "Added $BIN_DIR to your PATH in $PROFILE_FILE"
            print_instruction "Please run 'source $PROFILE_FILE' or restart your terminal to apply changes"
        fi
    fi

    # Create wrapper script
    WRAPPER_CONTENT="#!/bin/bash
# Deploid wrapper script

# Get the directory of this script
SCRIPT_DIR=\"\$(cd \"\$(dirname \"\${BASH_SOURCE[0]}\")\" && pwd)\"

# Activate virtual environment and run deploid
cd \"$INSTALL_DIR\"
source venv/bin/activate
python deploid.py \"\$@\"
deactivate
"

    if [ "$SUDO_REQUIRED" = true ]; then
        echo "$WRAPPER_CONTENT" | sudo tee "$BIN_DIR/deploid" > /dev/null
        sudo chmod +x "$BIN_DIR/deploid"
    else
        echo "$WRAPPER_CONTENT" > "$BIN_DIR/deploid"
        chmod +x "$BIN_DIR/deploid"
    fi

    print_instruction "Executable wrapper created at $BIN_DIR/deploid"
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--version)
                VERSION="$2"
                shift 2
                ;;
            -d|--directory)
                INSTALL_DIR="$2"
                shift 2
                ;;
            -y|--yes)
                AUTO_CONFIRM=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  -v, --version VERSION    Specify the version to install (default: latest)"
                echo "  -d, --directory DIR      Specify the installation directory (default: $DEFAULT_INSTALL_DIR)"
                echo "  -y, --yes                Automatic yes to prompts"
                echo "  -h, --help               Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use -h or --help to see available options"
                exit 1
                ;;
        esac
    done
}

# Main installation process
main() {
    print_message "Starting Deploid installation..."

    # Parse command line arguments
    parse_args "$@"

    # Check requirements
    check_python
    check_pip

    # Ask for installation directory if not specified and not in auto mode
    if [ -z "$INSTALL_DIR" ] && [ "$AUTO_CONFIRM" != true ]; then
        read -p "Enter installation directory (default: $DEFAULT_INSTALL_DIR): " user_install_dir
        if [ -n "$user_install_dir" ]; then
            INSTALL_DIR="$user_install_dir"
        fi
    fi

    # Download and install
    download_deploid
    setup_venv
    create_wrapper

    print_message "Deploid has been successfully installed!"
    print_instruction "You can now run 'deploid' from anywhere in your terminal."
    print_instruction "If the command is not found, you may need to restart your terminal or run 'source ~/.bashrc' (or your shell's equivalent)."
}

# Run the main function with all arguments
main "$@"
