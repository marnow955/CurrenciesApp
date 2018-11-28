from flask import Blueprint, jsonify, request, abort
from flask_cors import cross_origin

from currenciesapp import db
from currenciesapp.token_auth import requires_auth
from currenciesapp.data_models import Users, Favourites, CurrencyRates, Currency

users_favourites = Blueprint('users_favourites', __name__, url_prefix='/favourites')


@users_favourites.route("/get_favourites", methods=['POST'])
@cross_origin()
@requires_auth
def get_favourites():
    json = request.get_json()
    if not json:
        abort(400)
    if 'username' not in json:
        abort(422)
    user = Users.query.filter_by(username=json['username']).first()
    if not user:
        return jsonify(errorCode='0010', errorDesc='Nie znaleziono użytkownika')
    currencies_codes = [fav.currency_code for fav in user.favourites]
    currencies_list = []
    for code in currencies_codes:
        last_date = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
            .filter(Currency.code == code).order_by(CurrencyRates.date.desc()).first().date.date()
        date = last_date.strftime('%Y-%m-%d')
        rates = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
            .filter(Currency.code == code).filter(CurrencyRates.date == date).all()
        for rate in rates:
            currencies_list.append({
                'date': date,
                'code': rate.currency.code,
                'name': rate.currency.name,
                'price': str(rate.price) + ' ' + rate.base_currency_code,
                'change': rate.change
            })
    return jsonify(currencies=currencies_list)


@users_favourites.route("/add_to_favourites", methods=['POST'])
@cross_origin()
@requires_auth
def add_to_favourites():
    json = request.get_json()
    if not json:
        abort(400)
    if 'username' not in json or 'currencyCode' not in json:
        abort(422)
    user = Users.query.filter_by(username=json['username']).first()
    curr = Currency.query.filter_by(code=json['currencyCode']).first()
    if not user:
        return jsonify(errorCode='0010', errorDesc='Nie znaleziono użytkownika')
    if not curr:
        return jsonify(errorCode='0011', errorDesc=f"Nie znaleziono waluty {json['currencyCode']}")
    fav = Favourites(user_id=user.id, currency_code=json['currencyCode'])
    if len(user.favourites) is 0:
        user.favourites = [fav]
    else:
        fav_check = Favourites.query.filter_by(user_id=user.id).filter_by(currency_code=json['currencyCode']).first()
        if not fav_check:
            user.favourites.append(fav)
    db.session.commit()
    return jsonify(errorCode='0')
