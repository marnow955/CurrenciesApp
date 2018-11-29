from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    cors = CORS(app)

    # from currenciesapp.main import main
    from currenciesapp.currencies import currencies
    # from currenciesapp.predictions import predictions
    # app.register_blueprint(main)
    app.register_blueprint(currencies)
    # app.register_blueprint(predictions)

    return app