SQL Injection Automated Testing Tool
A powerful Python-based tool for automated testing of SQL injection vulnerabilities in web applications. This script is created for penetration testers, students, and cybersecurity enthusiasts to identify potential SQLi issues in GET and POST parameters using multiple payloads and smart detection logic.

Features
Automated Detection: Scans all URL parameters with a range of classic SQLi payloads.

GET/POST Support: Works for both GET query parameters and POST body data.

Advanced Payloads: Boolean-based, error-based, time-based blind, and UNION-based SQLi payloads included.

Stealth Requests: Rotates User-Agents and randomizes timing for basic stealth.

Color-Coded Output: Uses Colorama to clearly highlight possible vulnerabilities.

Progress Tracking: See testing progress with tqdm progress bars.

Comprehensive Logging: Results are stored in sqli_tool_log.txt for later analysis.

Requirements
Python 3.x

Modules: requests, tqdm, colorama

text
pip install requests tqdm colorama
Usage
Run the script:

text
python sqlitest.py
Follow prompts:

Enter the target URL (with parameters for GET).

Select request method (GET or POST).

For POST, enter each parameter name and value manually.

Example:

For GET:

text
Enter full URL (with parameters) for GET: http://example.com/search.php?id=1
For POST:

text
Enter URL: http://example.com/login.php
Request method (GET/POST): POST
Then enter parameter names/values as prompted.
Detection Logic
Baseline response length is calculated first.

For each parameter, all payloads are injected one-by-one.

If the response length changes significantly for any payload, it flags as a possible vulnerability.

Example Payloads Used
Boolean-based:

' OR '1'='1

" OR "1"="1" --

Error-based:

' AND 1=CONVERT(int, (SELECT @@version)) --

Time-based blind:

' WAITFOR DELAY '0:0:5'--

UNION-based:

' UNION SELECT NULL,NULL--

(Full payload list is editable in code for customization)

Output
Green Alert: Parameter may be vulnerable to SQL injection.

White: No signficant response difference found.

Logs: Details stored in sqli_tool_log.txt for audit trail.

Disclaimer
This tool is for educational and authorized penetration testing only. Never use it on live or production systems without explicit permission. All users are responsible for legal and ethical usage.

Author
Yashika Kanwer — Made for RTU Cybersecurity/Ethical Hacking Practice.

