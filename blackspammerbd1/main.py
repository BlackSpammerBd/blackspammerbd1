#!/usr/bin/env python3
import sys
import os
import random
import string
import requests
import base64

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# সার্ভারের URL (আপনার প্রয়োজনে পরিবর্তন করুন)
SERVER_URL = "http://your_server_address:5000"

def generate_connection_code():
    return ''.join(random.choices(string.digits, k=8))

def start():
    code = generate_connection_code()
    print(f"[92m[+] Your connection code: {code}[0m")
    # প্রয়োজনে এখানে সার্ভার শুরু করার কোড যোগ করুন
    return code

def connect(code):
    print(f"[96m[+] Attempting to connect using code: {code}[0m")
    try:
        response = requests.post(f"{SERVER_URL}/connect", json={"connection_code": code})
        if response.status_code == 200:
            print(f"[92m[+] Connection successful: {response.json()}[0m")
        else:
            print(f"[91m[-] Connection failed: {response.text}[0m")
    except Exception as e:
        print(f"[91m[-] Error connecting: {e}[0m")

def list_all():
    print(f"[93m[+] Listing all files and folders...[0m")
    try:
        response = requests.get(f"{SERVER_URL}/list")
        if response.status_code == 200:
            files = response.json().get("files", [])
            for item in files:
                print(f"  - {item}")
        else:
            print(f"[91m[-] Failed to retrieve list: {response.text}[0m")
    except Exception as e:
        print(f"[91m[-] Error: {e}[0m")

def download_item(item_name):
    print(f"[96m[+] Downloading: {item_name}[0m")
    try:
        response = requests.get(f"{SERVER_URL}/download/{item_name}")
        if response.status_code == 200:
            data = base64.b64decode(response.json().get("data", ""))
            with open(item_name, "wb") as f:
                f.write(data)
            print(f"[92m[+] Downloaded '{item_name}' successfully.[0m")
        else:
            print(f"[91m[-] Download failed: {response.text}[0m")
    except Exception as e:
        print(f"[91m[-] Error: {e}[0m")

def upload_item(item_name):
    print(f"[96m[+] Uploading: {item_name}[0m")
    try:
        with open(item_name, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        response = requests.post(f"{SERVER_URL}/upload", json={"item": item_name, "data": data})
        if response.status_code == 200:
            print(f"[92m[+] Uploaded '{item_name}' successfully.[0m")
        else:
            print(f"[91m[-] Upload failed: {response.text}[0m")
    except Exception as e:
        print(f"[91m[-] Error: {e}[0m")

def main():
    if len(sys.argv) < 2:
        print(f"[93mUsage: bsb -start | -connect <code> | -list all | -download <name> | -upload <name>[0m")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "-start":
        start()
    elif cmd == "-connect":
        if len(sys.argv) < 3:
            print(f"[91m[-] Please provide a connection code.[0m")
        else:
            connect(sys.argv[2])
    elif cmd == "-list" and len(sys.argv) == 3 and sys.argv[2] == "all":
        list_all()
    elif cmd == "-download":
        if len(sys.argv) < 3:
            print(f"[91m[-] Please specify the item name to download.[0m")
        else:
            download_item(sys.argv[2])
    elif cmd == "-upload":
        if len(sys.argv) < 3:
            print(f"[91m[-] Please specify the item name to upload.[0m")
        else:
            upload_item(sys.argv[2])
    else:
        print(f"[91m[-] Unknown command.[0m")

if __name__ == "__main__":
    main()
