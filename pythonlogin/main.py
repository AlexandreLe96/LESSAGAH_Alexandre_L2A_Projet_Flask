
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.models import app
from website import create_app

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:alexandre@localhost:5632/pythonlogin'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
