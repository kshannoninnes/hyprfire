import subprocess
import sys

python_path = "venv-hyprfire/bin/python"
if len(sys.argv) == 1:
    subprocess.call([python_path, "manage.py", "runserver"])

elif len(sys.argv) == 3:
    ip_port = sys.argv[1] + ":" + sys.argv[2]
    print(ip_port)
    subprocess.call([python_path, "manage.py", "runserver", ip_port])
