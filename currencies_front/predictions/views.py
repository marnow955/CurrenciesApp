from flask import Blueprint, render_template
from datetime import datetime, timedelta

from currenciesapp.predictions.forms import PredictionsForm


predictions = Blueprint('predictions', __name__, url_prefix='/prediction')

@predictions.route("/<int:currency_id>", methods=['GET', 'POST'])
def prediction(currency_id):
    pass