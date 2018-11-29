from flask import Blueprint, render_template, request
from flask_cors import cross_origin
from datetime import datetime
import requests

# from currencies_front.front_run import CURRENCIES_URL

main = Blueprint('main', __name__)

API_URL = 'http://localhost:5000/'

CURRENCIES_URL = API_URL + 'get_currencies'


@main.route("/")
@main.route("/home")
@cross_origin()
def home():
    type = request.args.get('type', 'fiat', type=str)
    date = request.args.get('date', type=str)
    data = {"type": type}
    if date:
        data["date"] = date
    reports_data = requests.post(CURRENCIES_URL, json=data)
    reports = reports_data.json()
    print(reports)
    return render_template('home.html', reports=reports["currencies"], type=type, selected_date=reports['date'])
