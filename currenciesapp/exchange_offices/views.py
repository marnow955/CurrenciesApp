from flask import Blueprint, jsonify
from flask_cors import cross_origin

exchange_offices = Blueprint('exchange_offices', __name__, url_prefix='/exchange_offices')


@exchange_offices.route("/get_provinces", methods=['GET'])
@cross_origin()
def get_provinces():
    provinces = ['Mazowieckie', 'Lubelskie', 'Lubuskie', 'Małopolskie']
    return jsonify(provinces=provinces)


@exchange_offices.route("/get_cities", methods=['POST'])
@cross_origin()
def get_cities():
    cities = ['Warszawa', 'Lublin', 'Radom', 'Puławy']
    return jsonify(cities=cities)


@exchange_offices.route("/get_offices", methods=['POST'])
@cross_origin()
def get_offices():
    offices = [{'id': 1, 'name': 'KANTOREX - POL', 'rank': 10, 'country': 'Polska', 'province': 'Mazowieckie',
                'city': 'Warszawa', 'street': 'Al. Jerozolimskie', 'streetNumber': 13, 'flatNumber': 2,
                'postalCode': '02-023'},
               {'id': 2, 'name': 'KANTORUŚ', 'rank': 1, 'country': 'Polska', 'province': 'Mazowieckie',
                'city': 'Radom', 'street': 'Al. Jerozolimskie', 'streetNumber': 3, 'flatNumber': 22,
                'postalCode': '01-013'}]
    return jsonify(offices=offices)


@exchange_offices.route("/evaluate", methods=['POST'])
@cross_origin()
def evaluate():
    return jsonify(errorCode='0')
