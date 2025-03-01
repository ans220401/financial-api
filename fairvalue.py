#!/usr/bin/env python3

import yfinance as yf

def calculate_fair_value(eps, growth_rate):
 
    return eps * growth_rate

def get_eps_growth_rate(info, ticker):
  
    forward_eps = info.get("forwardEps")
    trailing_eps = info.get("trailingEps")
    if forward_eps is not None and trailing_eps is not None and trailing_eps != 0:
        growth_rate = (forward_eps / trailing_eps - 1) * 100
        return growth_rate
    earnings_growth = info.get("earningsGrowth")
    if earnings_growth is not None:
        return earnings_growth * 100
    print(f"Data for {ticker} is missing EPS growth information.")
    return None

def get_current_price(stock, info, ticker):
   
    current_price = info.get("regularMarketPrice") or info.get("currentPrice")
    if current_price is None:
        try:
            history = stock.history(period="1d")
            if not history.empty:
                current_price = history["Close"].iloc[-1]
        except Exception as e:
            print(f"Error retrieving historical price for {ticker}: {e}")
            current_price = None
    return current_price

def main():
    tickers_input = input("Enter stock tickers separated by commas (e.g., AAPL, MSFT, AMZN): ")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
    
    if not tickers:
        print("No valid tickers provided. Exiting.")
        return
    
    print("\nCalculating fair values...\n")
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        trailing_eps = info.get("trailingEps")
        if trailing_eps is None:
            print(f"Data for {ticker} is missing trailing EPS. Skipping.\n")
            continue
        
        eps_growth_rate = get_eps_growth_rate(info, ticker)
        if eps_growth_rate is None:
            print(f"Data for {ticker} is missing EPS growth rate. Skipping.\n")
            continue
        
        current_price = get_current_price(stock, info, ticker)
        if current_price is None:
            print(f"Data for {ticker} is missing current price. Skipping.\n")
            continue
        
        fair_value = calculate_fair_value(trailing_eps, eps_growth_rate)
        
        print(f"Ticker: {ticker}")
        print(f"  Trailing EPS: {trailing_eps}")
        print(f"  Calculated EPS Growth Rate: {eps_growth_rate:.2f}%")
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
    
if __name__ == '__main__':
    main()
