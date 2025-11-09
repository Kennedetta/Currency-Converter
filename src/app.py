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

    return jsonify({"converted": ending_amount, "rate": conversion_rate})