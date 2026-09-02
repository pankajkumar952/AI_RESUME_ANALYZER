#!/bin/bash
# Startup script for Smart AI Resume Analyzer
# This script installs the correct chromedriver before starting the application

echo "Starting Smart AI Resume Analyzer setup..."

# Check if Chrome/Chromium is installed
if command -v google-chrome &> /dev/null; then
    CHROME_BIN="google-chrome"
elif command -v chromium &> /dev/null; then
    CHROME_BIN="chromium"
elif command -v chromium-browser &> /dev/null; then
    CHROME_BIN="chromium-browser"
else
    echo "Chrome/Chromium not found. Installing Chromium..."
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y chromium-browser
        CHROME_BIN="chromium-browser"
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y chromium
        CHROME_BIN="chromium"
    else
        echo "Could not install Chrome/Chromium. Please install it manually."
        exit 1
    fi
fi

# Get Chrome version
CHROME_VERSION=$($CHROME_BIN --version | awk '{print $2}' | cut -d. -f1)
echo "Detected Chrome/Chromium version: $CHROME_VERSION"

# Run the chromedriver setup script
echo "Setting up chromedriver..."
python setup_chromedriver.py

# Make the script executable
chmod +x setup_chromedriver.py

echo "Setup completed. Starting application..."

# Start the application
streamlit run app.py 