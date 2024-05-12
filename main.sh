#!/bin/bash
set -e

sudo yum install -y git
current_user=$(whoami)
GIT_REPO_URL="https://github.com/76assignments/realworld.git"

PROJECT_MAIN_DIR_NAME="conduit"
rm -rf /home/$current_user/conduit
git clone "$GIT_REPO_URL" "/home/$current_user/$PROJECT_MAIN_DIR_NAME"

cd "/home/$current_user/$PROJECT_MAIN_DIR_NAME"

chmod +x scripts/*.sh

./scripts/install_os_dependencies.sh
./scripts/install_python_dependencies.sh
./scripts/install_gunicorn.sh
./scripts/start_app.sh
