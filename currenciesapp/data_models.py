from datetime import datetime

from currenciesapp import db


class Currency(db.Model):
    code = db.Column(db.String(4), primary_key=True)  # size = 3 for fiat, min 4 for crypto
    name = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(30), nullable=False)  # fiat/crypto
    area = db.Column(db.String(30), nullable=True)
    rates = db.relationship('CurrencyRates', backref='currency', lazy=True,
                            primaryjoin="Currency.code == CurrencyRates.currency_code")

    def __repr__(self):
        return f"Currency('{self.code}' - '{self.name}' ({self.type}))"


class CurrencyRates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    base_currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Numeric(scale=4, decimal_return_scale=4), nullable=False)
    change = db.Column(db.Numeric(scale=2), nullable=False)

    def __repr__(self):
        return f"Report('{self.currency_code}' - '{self.date}' - '{self.price}', '{self.change}')"


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(30), nullable=False)
