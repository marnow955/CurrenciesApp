import requests
from currencies_front.front_run import CURRENCIES_URL, RATES_URL
from flask import Blueprint, render_template

from currencies_front.currencies.forms import CurrencyForm


currencies = Blueprint('currencies', __name__, url_prefix='/currency')


@currencies.route('/<string:currency_code>', methods=['GET', 'POST'])
def currency(currency_code):
    form = CurrencyForm()
    if form.validate_on_submit():
        reports = requests.post(RATES_URL, {type, "start_date": form.start_date, "end_date": form.end_date})
    return render_template('currency.html', title=curr.name, form=form, reports=reports, currency=currency_code, last=last)
