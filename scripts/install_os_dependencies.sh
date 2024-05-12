#!/usr/bin/env bash
sudo yum update -y  # Update package lists

# Install Python3 pip
sudo yum install -y python3-pip

# Install Virtualenv
sudo pip3 install virtualenv



# Install pkg-config
sudo yum install -y pkgconfig

sudo yum groupinstall -y "Development Tools"


sudo yum install  -y python3-devel