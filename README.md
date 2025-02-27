# Stock Price Predictor

## Description
This project is a web-based application that predicts stock prices using machine learning techniques. It combines historical stock data analysis with LSTM (Long Short-Term Memory) neural networks to forecast future stock prices.

## Why LSTM?
LSTM is used because it efficiently processes sequential stock price data, capturing long-term dependencies and trends for accurate forecasting. It predicts by learning patterns from historical prices, using past time steps as input to forecast future values while handling market fluctuations.

## Features
- Fetch historical stock data using Yahoo Finance API
- Predict stock prices using LSTM neural networks
- Visualize historical and predicted stock prices using Plotly
- Display additional stock details (Open, High, Low prices)

## Technologies Used
- Python 3.x
- Flask (Web Framework)
- TensorFlow (Machine Learning Library)
- Pandas (Data Manipulation)
- NumPy (Numerical Computing)
- yfinance (Yahoo Finance API)
- Plotly (Data Visualization)
- HTML/CSS/JavaScript (Frontend)

## Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/stock-price-predictor.git
cd stock-price-predictor
```

2. Create a virtual environment (optional but recommended):
```sh
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. Install the required packages:
```sh
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```sh
python app.py
```

2. Open a web browser and go to `http://localhost:5000`

3. Enter a stock symbol (e.g., AAPL for Apple Inc.), select a date range, and click "Predict"

4. View the historical and predicted stock prices on the interactive chart

Demo:


<img width="463" alt="image" src="https://github.com/user-attachments/assets/835ff6a5-98e1-4145-b171-0a1b0268818a" />


<img width="431" alt="image" src="https://github.com/user-attachments/assets/b466eb52-27a9-48f8-be1f-23f7c2a55184" />
