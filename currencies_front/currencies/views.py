import requests
# from currencies_front.front_run import CURRENCIES_URL, RATES_URL
from flask import Blueprint, render_template

from currencies_front.currencies.forms import CurrencyForm

API_URL = 'http://localhost:5000/'
RATES_URL = API_URL + 'get_all_currency_rates'

currencies = Blueprint('currencies', __name__, url_prefix='/currency')


@currencies.route('/<string:currency_code>', methods=['GET', 'POST'])
def currency(currency_code):
    form = CurrencyForm()
    data = {
        "currencyCode": currency_code
    }
    if form.validate_on_submit():
        data["startDate"] = form.start_date.data.strftime('%Y-%m-%d')
        data["endDate"] = form.end_date.data.strftime('%Y-%m-%d')
    response = requests.post(RATES_URL, json=data)
    json = response.json()
    return render_template('currency.html', title=json['currencyName'], form=form, reports=json['rates'],
                           currency_name=json['currencyName'], currency_code=currency_code,
                           last_price=json['lastPrice'], last_change=json['lastChange'], last_date=json['lastDate'])
