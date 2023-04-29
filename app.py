from flask import Flask, render_template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return render_template("sign-up.html")


@app.route('/login')
def login():
    return render_template("log-in.html")
@app.route('/pp')
def pp():
    return render_template("privacy-policy.html")
@app.route('/tac')
def tac():
    return render_template("terms-conditions.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
