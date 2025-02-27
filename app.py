from flask import Flask, render_template, request, jsonify
from model import predict_stock_price

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        try:
            predictions = predict_stock_price(symbol, start_date, end_date)
            return jsonify(predictions)
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
