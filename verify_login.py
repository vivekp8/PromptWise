import requests
import json

BASE_URL = "http://localhost:8000"

def try_login(username, password):
    print(f"Testing login for: {username} ...", end=" ")
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        if res.status_code == 200:
            print(f"SUCCESS! Role: {res.json().get('role')}")
            return True
        else:
            print(f"FAILED ({res.status_code}): {res.text}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

print("--- Verifying Credentials ---")
# Try 1: Username 'admin'
try_login("admin", "adminpassword123")

# Try 2: Email 'admin@promptwise.com'
try_login("admin@promptwise.com", "adminpassword123")
