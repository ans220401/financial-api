#!/usr/bin/env python3
import requests
import time

API_KEY = "IAJXDDF45X75TGIS"  # Replace with your own Alpha Vantage API key

def calculate_fair_value(eps, growth_rate):
    # (This demo formula multiplies EPS by the growth rate percentage.)
    return eps * growth_rate

def get_overview(ticker):
    """
    Retrieves the company's overview from Alpha Vantage.
    """
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching overview for {ticker}: status code {response.status_code}")
        return None
    data = response.json()
    # Uncomment the next line to inspect raw output:
    # print(f"Raw overview for {ticker}:", data)
    if not data or "EPS" not in data:
        print(f"Overview data missing or incomplete for {ticker}. Data received: {data}")
        return None
    return data

def get_current_price(ticker):
    """
    Retrieves the current stock price using the GLOBAL_QUOTE endpoint.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching global quote for {ticker}: status code {response.status_code}")
        return None
    data = response.json()
    try:
        price = float(data["Global Quote"]["05. price"])
        return price
    except Exception as e:
        print(f"Error parsing current price for {ticker}: {e}")
        return None

def main():
    tickers_input = input("Enter stock tickers separated by commas (e.g., AAPL, MSFT, AMZN): ")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
    
    if not tickers:
        print("No valid tickers provided. Exiting.")
        return
    
    print("\nCalculating fair values using Alpha Vantage...\n")
    
    for ticker in tickers:
        overview = get_overview(ticker)
        if not overview:
            print(f"Skipping {ticker} due to missing overview data.\n")
            continue
        
        # Get trailing EPS from the "EPS" field
        trailing_eps_val = overview.get("EPS")
        if trailing_eps_val is None:
            print(f"Data for {ticker} is missing trailing EPS. Skipping.\n")
            continue
        try:
            trailing_eps = float(trailing_eps_val)
        except Exception as e:
            print(f"Error parsing trailing EPS for {ticker}: {e}")
            continue
        if trailing_eps == 0:
            print(f"Trailing EPS for {ticker} is zero. Skipping.\n")
            continue
        
        # Try to get a forward measure.
        # Some tickers may include "ForwardEps", but if not, try using "EarningsGrowth"
        forward_eps_val = overview.get("ForwardEps")
        if forward_eps_val is not None:
            try:
                forward_eps = float(forward_eps_val)
                eps_growth_rate = (forward_eps / trailing_eps - 1) * 100
            except Exception as e:
                print(f"Error parsing Forward EPS for {ticker}: {e}")
                continue
        else:
            earnings_growth_val = overview.get("EarningsGrowth")
            if earnings_growth_val is not None:
                try:
                    # Assume the EarningsGrowth field is given as a percentage (e.g. 12 means 12%)
                    eps_growth_rate = float(earnings_growth_val)
                    print(f"Data for {ticker} is missing Forward EPS. Using Earnings Growth ({eps_growth_rate:.2f}%) instead.")
                except Exception as e:
                    print(f"Error parsing Earnings Growth for {ticker}: {e}")
                    continue
            else:
                print(f"Data for {ticker} is missing both Forward EPS and Earnings Growth. Skipping.\n")
                continue
        
        current_price = get_current_price(ticker)
        if current_price is None:
            print(f"Data for {ticker} is missing current price. Skipping.\n")
            continue
        
        fair_value = calculate_fair_value(trailing_eps, eps_growth_rate)
        
        print(f"Ticker: {ticker}")
        print(f"  Trailing EPS: {trailing_eps}")
        if forward_eps_val is not None:
            print(f"  Forward EPS: {forward_eps_val}")
            print(f"  Calculated EPS Growth Rate (from Forward EPS): {eps_growth_rate:.2f}%")
        else:
            print(f"  Earnings Growth (used as EPS Growth Rate): {eps_growth_rate:.2f}%")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  Calculated Fair Value: ${fair_value:.2f}")
        
        if fair_value > current_price:
            diff = fair_value - current_price
            print(f"  Suggestion: The stock may be undervalued by ${diff:.2f}.\n")
        elif fair_value < current_price:
            diff = current_price - fair_value
            print(f"  Suggestion: The stock may be overvalued by ${diff:.2f}.\n")
        else:
            print("  Suggestion: The stock appears to be fairly valued.\n")
        
        # Wait to respect rate limits (free API limit is 5 calls per minute)
        time.sleep(12)

if __name__ == '__main__':
    main()