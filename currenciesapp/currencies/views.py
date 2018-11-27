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
            currency = {}
            currency['code'] = rate.currency.code
            currency['name'] = rate.currency.name
            currency['price'] = str(rate.price) + ' ' + rate.base_currency_code
            currency['change'] = rate.change
            currencies_list.append(currency)
        return jsonify(date=date, currencies=currencies_list)
    except Exception as e:
        print(e)
        abort(500)


@currencies.route("/get_all_currency_rates", methods=['POST'])
@cross_origin()
def get_all_currency_rates():
    rates_list = [{'date': '2018-06-03', 'price': '7720.2500 USD', 'change': 1.00},
                  {'date': '2018-06-02', 'price': '7689.3410 USD', 'change': -0.67}]
    return jsonify(currency_name='Bitcoin', last_price='7720.2500 USD', last_change=1.00, last_date='2018-06-03',
                   rates=rates_list)


@currencies.route("/prediction", methods=['POST'])
@cross_origin()
def prediction():
    rates_list = [{'date': '2018-06-03', 'price': '7720.2500 USD', 'change': 1.00},
                  {'date': '2018-06-02', 'price': '7689.3410 USD', 'change': -0.67}]
    return jsonify(rates=rates_list)
