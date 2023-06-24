# Update apt
apt update
apt upgrade

# Install necessary packages
apt update
apt install -y clang libxml2
pkg install -y python
pkg install -y libxslt python3-pip python3-dev openssl-dev libffi-dev

# Install lxml dependencies
apt install -y libxml2-dev libxslt-dev

# Install aiohttp
pip3 install --upgrade pip
pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org aiohttp

# Install dependencies
apt-get update
apt-get install -y libxml2 libxslt

# Install lxml from the repository
pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org lxml

# Install other Python packages
pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

# Start main.py
python main.py
