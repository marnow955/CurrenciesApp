from flask import Blueprint, jsonify
from flask_cors import cross_origin


users_favourites = Blueprint('users_favourites', __name__, url_prefix='/favourites')


@users_favourites.route("/get_favourites", methods=['POST'])
@cross_origin()
def get_favourites():
    currencies = [{'code': 'BTC', 'name': 'Bitcoin', 'price': '7720.2500 USD', 'change': 1.00},
                  {'code': 'USD', 'name': 'Dolar amerykański', 'price': '3.4712 PLN', 'change': 0.63}]
    return jsonify(date='2018-06-03', currencies=currencies)


@users_favourites.route("/add_to_favourites", methods=['POST'])
@cross_origin()
def add_to_favourites():
    return jsonify(errorCode='0')
