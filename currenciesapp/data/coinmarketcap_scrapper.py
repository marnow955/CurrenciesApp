import urllib.request
from datetime import datetime
from decimal import Decimal

import bs4 as bs

from currenciesapp import db, create_app
from currenciesapp.data_models import Currency, CurrencyRates

coins = {"BTC": "bitcoin", "ETH": "ethereum", "XRP": "ripple",
         "BCH": "bitcoin-cash", "EOS": "eos"}
base_currency_code = "USD"
date = datetime.now().strftime("%y%m%d")


def get_data(coin, from_date=None):
    url = ('https://coinmarketcap.com/currencies/' + coin +
           '/historical-data/?start=20130428&end=20' + date)
    print(url)
    source = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(source, 'lxml')
    table = soup.find('table', attrs={'class': 'table'})
    table_body = table.find('tbody')
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if from_date is None:
            data.append([cols[i] for i in [0, 4]])
        else:
            date_str = cols[0]
            row_date = datetime.strptime(date_str, "%b %d, %Y").date()
            if row_date >= from_date:
                data.append([cols[i] for i in [0, 4]])
            else:
                break
    print(data)
    return data


def get_archive(from_last_date=False):
    for key, coin in coins.items():
        currency = Currency.query.filter_by(code=key).first()
        if from_last_date:
            max_date = CurrencyRates.query.filter_by(currency=currency) \
                .order_by(CurrencyRates.date.desc()).first().date.date()
            data = get_data(coin, max_date)[::-1]
        else:
            data = get_data(coin)[::-1]  # reverse
        for i, report in enumerate(data):
            if from_last_date and i is 0:
                continue
            date_str, price_str = report
            price_str = price_str.replace(',', '.')
            price = Decimal(price_str)
            rdate = datetime.strptime(date_str, "%b %d, %Y").date()
            if i is 0:
                change = 0.00
            else:
                price_before_str = data[i - 1][1]
                price_before = Decimal(price_before_str)
                change = round((price - price_before) * 100 / price_before, 2)
            report = CurrencyRates(date=rdate, price=Decimal(price_str), change=change,
                                   currency_code=currency.code, base_currency_code=base_currency_code)
            db.session.add(report)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        get_archive(False)
