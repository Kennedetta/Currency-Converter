from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Parse API data
url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json"
response = requests.get(url)
print(response)
if response.status_code == 200:
    data = response.json()
    time = data["date"]
    rates = data["eur"]

@app.route('/test', methods=["GET"])
        
@app.route('/', methods=["GET", "POST"])
def index():
    currencies = [c.upper() for c in rates.keys()]

    starting = request.args.get("starting")
    ending = request.args.get("ending")
    starting_amount = request.args.get("starting_amount")

    # If no query params, render the main HTML page
    if not (starting and ending and starting_amount):
        return render_template("index.html", time=time, currencies=currencies, ending_amount="Amount")

    # If query params exist (i.e. fetch request)
    starting_amount = float(starting_amount)
    conversion_rate = rates[ending.lower()] / rates[starting.lower()]
    ending_amount = starting_amount * conversion_rate

    # Finding previous dates to feed into the API
    today = datetime.today()
    exchange_dates = []

    for i in range(7):
        day = today - timedelta(weeks=i)
        exchange_dates.append(day.strftime("%Y-%m-%d"))

    exchange_dates.reverse()
    prices = []

    for i in range(7):
        data = (requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{exchange_dates[i]}/v1/currencies/eur.json").json())
        new_rates = data["eur"]
        converted_rate = new_rates[ending.lower()] / new_rates[starting.lower()]
        ending_amount = starting_amount * converted_rate
        prices.append(ending_amount)

    return jsonify({"converted": ending_amount, "rate": conversion_rate, "exchange_dates": exchange_dates, "prices": prices})