from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)

from users.routes import users

app.register_blueprint(users)

from blog.routes import main

app.register_blueprint(main)

from client.routes import client

app.register_blueprint(client)

from errors.handlers import errors

app.register_blueprint(errors)
