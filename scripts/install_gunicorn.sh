#!/usr/bin/bash


PROJECT_MAIN_DIR_NAME="conduit"
current_user=$(whoami)
# Copy gunicorn  service file
sudo cp "/home/$current_user/$PROJECT_MAIN_DIR_NAME/gunicorn/gunicorn.service" "/etc/systemd/system/gunicorn.service"

# Start and enable Gunicorn service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service