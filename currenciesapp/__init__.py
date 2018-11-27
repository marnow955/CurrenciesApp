from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from currenciesapp.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    cors = CORS(app)

    from currenciesapp.users import users
    from currenciesapp.currencies import currencies
    from currenciesapp.users_favourites import users_favourites
    from currenciesapp.exchange_offices import exchange_offices

    app.register_blueprint(users)
    app.register_blueprint(currencies)
    app.register_blueprint(users_favourites)
    app.register_blueprint(exchange_offices)

    return app
