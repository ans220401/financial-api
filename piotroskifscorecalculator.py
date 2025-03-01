import re
from finvizfinance.quote import finvizfinance

def parse_value(val):
    """
    Clean and convert a string financial value to a float.
    Removes "$", "%", commas, and extra spaces.
    Returns None if conversion fails.
    """
    if isinstance(val, str):
        val = val.replace("$", "").replace("%", "").replace(",", "").strip()
        try:
            return float(val)
        except:
            return None
    return val

def calculate_piotroski_score(ticker):
    """
    Calculate the Piotroski F-Score using Finviz fundamental data.
    
    Expected keys in the returned Finviz dictionary are (if available):
      - "ROA" and "Prev ROA"
      - "Net Income" (current) 
      - "Operating Cash Flow" (current)
      - "Long Term Debt" and "Prev Long Term Debt"
      - "Current Ratio" and "Prev Current Ratio"
      - "Shares Outstanding" and "Prev Shares Outstanding"
      - "Gross Margin" and "Prev Gross Margin"
      - "Asset Turnover" and "Prev Asset Turnover"
      
    If a metric is missing, that criterion is set to 0.
    """
    # Initialize Finviz object and retrieve fundamentals
    stock = finvizfinance(ticker)
    data = stock.ticker_fundament()

    # Parse numerical values (convert percentage and currency strings)
    roa = parse_value(data.get("ROA"))
    prev_roa = parse_value(data.get("Prev ROA"))
    net_income = parse_value(data.get("Net Income"))
    operating_cash_flow = parse_value(data.get("Operating Cash Flow"))
    lt_debt = parse_value(data.get("Long Term Debt"))
    prev_lt_debt = parse_value(data.get("Prev Long Term Debt"))
    current_ratio = parse_value(data.get("Current Ratio"))
    prev_current_ratio = parse_value(data.get("Prev Current Ratio"))
    shares_outstanding = parse_value(data.get("Shares Outstanding"))
    prev_shares_outstanding = parse_value(data.get("Prev Shares Outstanding"))
    gross_margin = parse_value(data.get("Gross Margin"))
    prev_gross_margin = parse_value(data.get("Prev Gross Margin"))
    asset_turnover = parse_value(data.get("Asset Turnover"))
    prev_asset_turnover = parse_value(data.get("Prev Asset Turnover"))

    score = 0
    breakdown = {}

    # 1. ROA Positive: Score 1 if current ROA > 0
    if roa is not None:
        breakdown["ROA_Positive"] = 1 if roa > 0 else 0
    else:
        breakdown["ROA_Positive"] = 0
    score += breakdown["ROA_Positive"]

    # 2. Operating Cash Flow Positive: Score 1 if operating cash flow > 0
    if operating_cash_flow is not None:
        breakdown["CFO_Positive"] = 1 if operating_cash_flow > 0 else 0
    else:
        breakdown["CFO_Positive"] = 0
    score += breakdown["CFO_Positive"]

    # 3. ROA Improvement: Score 1 if current ROA > previous ROA
    if roa is not None and prev_roa is not None:
        breakdown["ROA_Change"] = 1 if roa > prev_roa else 0
    else:
        breakdown["ROA_Change"] = 0
    score += breakdown["ROA_Change"]

    # 4. Quality of Earnings: Score 1 if Operating Cash Flow > Net Income
    if operating_cash_flow is not None and net_income is not None:
        breakdown["Quality_Earnings"] = 1 if operating_cash_flow > net_income else 0
    else:
        breakdown["Quality_Earnings"] = 0
    score += breakdown["Quality_Earnings"]

    # 5. Debt Decrease: Score 1 if current Long Term Debt < previous Long Term Debt
    if lt_debt is not None and prev_lt_debt is not None:
        breakdown["Debt_Decrease"] = 1 if lt_debt < prev_lt_debt else 0
    else:
        breakdown["Debt_Decrease"] = 0
    score += breakdown["Debt_Decrease"]

    # 6. Current Ratio Improvement: Score 1 if current ratio > previous ratio
    if current_ratio is not None and prev_current_ratio is not None:
        breakdown["Current_Ratio_Change"] = 1 if current_ratio > prev_current_ratio else 0
    else:
        breakdown["Current_Ratio_Change"] = 0
    score += breakdown["Current_Ratio_Change"]

    # 7. No New Shares Issued: Score 1 if current shares outstanding <= previous shares outstanding
    if shares_outstanding is not None and prev_shares_outstanding is not None:
        breakdown["No_New_Shares"] = 1 if shares_outstanding <= prev_shares_outstanding else 0
    else:
        breakdown["No_New_Shares"] = 0
    score += breakdown["No_New_Shares"]

    # 8. Gross Margin Improvement: Score 1 if current gross margin > previous gross margin
    if gross_margin is not None and prev_gross_margin is not None:
        breakdown["Gross_Margin_Change"] = 1 if gross_margin > prev_gross_margin else 0
    else:
        breakdown["Gross_Margin_Change"] = 0
    score += breakdown["Gross_Margin_Change"]

    # 9. Asset Turnover Improvement: Score 1 if current asset turnover > previous asset turnover
    if asset_turnover is not None and prev_asset_turnover is not None:
        breakdown["Asset_Turnover_Change"] = 1 if asset_turnover > prev_asset_turnover else 0
    else:
        breakdown["Asset_Turnover_Change"] = 0
    score += breakdown["Asset_Turnover_Change"]

    return {
        "ticker": ticker,
        "f_score": score,
        "breakdown": breakdown,
        "data": data  # raw data for further inspection
    }

def print_f_score_analysis(result):
    print(f"\nPiotroski F-Score for {result['ticker']}: {result['f_score']}/9")
    print("-" * 50)
    criteria_desc = {
        "ROA_Positive": "Return on Assets is positive",
        "CFO_Positive": "Operating Cash Flow is positive",
        "ROA_Change": "ROA improved over previous period",
        "Quality_Earnings": "Operating Cash Flow exceeds Net Income",
        "Debt_Decrease": "Long Term Debt decreased",
        "Current_Ratio_Change": "Current Ratio improved",
        "No_New_Shares": "No new shares issued",
        "Gross_Margin_Change": "Gross Margin improved",
        "Asset_Turnover_Change": "Asset Turnover improved"
    }
    for key, passed in result["breakdown"].items():
        print(f"{'✓' if passed else '✗'} {criteria_desc.get(key, key)}")

if __name__ == "__main__":
    ticker = input("Enter ticker symbol (default GOOG): ") or "GOOG"
    result = calculate_piotroski_score(ticker)
    print_f_score_analysis(result)