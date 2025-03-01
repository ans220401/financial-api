import requests
from bs4 import BeautifulSoup

def get_pe_ratio(ticker: str) -> str:
    """
    Scrapes Finviz to retrieve the Price/Earnings (P/E) ratio for the given stock ticker.
    """
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}  # Finviz requires a user-agent header
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching page for {ticker}: status code {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", class_="snapshot-table2")
    if not table:
        print("Could not find the snapshot table on Finviz.")
        return None

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        # Iterate in key-value pairs
        for i in range(0, len(cells), 2):
            key = cells[i].text.strip()
            value = cells[i+1].text.strip() if i+1 < len(cells) else ""
            if key == "P/E":
                return value

    print(f"P/E ratio not found for ticker: {ticker}")
    return None

if __name__ == "__main__":
    print("Press 'exit' or 'quit' to stop.")
    while True:
        ticker = input("Enter a stock ticker (e.g., AAPL): ").upper().strip()
        if ticker.lower() in ['exit', 'quit']:
            print("Exiting...")
            break
        pe_ratio = get_pe_ratio(ticker)
        if pe_ratio:
            print(f"P/E ratio for {ticker} is: {pe_ratio}\n")
        else:
            print("Unable to retrieve P/E ratio. Please check the ticker and try again.\n")