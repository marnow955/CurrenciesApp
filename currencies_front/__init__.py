from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config.update(dict(
        SECRET_KEY='8A7AABFC9F16DC8F982FA9B073B4EAD0706D646',
        CORS_HEADERS='Content-Type'
    ))
    cors = CORS(app)
    from currencies_front.main import main
    from currencies_front.currencies import currencies
    from currencies_front.predictions import predictions
    from currencies_front.login import login
    app.register_blueprint(main)
    app.register_blueprint(currencies)
    app.register_blueprint(predictions)
    app.register_blueprint(login)
    login = LoginManager(app)
    return app
