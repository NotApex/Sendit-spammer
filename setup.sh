#!/bin/bash

# Install necessary packages
pkg update
pkg install -y clang libxml2 libxslt python
pkg update -y && pkg upgrade -y

# Install lxml dependencies
pip install -y libxml2-dev libxslt-dev

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# Install dependencies
apt-get update
apt-get install -y libxml2 libxslt

# Install lxml from the repository
pip install lxml

# Install other Python packages
pip install -r requirements.txt

# Start main.py
python main.py
