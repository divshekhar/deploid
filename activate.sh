#!/bin/sh
# Script to activate the virtual environment

# Check if the script is being sourced
# https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
sourced=0
if [ -n "$ZSH_VERSION" ]; then
    # zsh
    if [ "$ZSH_EVAL_CONTEXT" = "toplevel:file" ] || [ "$ZSH_EVAL_CONTEXT" = "file" ]; then
        sourced=1
    fi
elif [ -n "$BASH_VERSION" ]; then
    # bash
    (return 0 2>/dev/null) && sourced=1
else
    # other shells: assume not sourced
    sourced=0
fi

# Get the directory of this script
# This works in both bash and zsh
if [ -n "$BASH_SOURCE" ]; then
    # For Bash
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
elif [ -n "$ZSH_VERSION" ]; then
    # For Zsh
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
else
    # Fallback
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Virtual environment not found. Creating one now..."
    python3 -m venv "$SCRIPT_DIR/venv"
    "$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
fi

# Check if the script is being sourced
if [ "$sourced" = "1" ]; then
    # Activate the virtual environment
    . "$SCRIPT_DIR/venv/bin/activate"

    # Print success message
    echo "Virtual environment activated!"
    echo "You can now run the deploid.py script with: python deploid.py"
else
    # Print warning message
    echo "⚠️  WARNING: This script must be sourced to activate the virtual environment."
    echo "Please run: source ./activate.sh"
    echo ""
    echo "Running the script with ./activate.sh will not work because the environment"
    echo "changes will only affect the subshell and not your current terminal session."
    exit 1
fi
