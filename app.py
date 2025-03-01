from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_stock_gross_margin(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch data for {ticker}"}

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", class_="snapshot-table2")

    if not table:
        return {"error": "Snapshot table not found"}

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        for i in range(0, len(cells), 2):
            key = cells[i].text.strip()
            value = cells[i+1].text.strip() if i+1 < len(cells) else ""
            if key == "Gross Margin":
                return {"ticker": ticker, "gross_margin": value}

    return {"error": f"Gross Margin not found for {ticker}"}

@app.route("/gross_margin", methods=["GET"])
def gross_margin_api():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Stock ticker is required"}), 400

    result = get_stock_gross_margin(ticker)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)