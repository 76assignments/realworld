#!/usr/bin/env bash
set -e

PROJECT_MAIN_DIR_NAME="conduit"
current_user=$(whoami)
# Validate variables
if [ -z "$PROJECT_MAIN_DIR_NAME" ]; then
    echo "Error: PROJECT_MAIN_DIR_NAME is not set. Please set it to your project directory name." >&2
    exit 1
fi

# Change ownership to  user
sudo chown -R $current_user:$current_user "/home/$current_user/$PROJECT_MAIN_DIR_NAME"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "/home/$current_user/$PROJECT_MAIN_DIR_NAME/venv"

# Activate virtual environment
echo "Activating virtual environment..."
source "/home/$current_user/$PROJECT_MAIN_DIR_NAME/venv/bin/activate"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r "/home/$current_user/$PROJECT_MAIN_DIR_NAME/requirements.txt"

pip install mysqlclient
pip install gunicorn
echo "Dependencies installed successfully."
