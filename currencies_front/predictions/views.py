import requests

from flask import Blueprint, render_template
from datetime import datetime, timedelta

from currencies_front.predictions.forms import PredictionsForm

API_URL = 'http://localhost:5000/'
PREDICTION_URL = API_URL + 'prediction'

predictions = Blueprint('predictions', __name__, url_prefix='/prediction')


@predictions.route("/<string:currency_code>", methods=['GET', 'POST'])
def prediction(currency_code):
    form = PredictionsForm()
    data = {
        "currencyCode": currency_code
    }
    if form.validate_on_submit():
        data["startDate"] = form.start_date.data.strftime('%Y-%m-%d')
        data["endDate"] = form.end_date.data.strftime('%Y-%m-%d')
    response = requests.post(PREDICTION_URL, json=data)
    json = response.json()
    rates = json['rates']
    return render_template('prediction.html', title='Predykcja', form=form, reports_predictions=json['rates'],
                           currency_name=json['currencyName'], currency_code=currency_code,
                           last_price=json['lastPrice'], last_change=json['lastChange'], last_date=json['lastDate'])
