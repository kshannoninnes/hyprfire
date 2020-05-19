In this current directory (project root directory)

To install
1. Run 'python install.py' if you wish to install all the requirements for the application. (sudo password for user is required for apt-get install and postgres commands)

To use the app, activate the virtual environment and start the server.
1. source venv-hyprfire/bin/activate
2. manage.py runserver, optional arguments [ip]:[port], default is port 127.0.0.1:8000
3. travel to [ip]:[port] on your browser

Other directories
-logs directory is where logs will be stored at
-pcaps directory is where pcap files should be stored at

Source distribution
Run python3 setup.py sdist to create a tar.gz of the project. This will be located in dist directory.

To enable debug-level logging
1) Under hyprfire/settings.py, the last section logging describes how to enable debug-level logging.
