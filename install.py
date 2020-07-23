import subprocess

# Install non-python libraries
subprocess.call("sudo apt-get install python python-setuptools python3.8 virtualenv python3-pip libpq-dev python3-dev python3.8-dev postgresql-contrib wireshark gcc", shell=True)

# Create User
subprocess.call("sudo -u postgres psql postgres -c \"ALTER USER postgres WITH PASSWORD 'adminPostgres'\"", shell=True)

# Create database
subprocess.call("sudo -u postgres psql postgres -c 'CREATE DATABASE hyprfiredb'", shell=True)

# Create Virtual Env
subprocess.call("virtualenv -p /usr/bin/python3.8 venv-hyprfire", shell=True)

# Run pip install
pip_path = "venv-hyprfire/bin/pip"
subprocess.call([pip_path, "install", "-e", ".", "-r", "requirements.txt"])

# Run manage.py makemigrations
python_path = "venv-hyprfire/bin/python"
subprocess.call([python_path, "manage.py", "makemigrations"])

# Run manage.py migrate
subprocess.call([python_path, "manage.py", "migrate"])
