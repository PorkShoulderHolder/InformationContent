#!/bin/bash
set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting installation...${NC}"

# Check if zstd is installed
if ! command -v zstd &> /dev/null; then
    echo -e "${YELLOW}Installing zstd...${NC}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y zstd
        elif command -v yum &> /dev/null; then
            sudo yum install -y zstd
        else
            echo -e "${RED}Unsupported package manager. Please install zstd manually.${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install zstd
        else
            echo -e "${RED}Homebrew not found. Please install Homebrew first.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Unsupported operating system. Please install zstd manually.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}zstd is already installed${NC}"
fi

# Check if we're in a virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}No virtual environment detected. Creating one...${NC}"
    
    # Check if python3 is installed
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
        exit 1
    fi

    # Check if virtualenv is installed
    if ! command -v virtualenv &> /dev/null; then
        echo -e "${YELLOW}Installing virtualenv...${NC}"
        python3 -m pip install --user virtualenv
    fi

    # Create and activate virtual environment
    python3 -m virtualenv venv
    source venv/bin/activate
else
    echo -e "${GREEN}Using existing virtual environment: ${VIRTUAL_ENV}${NC}"
fi

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}To activate the virtual environment, run: source venv/bin/activate${NC}" 