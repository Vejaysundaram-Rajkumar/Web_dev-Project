from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import hashlib

#Creating an object for the flask called app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


names=['YourAccount','Signup','Login']


#Connect with the customers database to store the user details
def connect_db():
    connection = sqlite3.connect('customers.db')
    return connection


#rendering the landing or the home page
@app.route('/')
def index():
    if 'username' in session:
        if session['username'] == 'admin@fascars.com':
            return redirect('/fascarsadmin')
        else:
            but_name=names[0]
            return render_template("index.html",name1=but_name,name2=but_name)
    else:
        but1=names[1]
        but2=names[2]
        return render_template("index.html",name1=but2,name2=but1)
  

@app.route('/fascarsadmin')
def fascarsadmin():
    try:
        if session['username'] == 'admin@fascars.com':
            conn = sqlite3.connect('customers.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cardetails')
            details = cursor.fetchall()
            cursor.close()
            return render_template('admin.html', details=details)
        else:
            return "Login as Admin"
    except:
            return "Login as Admin"
    

#rendering the signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'username' in session:
        if session['username'] == 'admin@fascars.com':
            return redirect('/fascarsadmin')
        else:
            return redirect('/dash')
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
        if session['username'] == 'admin@fascars.com':
            return redirect('/fascarsadmin')
        else:
            return redirect('/dash')
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
                if useremail == 'admin@fascars.com':
                    return redirect('/fascarsadmin')
                print("logged in sucessfully.")
                return redirect('/dash')
            
            else:
                err_message="Invalid mail or password!!"
                return render_template('index.html')
        
        else:
            err_message="Invalid mail or password!!"
            return render_template('index.html')
    return render_template('log-in.html')

#logging out from the session of the user or the administrator
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#customer dashboard for buying,selling and repair booking
@app.route('/dash')
def dash():
    # to check the user is logged in or not
    if 'username' not in session:
        return redirect('/login')
    useremail = session['username']
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM user WHERE email=?",(useremail,))
    username=cursor.fetchone()
    # Render the dashboard template 
    return render_template('customerdash.html',customer=username[0])

@app.route('/carupload', methods=['GET', 'POST'])
def carupload():
    # to check the user is logged in or not
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        car_name = request.form['carname']
        age = request.form['yearsold']
        dis=request.form['distance']
        cost=request.form['price']
        useremail = session['username']
        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM user WHERE email=?",(useremail,))
        cname=cursor.fetchone()
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO cardetails (customername, carname, yearsold,kmdriven,price) VALUES (?, ?, ?, ?, ?)", (cname[0], car_name, age, dis,cost))
            connection.commit()
            connection.close()
            print("cardetails updated")
        except:
            err_message="error updating the database"
            return render_template('customerdash.html',message=err_message)
    return redirect('/dash')

@app.route('/accept/<int:id>', methods=['GET', 'POST'])
def accept(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cardetails WHERE id =?",(id,))
    data=cursor.fetchall()
    print(data[0][0])
    cursor.execute("DELETE FROM cardetails WHERE id =?",(id,))
    connection.commit()
    print("accepted ")
    cursor.execute("INSERT INTO accept (customername, carname, yearsold,kmdriven,price) VALUES (?, ?, ?, ?, ?)", (data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]))
    connection.commit()
    connection.close()
    print("Updated in accepted table")
    return redirect('/fascarsadmin')


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
