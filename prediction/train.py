import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from prediction import model
from currenciesapp.data_models import CurrencyRates
from currenciesapp import db, create_app


def create_dataset(dataset, look_back=1):
    data_x, data_y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        data_x.append(a)
        data_y.append(dataset[i + look_back, 0])
    return np.array(data_x), np.array(data_y)


def prepare_data(from_date, to_date, currency, split_ratio, look_back):
    currency_data = db.session.query(CurrencyRates).filter_by(currency_code=currency)
    prices_df = pd.DataFrame([(data.price, data.date) for data in currency_data])
    prices_df = prices_df[(prices_df[1] < to_date)]
    dataset = prices_df[0].values.astype('float32')
    dataset = np.reshape(prices_df[0], (len(dataset), 1))
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    train_size = int(len(dataset) * split_ratio)
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    train_x, train_y = create_dataset(train, look_back)
    test_x, test_y = create_dataset(test, look_back)
    train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))
    return train_x, test_x, train_y, test_y, scaler, dataset


def train_and_predict(currency, from_date, to_date, neurons=4,
                      activ_func="linear", split_ratio=0.95, epochs=20,
                      batch_size=2, look_back=5, optimizer="adam"):

    train_x, test_x, train_y, test_y, scaler, dataset = prepare_data(
        from_date, to_date, currency, split_ratio, look_back)
    model_t = model.build_model(look_back, activ_func=activ_func, neurons=neurons,
                              optimizer=optimizer)
    model_t = model.fit_model(model_t, train_x, train_y, epochs, batch_size)
    train_predict, test_predict = model.make_prediction(model_t, train_x, test_x)
    train_predict, train_y, test_predict, test_y = model.invert_prediction(
        scaler, train_predict, test_predict, train_y, test_y)
    return train_predict, test_predict


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        print(train_and_predict('BTC', "2018-05-01", "2018-06-01"))
