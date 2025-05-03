#!/bin/bash
# Script to build a standalone executable for Deploid

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building Deploid executable...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed. Please install pip3 and try again.${NC}"
    exit 1
fi

# Install required packages
echo -e "${BLUE}Installing required packages...${NC}"
pip3 install PyInstaller readchar

# Create hooks directory if it doesn't exist
mkdir -p hooks

# Create hook file for readchar
echo -e "${BLUE}Creating hook file for readchar...${NC}"
cat > hooks/hook-readchar.py << 'EOF'
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('readchar')
EOF

# Build the executable
echo -e "${BLUE}Building executable...${NC}"
python3 -m PyInstaller --onefile \
  --additional-hooks-dir=hooks \
  --hidden-import=readchar \
  --hidden-import=importlib.metadata \
  --collect-all readchar \
  deploid.py

# Check if the build was successful
if [ -f "dist/deploid" ]; then
    echo -e "${GREEN}Build successful!${NC}"
    echo -e "${BLUE}Executable created at: ${YELLOW}$(pwd)/dist/deploid${NC}"
    
    # Make the executable executable
    chmod +x dist/deploid
    
    # Ask if the user wants to install the executable
    read -p "Do you want to install the executable to /usr/local/bin? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Installing executable...${NC}"
        sudo cp dist/deploid /usr/local/bin/
        echo -e "${GREEN}Executable installed to /usr/local/bin/deploid${NC}"
        echo -e "${BLUE}You can now run Deploid from anywhere by typing: ${YELLOW}deploid${NC}"
    else
        echo -e "${BLUE}You can manually copy the executable to a directory in your PATH:${NC}"
        echo -e "${YELLOW}sudo cp dist/deploid /usr/local/bin/${NC}"
    fi
else
    echo -e "${RED}Build failed. Please check the output for errors.${NC}"
    exit 1
fi
