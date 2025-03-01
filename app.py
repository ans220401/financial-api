from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import functions from your 11 calculator files
from fairvalue import calculate_fair_value
from roe import get_stock_roe
from pe import get_pe_ratio
from beta import get_beta
from roa import get_stock_roa
from revenue_growth import get_stock_revenue_growth
from fcf import get_stock_pfcf
from ps import get_price_sales
from operatingmargin import get_operating_margin
from pricebook import get_price_book
from currentratio import get_current_ratio

app = Flask(__name__)
CORS(app)  # Enable CORS so that your API can be accessed from Squarespace

@app.route("/analyze", methods=["GET"])
def analyze():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Stock ticker is required"}), 400

    results = {
        "ticker": ticker,
        "fair_value": calculate_fair_value(0, 0),  # Adjust parameters as needed
        "roe": get_stock_roe(ticker),
        "pe_ratio": get_pe_ratio(ticker),
        "beta": get_beta(ticker),
        "roa": get_stock_roa(ticker),
        "revenue_growth": get_stock_revenue_growth(ticker),
        "free_cash_flow": get_stock_pfcf(ticker),
        "price_to_sales": get_price_sales(ticker),
        "operating_margin": get_operating_margin(ticker),
        "price_to_book": get_price_book(ticker),
        "current_ratio": get_current_ratio(ticker)
    }
    return jsonify(results)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Financial API!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))