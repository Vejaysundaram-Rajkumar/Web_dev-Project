from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib

#Creating an object for the flask called app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('customers.db')
    return connection


#rendering the landing or the home page
@app.route('/')
def index():
    return render_template("index.html")
#rendering the signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'username' in session:
        return redirect(url_for('#'))
    if request.method == 'POST':
        username = request.form['sname']
        password = request.form['spassword']
        email = request.form['semail']
        
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        user = cursor.fetchone()
        print(user)
        try:
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)", (username, password_hash, email))
            connection.commit()
            connection.close()
           
        except:
            err_message="E-mail already registered!"
            return render_template('index.html',message=err_message)
        return redirect('/login')
    create_message ="Account created successfully!"
    return render_template("sign-up.html")

#rendering the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #checking if already any useer logged in and that person is in session or not.
    if 'username' in session:
        return redirect(url_for('/'))
    
    #checking if the user subbmitted the form for login or not.
    if request.method == 'POST':
        try:
            useremail = request.form['lemail']
            password = request.form['lpassword']
            connection = connect_db()
            cursor = connection.cursor()
            #Getting the user's info by using the usermail
            cursor.execute("SELECT * FROM user WHERE email=?", (useremail,))
            user = cursor.fetchone()
            print(user)
        except:
            return "E-mail already Exists"
        #checking if the user exists
        if user:
            # Hash the entered password and compare with the stored hash
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            #Checking if the password entered is correct or not with the help of database.
            if password_hash == user[2]:
                #Setting the session in that particular user's session 
                session['username'] = useremail
                
                #if the mail is admins .. then redirect to his dashboard not the users.
                if useremail == 'printease2023@gmail.com':
                    return redirect('/admin')
                print("logged in sucessfully.")
                return redirect('/')
            
            else:
                err_message="Invalid mail or password!!"
                return render_template('index.html')
        
        else:
            err_message="Invalid mail or password!!"
            return render_template('index.html')
    return render_template('log-in.html')

#rendering the privacy policy page
@app.route('/pp')
def pp():
    return render_template("privacy-policy.html")

#rendering the terms and conditions page
@app.route('/tac')
def tac():
    return render_template("terms-conditions.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
