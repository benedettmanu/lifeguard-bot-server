from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_cors import CORS
from app.telegram_bot.bot import bot  # Importa o bot do Telegram

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

# Inicialização do bot do Telegram


def initialize_telegram_bot():
    from telegram_bot.bot import bot
    bot.infinity_polling()  # Inicia o bot do Telegram
    return bot
