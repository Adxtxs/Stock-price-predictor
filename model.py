import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
import tensorflow as tf

# Fetch stock data using yfinance
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    return df

# Create sequences for LSTM input
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

# To avoid retracing warnings
@tf.function
def predict_lstm(model, input_sequence):
    return model(input_sequence)

# Predict stock prices using LSTM
def predict_stock_price(symbol, start_date="2020-01-01", end_date=None):
    df = get_stock_data(symbol, start_date=start_date, end_date=end_date)

    if len(df) < 60:
        raise ValueError("Not enough data to make predictions. Please select a larger date range.")

    # Prepare data for LSTM
    df = df[['Open', 'High', 'Low', 'Close']]
    scaler = MinMaxScaler()
    df['Scaled_Close'] = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

    # Create sequences for LSTM
    seq_length = 60
    X, y = create_sequences(df['Scaled_Close'].values, seq_length)

    X = X.reshape(X.shape[0], X.shape[1], 1)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build LSTM model with an explicit Input layer
    model = Sequential([
        Input(shape=(seq_length, 1)),
        LSTM(50, return_sequences=True),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, verbose=0)

    lstm_predictions = model.predict(X_test)
    lstm_predictions = scaler.inverse_transform(lstm_predictions)

    last_sequence = X_test[-1].reshape(1, seq_length, 1)
    next_7_days = []

    for _ in range(7):
        lstm_pred = predict_lstm(model, last_sequence)[0][0].numpy()
        next_7_days.append(lstm_pred)
        last_sequence = np.roll(last_sequence, -1, axis=1)
        last_sequence[0, -1, 0] = lstm_pred

    next_7_days = scaler.inverse_transform(np.array(next_7_days).reshape(-1, 1))

    return {
        'symbol': symbol,
        'historical': df['Close'].tolist(),
        'predictions': next_7_days.flatten().tolist(),
        'details': {
            'open': df['Open'].tolist(),
            'high': df['High'].tolist(),
            'low': df['Low'].tolist()
        }
    }
