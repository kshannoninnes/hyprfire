import subprocess
import sys

# checks for shell command arguments to see whether it should run as default server or server on specific port.

# example: "python run.py" will trigger this, run server at 127.0.0.1 on 8000
python_path = "venv-hyprfire/bin/python"
if len(sys.argv) == 1:
    subprocess.call([python_path, "manage.py", "runserver"])

# example: "python run.py 192.168.1.5 9999" will trigger this, run server at 192.168.1.5 on port 9999
elif len(sys.argv) == 3:
    ip_port = sys.argv[1] + ":" + sys.argv[2]
    print(ip_port)
    subprocess.call([python_path, "manage.py", "runserver", ip_port])
