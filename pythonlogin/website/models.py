from flask import Flask, request, session, Blueprint, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
import re
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:alexandre@localhost:5632/pythonlogin'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

conn = psycopg2.connect(dbname="pythonlogin", user="postgres",
                        password="alexandre", host="localhost")


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    fullname = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f'<User {self.email}>'


auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(password)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            password_rs = account['password']
            print(password_rs)
            if password_rs == password:
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                return redirect(url_for('views.home'))
            else:
                flash(
                    'Incorrect username/Password/The username and password did not exists')
        else:
            flash(
                'Incorrect username/ password/ The username and password did not exists')
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'fullname' in request.form and 'password' in request.form and 'email' in request.form and 'passwordConfirm' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        passwordConfirm = request.form['passwordConfirm']
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z]+', username):
            flash('Username must contain only characters')
        elif not re.match(r'[A-Za-z]+', fullname):
            flash('Fullname must contain only characters')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        elif password != passwordConfirm:
            flash('Mismatching Password, Please Verify Your Password!')
        else:
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)",
                           (fullname, username, password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('register.html')


@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))
