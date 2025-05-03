#!/bin/bash
# This script downloads and runs the Deploid installer
# Usage: ./download.sh [version] [options]
# Example: ./download.sh v1.0.0 --directory ~/deploid-custom

# Set default version to latest
VERSION=${1:-latest}

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Downloading Deploid installer...${NC}"

# Determine download URL based on version
if [ "$VERSION" = "latest" ]; then
    DOWNLOAD_URL="https://github.com/yourusername/deploid/releases/latest/download/install.sh"
else
    DOWNLOAD_URL="https://github.com/yourusername/deploid/releases/download/${VERSION}/install.sh"
fi

echo -e "${BLUE}Download URL: ${DOWNLOAD_URL}${NC}"

# Download the installer
if command -v curl &> /dev/null; then
    curl -sSL "$DOWNLOAD_URL" -o install.sh
elif command -v wget &> /dev/null; then
    wget -qO install.sh "$DOWNLOAD_URL"
else
    echo "Error: Neither curl nor wget is installed. Please install one of them and try again."
    exit 1
fi

# Make it executable
chmod +x install.sh

# Prepare arguments for the installer
INSTALLER_ARGS=""
if [ "$VERSION" != "latest" ]; then
    INSTALLER_ARGS="--version $VERSION"
fi

# Add any additional arguments passed to this script
if [ $# -gt 1 ]; then
    shift
    INSTALLER_ARGS="$INSTALLER_ARGS $@"
fi

echo -e "${GREEN}Running installer with arguments: ${INSTALLER_ARGS}${NC}"

# Run the installer with arguments
./install.sh $INSTALLER_ARGS

# Clean up
rm install.sh

echo -e "${GREEN}Installation complete!${NC}"
