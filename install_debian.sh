#!/bin/bash

# Google Dorking Tool - Debian/Ubuntu Installation Script
# MissDorking - Cross-platform Google Dorking Application

echo "============================================"
echo "   Google Dorking Tool - Debian/Ubuntu Setup"
echo "============================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. This is not recommended."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update package list
print_status "Updating package list..."
sudo apt update

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_status "Python 3 not found. Installing Python 3..."
    sudo apt install -y python3
    if [ $? -ne 0 ]; then
        print_error "Failed to install Python 3."
        exit 1
    fi
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_status "pip3 not found. Installing pip3..."
    sudo apt install -y python3-pip
    if [ $? -ne 0 ]; then
        print_error "Failed to install pip3."
        exit 1
    fi
fi

# Install python3-venv if not available
if ! python3 -c "import venv" &> /dev/null; then
    print_status "Installing python3-venv..."
    sudo apt install -y python3-venv
    if [ $? -ne 0 ]; then
        print_error "Failed to install python3-venv."
        exit 1
    fi
fi

# Install system dependencies for some Python packages
print_status "Installing system dependencies..."
sudo apt install -y python3-dev python3-tk libxml2-dev libxslt1-dev zlib1g-dev

print_success "Python 3 is installed."
python3 --version

# Check Python version
python3 -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)"
if [ $? -ne 0 ]; then
    print_error "Python 3.7 or higher is required."
    print_status "Please update your Python installation."
    exit 1
fi

print_success "Python version is compatible."
echo

# Create virtual environment
print_status "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
print_status "Installing required packages..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install requirements."
    print_status "Please check your internet connection and try again."
    exit 1
fi

# Create launch script
print_status "Creating launch script..."
cat > run_dorking_tool.sh << 'EOF'
#!/bin/bash
# Google Dorking Tool Launcher

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# Activate virtual environment
source venv/bin/activate

# Run the application
python main_gui.py

# Deactivate when done
deactivate
EOF

# Make launch script executable
chmod +x run_dorking_tool.sh

# Create desktop entry if desktop environment is available
if [ ! -z "$XDG_CURRENT_DESKTOP" ]; then
    print_status "Creating desktop entry..."
    
    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    
    SCRIPT_DIR="$(pwd)"
    
    cat > "$DESKTOP_DIR/google-dorking-tool.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Google Dorking Tool
Comment=Cross-platform Google dorking application for security testing
Exec=$SCRIPT_DIR/run_dorking_tool.sh
Icon=applications-internet
Path=$SCRIPT_DIR
Terminal=false
StartupNotify=true
Categories=Network;Security;
Keywords=google;dorking;security;reconnaissance;
EOF
    
    chmod +x "$DESKTOP_DIR/google-dorking-tool.desktop"
    print_success "Desktop entry created."
fi

# Create man page directory and install man page
print_status "Creating documentation..."
sudo mkdir -p /usr/local/share/man/man1
cat > dorking-tool.1 << 'EOF'
.TH DORKING-TOOL 1 "2024" "MissDorking" "User Commands"
.SH NAME
dorking-tool \- Google dorking tool for security testing
.SH SYNOPSIS
.B python main_gui.py
.SH DESCRIPTION
MissDorking is a cross-platform Google dorking application that helps security professionals
and researchers perform comprehensive Google searches using various dork queries.
.PP
The tool includes predefined dork categories such as:
.IP \(bu 2
Information Disclosure
.IP \(bu 2
Login Pages
.IP \(bu 2
Configuration Files
.IP \(bu 2
Error Messages
.IP \(bu 2
Database Files
.IP \(bu 2
Directory Listings
.IP \(bu 2
And more...
.SH FEATURES
.IP \(bu 2
Cross-platform GUI using tkinter
.IP \(bu 2
Comprehensive dork query database
.IP \(bu 2
PDF and CSV export capabilities
.IP \(bu 2
Configurable delays to respect rate limits
.IP \(bu 2
Progress tracking and logging
.SH AUTHOR
MissDorking Development Team
.SH "SEE ALSO"
.BR python3 (1)
EOF

sudo cp dorking-tool.1 /usr/local/share/man/man1/ 2>/dev/null || print_warning "Could not install man page (permission denied)"
rm -f dorking-tool.1

echo
echo "============================================"
echo "           Installation Complete!"
echo "============================================"
echo
print_success "The Google Dorking Tool has been successfully installed."
echo
echo "To run the application:"
echo "  1. Run: ./run_dorking_tool.sh"
echo "  2. Or activate venv and run: python main_gui.py"
echo
if [ ! -z "$XDG_CURRENT_DESKTOP" ]; then
    echo "The application has also been added to your applications menu."
fi
echo
print_warning "IMPORTANT NOTES:"
echo "- Use this tool only for authorized security testing"
echo "- Respect Google's terms of service and rate limits"
echo "- The tool includes delays to avoid being blocked"
echo "- Export results to PDF or CSV for analysis"
echo "- Run 'man dorking-tool' for more information"
echo

print_success "Setup completed successfully!"
