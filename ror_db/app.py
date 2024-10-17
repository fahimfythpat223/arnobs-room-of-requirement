from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = '80e32f4c51a8caacefc85d14461a0a7363851d1e25aef2c6'

#mysql connection

db = mysql.connector.connect(
    host ="ror_db",
    user ="root",
    password ="pwnthetesseract",
    database ="ror_db"

)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username, ))
        user = cursor.fetchone

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("invalid username or password")
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
    
if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)

