import math

import numpy

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout


def build_model(look_back, neurons=4, activ_func="linear",
                dropout=0.25, loss="mae", optimizer="adam"):
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(1, look_back)))
    model.add(Dropout(dropout))
    model.add(Dense(1))
    model.add(Activation(activ_func))
    model.compile(loss=loss, optimizer=optimizer)
    return model


def fit_model(model, train_x, train_y, epochs, batch_size):
    model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=2)
    return model


def make_prediction(model, train_x, test_x):
    trainPredict = model.predict(train_x)
    testPredict = model.predict(test_x)
    return trainPredict, testPredict


def invert_prediction(scaler, trainPredict, testPredict, train_y, test_y):
    trainPredict = scaler.inverse_transform(trainPredict)
    train_y = scaler.inverse_transform([train_y])
    testPredict = scaler.inverse_transform(testPredict)
    test_y = scaler.inverse_transform([test_y])
    return trainPredict, train_y, testPredict, test_y


def calculate_error(train_y, train_predict, test_y, testPredict):
    trainScore = math.sqrt(mean_squared_error(train_y[0], train_predict[:, 0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(test_y[0], testPredict[:, 0]))
    print('Test Score: %.2f RMSE' % (testScore))


def shift_train_prediction(dataset, look_back, trainPredict):
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    return trainPredictPlot


def shift_test_prediction(dataset, look_back, trainPredict, testPredict):
    testPredictPlot = numpy.empty_like(dataset)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict
    return testPredictPlot


def plot(scaler, dataset, trainPredictPlot, testPredictPlot):
    plt.plot(scaler.inverse_transform(dataset))
    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    plt.show()
