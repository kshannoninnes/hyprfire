In this current directory (project root directory)

To install
1. Run 'python install.py' if you wish to install all the requirements for the application. (sudo password for user is required for apt-get install and postgres commands)

To use the app, activate the virtual environment and start the server.
1. python run.py
1.1 optional: python run.py (local computer ip address) (whatever port to host django server)
2. travel to [ip]:[port] on your browser

Other directories
-logs directory is where logs will be stored at
-pcaps directory is where pcap files should be stored at

Source distribution
Run python3 setup.py sdist to create a tar.gz of the project. This will be located in dist directory.

To enable debug-level logging
1) Under hyprfire/settings.py, the last section logging describes how to enable debug-level logging.
