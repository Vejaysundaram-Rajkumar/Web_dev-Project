from flask import Flask, render_template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
