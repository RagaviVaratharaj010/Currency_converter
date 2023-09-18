from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

# Read currency data from JSON file
with open('currencies.json') as file:
    currency_data = json.load(file)


@app.route('/')
def home():
    return render_template('index.html', currencies=currency_data)


@app.route('/convert', methods=['POST'])
def convert():
    amount = float(request.form['amount'])
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    # activated_currencies = [currency for currency in currency_data if currency['activated']]


    # Fetch the exchange rates from a public API
    url = f'https://open.er-api.com/v6/latest/{from_currency}'
    response = requests.get(url)
    data = response.json()
    rate = data['rates'][to_currency]
    # rate = None
    # for currency in activated_currencies:
    #     if currency['code'] == to_currency:
    #         rate = data['rates'][to_currency]
    #         break
    #
    #     if rate is None:
    #         return render_template('index.html', currencies=currency_data, error='Selected currency is  not activated.')

    # Perform the currency conversion
    converted_amount = amount * rate

    return render_template('index.html', currencies=currency_data, result=converted_amount, amount=amount, to_currency=to_currency, from_currency=from_currency)


@app.route('/activate', methods=['POST'])
def activate():
    currency_code = request.form['currency_code']

    # Update the activation status of the selected currency
    for currency in currency_data:
        if currency['code'] == currency_code:
            currency['activated'] = True
            break

    # Save the updated currency data to the JSON file
    with open('currencies.json', 'w') as file:
        json.dump(currency_data, file)

    return render_template('index.html', currencies=currency_data,)


@app.route('/deactivate', methods=['POST'])
def deactivate():
    currency_code = request.form['currency_code']

    # Update the activation status of the selected currency
    for currency in currency_data:
        if currency['code'] == currency_code:
            currency['activated'] = False
            break

    # Save the updated currency data to the JSON file
    with open('currencies.json', 'w') as file:
       json.dump(currency_data, file)

    return render_template('index.html', currencies=currency_data)


if __name__ == '__main__':
    app.run(debug=True, port=7000)