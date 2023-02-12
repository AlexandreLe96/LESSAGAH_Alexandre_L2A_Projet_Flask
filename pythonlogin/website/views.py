
from flask import Blueprint, session, redirect, url_for, render_template
import psycopg2
import psycopg2.extras
from .models import auth

conn = psycopg2.connect(dbname="pythonlogin", user="postgres",
                        password="alexandre", host="localhost")

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', email=session['email'])
    return redirect(url_for('auth.login'))


@views.route('/profile')
def profile():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))
