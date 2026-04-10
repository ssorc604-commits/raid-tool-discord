# packages
import requests
import threading
import time
import random
import keyboard
import os

print("""                                    _     _   _              _ 
 ___ ___  ___  _ __ ___   _ __ __ _(_) __| | | |_ ___   ___ | |
/ __/ __|/ _ \| '__/ __| | '__/ _` | |/ _` | | __/ _ \ / _ \| |
\__ \__ \ (_) | | | (__  | | | (_| | | (_| | | || (_) | (_) | |
|___/___/\___/|_|  \___| |_|  \__,_|_|\__,_|  \__\___/ \___/|_|
                                                               """)

# main
tokens = []
print("\n1 - load from tokens.txt?")
print("2 - paste them manually?")
while True:
    choice = input("\nenter: ").strip()
    if choice == "1":
        tokens_file = "tokens.txt"
        if not os.path.exists(tokens_file):
            print("tokens.txt not found use paste instead")
            choice = "2"
        else:
            with open(tokens_file, "r", encoding="utf-8") as f:
                tokens = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
            print(f"loaded {len(tokens)} token(s) from file")
            break
    elif choice == "2":
        print("\npaste your discord tokens")
        print("when done just hit enter 2x")
        print("-----------------------------------------")
        while True:
            line = input().strip()
            if not line:
                break
            tokens.append(line)
        print(f"loaded {len(tokens)} token(s)")
        break
    else:
        print("just 1 or 2 bro")

if not tokens:
    print("no tokens")
    exit()


channel_id = input("\npaste the channel ID you wanna spam in: ").strip()
if not channel_id:
    print("no channel")
    exit()

print(f"\ntesting first token ")
headers = {"Authorization": tokens[0], "Content-Type": "application/json"}
test = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers)
if test.status_code != 200:
    print(f"first token can't access the channel (error {test.status_code})")
    print("make sure the accounts are in the server and can see the channel")
    exit()
else:
    print("send messages now\n")


# edit these messages ifu want
spam_messages = [
    "SPAM MESSAGE1",
    "SPAM MESSAGE2",
    "SPAM MESSAGE3"
    # put your own stuff here
]

if not spam_messages:
    print("add messages line 63")
    exit()


def send_via_token(token, message):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    payload = {"content": message}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200:
            print(f"[sent] {message[:60]}")
        else:
            print(f"[fail] {r.status_code}")
    except Exception as e:
        print(f"[error] {e}")

# cycle
cycler_running = False

def spam_cycler():
    index = 0
    while cycler_running:
        for token in tokens:
            if not cycler_running:
                break
            msg = spam_messages[index]
            send_via_token(token, msg)
            index = (index + 1) % len(spam_messages)
            time.sleep(random.uniform(0.08, 0.12))  # tiny delay so it looks natural
        time.sleep(random.uniform(3.5, 5.5))  # bigger pause between full cycles


def toggle_spam():
    global cycler_running
    cycler_running = not cycler_running
    if cycler_running:
        print(f"SPAMMING STARTeD - {len(tokens)}")
        threading.Thread(target=spam_cycler, daemon=True).start()
    else:
        print("spam stopped")

# keybind
keyboard.add_hotkey("p", toggle_spam)

print(f"loaded {len(tokens)} accounts")
print("press P to toggle")
print("press ESC to exit")
print("\npro tip: edit the messages list at the top before running next time")

keyboard.wait("esc")
