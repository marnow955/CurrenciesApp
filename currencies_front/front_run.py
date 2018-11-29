from currencies_front import create_app

API_URL = 'http://localhost:5000/'

CURRENCIES_URL = API_URL + 'get_currencies'
RATES_URL = API_URL + 'get_all_currency_rates'
PREDICTION_URL = API_URL + 'prediction'
GET_FAVOURITIES_URL = API_URL + 'favourities/get_favourities'
ADD_FAVOURITIES_URL = API_URL + 'favourities/add_to_favourities'


app = create_app()

if __name__ == '__main__':
    app.run(port=8080)
