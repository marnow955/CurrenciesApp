from time import sleep
from datetime import datetime
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from currenciesapp import db, create_app
from currenciesapp.data_models import Currency, CurrencyRates

currency_list = ["CHF", "GBP", "EUR", "USD", "SEK", "DKK"]
base_currency_code = "PLN"

url = 'https://www.bankier.pl/narzedzia/archiwum-kursow-walutowych'


def get_data(browser, currency_code, from_date=None):
    select_currency = Select(browser.find_element_by_id('currency'))
    select_currency.select_by_value(currency_code)

    select_date = Select(browser.find_element_by_id('set_date'))
    select_date.select_by_value('-1095')

    browser.find_element_by_id("archiwumKursowWalutSubmit").click()
    sleep(1)
    container = browser.find_element_by_class_name('hideTableRowContainer')
    container.find_element_by_class_name('showAllTableRow').click()
    sleep(1)
    table = container.find_element_by_class_name('show10TableRow')
    print(table)
    table_body = table.find_element_by_tag_name('tbody')
    data = []
    rows = table_body.find_elements_by_tag_name('tr')
    for row in rows:
        print(row)
        cols = row.find_elements_by_tag_name('td')
        cols = [ele.text.strip() for ele in cols]
        if from_date is None:
            data.append([ele for ele in cols if ele])
        else:
            date_str = cols[0]
            row_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if row_date > from_date:
                data.append([ele for ele in cols if ele])
            else:
                break
    print(data)
    return data


def get_archive(currency_list=None, from_last_date=False):
    # Chrome
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument('--load-extension='
    #                      'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\'
    #                      'jeoacafpbcihiomhlakheieifhpjdfeo\\5.18.23_0,'
    #                      'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\'
    #                      'cjpalhdlnbpafiamejdnhcphjbkeiagm\\1.17.0_0')
    options.add_argument('--load-extension='
                         'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\'
                         'cjpalhdlnbpafiamejdnhcphjbkeiagm\\1.17.0_0')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    # print(browser.page_source)

    for currency_code in currency_list:
        currency = Currency.query.filter_by(code=currency_code).first()
        if from_last_date:
            max_date = CurrencyRates.query.filter_by(currency=currency) \
                .order_by(CurrencyRates.date.desc()).first().date.date()
            data = get_data(browser, currency_code, max_date)
        else:
            data = get_data(browser, currency_code)
        for report in data:
            date_str, price_str, change_str, _ = report
            price_str = price_str.replace(',', '.')
            change_str = change_str.replace(',', '.')
            rdate = datetime.strptime(date_str, "%Y-%m-%d").date()
            rate = CurrencyRates(date=rdate, price=Decimal(price_str), change=Decimal(change_str),
                                 currency_code=currency.code, base_currency_code=base_currency_code)
            db.session.add(rate)
        db.session.commit()
        break  # DEV - TO REMOVE
    browser.quit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        get_archive(currency_list, False)
