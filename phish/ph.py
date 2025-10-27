from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import urlparse  # <-- Ye line jaruri hai

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            error = "Please enter a URL."
            return render_template('index.html', error=error)
        return redirect(url_for('result', user_url=url))
    return render_template('index.html')

# New improved phishing detection function
def is_phishing_url(url):
    suspicious_keywords = ['login', 'verify', 'update', 'bank', 'account']  # "secure" hata diya
    max_length = 120  # normal URLs bhi 75 se bade ho sakte hain

    if not url or url.strip() == "":
        return False

    if not url.startswith('http'):
        url = 'https://' + url  # Default to HTTPS

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc.lower()
    path = parsed_url.path.lower()

    # Whitelist: trusted domains
    whitelist = ['google.com', 'perplexity.ai', 'microsoft.com', 'github.com']
    for trusted in whitelist:
        if trusted in hostname:
            return False

    # Check keywords only in hostname and path
    for keyword in suspicious_keywords:
        if keyword in hostname or keyword in path:
            return True

    if len(url) > max_length:
        return False  # lamba URL phishing nahi hai unless suspicious na mile 

    if url.lower().startswith('http://'):
        return True

    return False
