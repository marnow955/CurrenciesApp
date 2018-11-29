from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.SECRET_KEY = '8A7AABFC9F16DC8F982FA9B073B4EAD0706D646'
    app.config.CORS_HEADERS = 'Content-Type'
    cors = CORS(app)
    from currencies_front.main import main
    # from currencies_front.currencies import currency
    # from currencies_front.predictions import predictions
    app.register_blueprint(main)
    # app.register_blueprint(currencies)
    # app.register_blueprint(predictions)

    return app
