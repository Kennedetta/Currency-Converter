from flask import Flask, render_template, request
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
    if request.method == "GET":
        print(currencies)
        ending_amount = "Amount"
        return render_template("index.html", time=time, currencies=currencies, ending_amount=ending_amount)
    else:
        starting_currency = request.form.get("starting")
        ending_currency = request.form  .get("ending")

        starting_amount = int(request.form.get("starting_amount"))
        conversion_rate = rates[ending_currency.lower()] / rates[starting_currency.lower()]
        
        ending_amount = starting_amount * conversion_rate
        print(ending_amount)

        # starting_amount * 
        return render_template("index.html", time=time, currencies=currencies, ending_amount=ending_amount)