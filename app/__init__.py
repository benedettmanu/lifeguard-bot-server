from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_cors import CORS


db = SQLAlchemy()
login_manager = flask_login.LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = '%P,}8|c/k$w:98i'
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    return app
