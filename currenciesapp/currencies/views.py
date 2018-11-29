from flask import Blueprint, request, abort, jsonify
from flask_cors import cross_origin
from datetime import datetime, timedelta

from currenciesapp.data_models import Currency, CurrencyRates
from currenciesapp.utils import validate_date
from prediction.train import train_and_predict

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
    return jsonify(currencyName=currency.name, lastPrice=last_price, lastChange=last_change, lastDate=last_date,
                   rates=rates_list)


@currencies.route("/prediction", methods=['POST'])
@cross_origin()
def prediction():
    json = request.get_json()
    if not json:
        abort(400)
    if 'currencyCode' not in json:
        abort(422)
    predictions = []
    rates = []
    pchanges = []
    currency = Currency.query.filter_by(code=json['currencyCode']).first()

    last_rate = CurrencyRates.query.join(Currency, Currency.code == CurrencyRates.currency_code) \
        .filter(Currency.code == json['currencyCode']).order_by(CurrencyRates.date.desc()).first()
    last_date = last_rate.date.strftime('%Y-%m-%d')
    last_price = str(last_rate.price) + ' ' + last_rate.base_currency_code
    last_change = last_rate.change

    if 'startDate' not in json or 'endDate' not in json:
        return jsonify(currencyName=currency.name, lastPrice=last_price, lastChange=last_change, lastDate=last_date,
                       rates=[])

    start_date = datetime.strptime(json['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(json['endDate'], '%Y-%m-%d')

    rates = CurrencyRates.query.filter(CurrencyRates.currency == currency,
                                       CurrencyRates.date.between(start_date, end_date)).order_by(
        CurrencyRates.date.desc()).all()
    train_predict, test_predict = train_and_predict(currency.code, start_date, end_date)
    test_predict_list = test_predict.tolist()
    test_predictions = [round(x, 4) for l in test_predict_list for x in l]
    pchanges.append(0.00)
    for i in range(1, len(test_predictions)):
        pchanges.append(round((test_predictions[i] - test_predictions[i - 1]) * 100 / test_predictions[i - 1], 2))
    test_predictions = test_predictions[::-1]
    # print(test_predictions)
    day_count = (end_date - start_date).days + 1
    for single_date in (end_date - timedelta(n) for n in range(day_count)):
        i = (end_date - single_date).days
        contains = False
        for rate in rates:
            print(rate.date.strftime("%Y-%m-%d") + " = " + single_date.strftime("%Y-%m-%d"))
            if rate.date.strftime("%Y-%m-%d") == single_date.strftime("%Y-%m-%d"):
                contains = True
                break
        if contains:
            # print(single_date.strftime("%Y-%m-%d") + " " + str(i))
            predictions.append(test_predictions[i])
    print(len(rates))
    print(len(predictions))
    pchanges = pchanges[::-1]
    rates_list = []
    for i in range(len(predictions)):
        rates_list.append({
            'date': rates[i].date.strftime('%Y-%m-%d'),
            'price': str(predictions[i]) + ' ' + rates[i].base_currency_code,
            'change': pchanges[i],
            'realPrice': str(rates[i].price) + ' ' + rates[i].base_currency_code,
            'realChange': rates[i].change
        })
    return jsonify(currencyName=currency.name, lastPrice=last_price, lastChange=last_change, lastDate=last_date,
                   rates=rates_list)
