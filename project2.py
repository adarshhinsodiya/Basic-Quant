''' This Python script performs a backtest comparing an equal-weighted S&P 500 portfolio 
to the SPY ETF (market-cap-weighted S&P 500). It simulates how a $100,000 investment 
would have performed over a 5-year period (2020-2025) under two strategies and visualizes 
and evaluates their performance. '''

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# ----- Config -----
start_date = "2020-06-01"
end_date = "2025-06-01"
portfolio_value = 100000  # Starting capital
rebalance = False         # Optional: monthly rebalance

# ----- Step 1: Get S&P 500 Tickers -----
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tickers = pd.read_html(sp500_url)[0]['Symbol'].tolist()
tickers = [ticker.replace('.', '-') for ticker in tickers]

# Limit for demo or API speed
tickers = tickers[:100]  # Use top 100 to avoid overload

equal_weight = 1 / len(tickers)

# ----- Step 2: Download historical data -----
data = yf.download(tickers + ["SPY"], start=start_date, end=end_date)["Close"]

# Drop any stocks with missing data
data = data.dropna(axis=1)

# Update tickers list to only those with full data
tickers = [ticker for ticker in tickers if ticker in data.columns]

# ----- Step 3: Equal-weight Portfolio Value -----
initial_investment = portfolio_value * equal_weight
initial_prices = data.iloc[0][tickers]
initial_shares = initial_investment // initial_prices

# Calculate portfolio value over time
portfolio_history = (data[tickers] * initial_shares).sum(axis=1)

# ----- Step 4: SPY Benchmark -----
spy_shares = portfolio_value // data["SPY"].iloc[0]
spy_history = data["SPY"] * spy_shares

# ----- Step 5: Plot Performance -----
plt.figure(figsize=(12, 6))
portfolio_history.plot(label="Equal-Weight Portfolio")
spy_history.plot(label="SPY (Cap-Weight Benchmark)")
plt.title("Equal-Weight vs. SPY Performance")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True)
plt.show()

# ----- Step 6: Performance Metrics -----
def calculate_metrics(returns):
    annual_return = np.mean(returns) * 252
    volatility = np.std(returns) * np.sqrt(252)
    sharpe = annual_return / volatility
    cumulative = (1 + returns).cumprod()[-1] - 1
    return round(annual_return, 4), round(volatility, 4), round(sharpe, 4), round(cumulative, 4)

portfolio_returns = portfolio_history.pct_change().dropna()
spy_returns = spy_history.pct_change().dropna()

p_metrics = calculate_metrics(portfolio_returns)
s_metrics = calculate_metrics(spy_returns)

print("\n📊 Performance Metrics")
print("Metric                 Equal-Weight     SPY")
print(f"Annual Return         {p_metrics[0]:<18} {s_metrics[0]}")
print(f"Volatility            {p_metrics[1]:<18} {s_metrics[1]}")
print(f"Sharpe Ratio          {p_metrics[2]:<18} {s_metrics[2]}")
print(f"Cumulative Return     {p_metrics[3]:<18} {s_metrics[3]}")
