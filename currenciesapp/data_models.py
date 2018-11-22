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


class ReportCurrency(db.Model):
    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)


class Hparams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    neurons_num = db.Column(db.Integer, nullable=False)
    activ_func = db.Column(db.String(25), nullable=False)
    hid_layer_size = db.Column(db.Integer, nullable=False)
    dropout = db.Column(db.Numeric(scale=4, decimal_return_scale=4), nullable=False)
    loss_func = db.Column(db.String(25), nullable=False)
    optimizer = db.Column(db.String(25), nullable=False)


class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)
    model_params_id = db.Column(db.Integer, db.ForeignKey('hparams.id'), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Numeric(scale=4, decimal_return_scale=4), nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)


class Favourites(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    currency_code = db.Column(db.String(4), db.ForeignKey('currency.code'), nullable=False)


class ExchangeOffices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    rank = db.Column(db.Integer)


class Address(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('exchange_offices.id'), unique=True, nullable=False)
    country = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    street = db.Column(db.String(150), nullable=False)
    street_num = db.Column(db.Integer)
    flat_num = db.Column(db.Integer)
    postal_code = db.Column(db.String(10))


class UserComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exchange_office_id = db.Column(db.Integer, db.ForeignKey('exchange_offices.id'), nullable=False)
    comment = db.Column(db.Text(), nullable=False)
