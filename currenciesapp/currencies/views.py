from flask import Blueprint, request, abort, jsonify
from flask_cors import cross_origin

from currenciesapp.data_models import Currency, CurrencyRates
from currenciesapp.utils import validate_date

currencies = Blueprint('currencies', __name__)


@currencies.route("/get_currencies", methods=['POST'])
@cross_origin()
def get_currencies():
    json = request.get_json()
    if not json:
        abort(400)
    if 'type' not in json:
        abort(422)
    type = json['type']
    date = None
    if 'date' in json:
        date = json['date']
    try:
        if date is None or not validate_date(date, '%Y-%m-%d'):
            last_date = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
                .filter(Currency.type == type).order_by(CurrencyRates.date.desc()).first().date.date()
            date = last_date.strftime('%Y-%m-%d')
        rates = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
            .filter(Currency.type == type).filter(CurrencyRates.date == date).all()
        currencies_list = []
        for rate in rates:
            currencies_list.append({
                'code': rate.currency.code,
                'name': rate.currency.name,
                'price': str(rate.price) + ' ' + rate.base_currency_code,
                'change': rate.change
            })
        return jsonify(date=date, currencies=currencies_list)
    except Exception as e:
        print(e)
        abort(500)


@currencies.route("/get_all_currency_rates", methods=['POST'])
@cross_origin()
def get_all_currency_rates():
    json = request.get_json()
    if not json:
        abort(400)
    if 'currencyCode' not in json:
        abort(422)
    if ('startDate' in json and 'endDate' not in json) or ('endDate' in json and 'startDate' not in json):
        abort(422)
    if 'startDate' in json and 'endDate' in json and (
            not validate_date(json['startDate'], '%Y-%m-%d') or not validate_date(json['endDate'], '%Y-%m-%d')):
        abort(422)
    currency = Currency.query.filter_by(code=json['currencyCode']).first()
    last_rate = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
        .filter(Currency.code == json['currencyCode']).order_by(CurrencyRates.date.desc()).first()
    last_date = last_rate.date.strftime('%Y-%m-%d')
    last_price = str(last_rate.price) + ' ' + last_rate.base_currency_code
    last_change = last_rate.change
    if 'startDate' in json and 'endDate' in json:
        rates = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
            .filter(Currency.code == json['currencyCode']) \
            .filter(CurrencyRates.date >= json['startDate']).filter(CurrencyRates.date <= json['endDate']) \
            .order_by(CurrencyRates.date.desc()).all()
    else:
        rates = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
            .filter(Currency.code == json['currencyCode']) \
            .order_by(CurrencyRates.date.desc()).all()
    rates_list = []
    for rate in rates:
        rates_list.append({
            'date': rate.date.strftime('%Y-%m-%d'),
            'price': str(rate.price) + ' ' + rate.base_currency_code,
            'change': rate.change
        })
    return jsonify(currency_name=currency.name, last_price=last_price, last_change=last_change, last_date=last_date,
                   rates=rates_list)


@currencies.route("/prediction", methods=['POST'])
@cross_origin()
def prediction():
    rates_list = [{'date': '2018-06-03', 'price': '7720.2500 USD', 'change': 1.00},
                  {'date': '2018-06-02', 'price': '7689.3410 USD', 'change': -0.67}]
    return jsonify(rates=rates_list)
