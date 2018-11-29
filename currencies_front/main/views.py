from flask import Blueprint, render_template, request
from flask_cors import cross_origin
from datetime import datetime

from currenciesapp.models import Report, Currency

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@cross_origin()
def home():
    type = request.args.get('type', 'fiat', type=str)
    start_date = Report.query.join(Currency).filter(Currency.type == type).order_by(Report.date.asc()).first().date.date()
    end_date = Report.query.join(Currency).filter(Currency.type == type).order_by(Report.date.desc()).first().date.date()
    date = request.args.get('date', end_date.strftime('%Y-%m-%d'), type=str)
    reports = Report.query.join(Currency).filter(Currency.type == type).filter(Report.date == date).all()
    return render_template('home.html', reports=reports, type=type, selected_date=date)
