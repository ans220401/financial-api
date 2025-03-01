#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import your calculators
from beta import get_beta
from currentratio import get_current_ratio
from debttoequity import get_debt_to_equity
from fcf import get_stock_pfcf        # Free Cash Flow calculator
from operatingmargin import get_operating_margin
from pricebook import get_price_book
from ps import get_price_sales
from revenue_growth import get_stock_revenue_growth
from roa import get_stock_roa   # Return on Assets calculator
from roe import get_stock_roe   # Return on Equity calculator
from grossmargin import get_stock_gross_margin  # Gross Margin calculator

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Financial Metrics API!"})

@app.route("/analyze", methods=["GET"])
def analyze_stock():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Ticker parameter is required"}), 400
    ticker = ticker.upper()
    results = {}

    try:
        results["beta"] = get_beta(ticker)
    except Exception as e:
        results["beta"] = f"Error: {str(e)}"

    try:
        results["current_ratio"] = get_current_ratio(ticker)
    except Exception as e:
        results["current_ratio"] = f"Error: {str(e)}"

    try:
        results["free_cash_flow"] = get_stock_pfcf(ticker)
    except Exception as e:
        results["free_cash_flow"] = f"Error: {str(e)}"

    try:
        results["operating_margin"] = get_operating_margin(ticker)
    except Exception as e:
        results["operating_margin"] = f"Error: {str(e)}"

    try:
        results["price_to_book"] = get_price_book(ticker)
    except Exception as e:
        results["price_to_book"] = f"Error: {str(e)}"

    try:
        results["price_to_sales"] = get_price_sales(ticker)
    except Exception as e:
        results["price_to_sales"] = f"Error: {str(e)}"

    try:
        results["revenue_growth"] = get_stock_revenue_growth(ticker)
    except Exception as e:
        results["revenue_growth"] = f"Error: {str(e)}"

    try:
        results["roa"] = get_stock_roa(ticker)
    except Exception as e:
        results["roa"] = f"Error: {str(e)}"

    try:
        results["roe"] = get_stock_roe(ticker)
    except Exception as e:
        results["roe"] = f"Error: {str(e)}"

    # Replace fair value with Gross Margin
    try:
        results["gross_margin"] = get_stock_gross_margin(ticker)
    except Exception as e:
        results["gross_margin"] = f"Error: {str(e)}"

    # Replace P/E with Debt to Equity
    try:
        results["debt_to_equity"] = get_debt_to_equity(ticker)
    except Exception as e:
        results["debt_to_equity"] = f"Error: {str(e)}"

    results["ticker"] = ticker

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))