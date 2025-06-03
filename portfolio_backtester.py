import argparse
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ----- CLI Parameters -----
parser = argparse.ArgumentParser(description="S&P 500 Portfolio Backtester")
parser.add_argument("--type", choices=["equal", "cap"], default="equal", help="Portfolio type")
parser.add_argument("--top", type=int, default=100, help="Top N stocks by market cap (default: 100)")
parser.add_argument("--sector", type=str, help="Filter by sector name (e.g. Information Technology)")
parser.add_argument("--rebalance", action="store_true", help="Enable monthly rebalancing")
parser.add_argument("--start", type=str, default="2020-06-01", help="Start date")
parser.add_argument("--end", type=str, default=datetime.today().strftime('%Y-%m-%d'), help="End date")
parser.add_argument("--capital", type=float, default=100000, help="Initial portfolio value")
args = parser.parse_args()

# ----- Step 1: Get S&P 500 Tickers -----
print("📥 Fetching S&P 500 data...")
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
table = pd.read_html(sp500_url)[0]

if args.sector:
    table = table[table['GICS Sector'] == args.sector]

tickers = table['Symbol'].tolist()
tickers = [ticker.replace('.', '-') for ticker in tickers][:args.top]

# ----- Step 2: Download Historical Data -----
print("📈 Downloading stock price data...")
data = yf.download(tickers + ["SPY"], start=args.start, end=args.end)["Close"]
data = data.dropna(axis=1)
tickers = [t for t in tickers if t in data.columns]

# ----- Step 3: Initial Portfolio Setup -----
print("💰 Constructing portfolio...")
initial_prices = data.iloc[0][tickers]

if args.type == "equal":
    weights = np.repeat(1 / len(tickers), len(tickers))
else:  # Cap-weighted approximation using price as proxy
    weights = initial_prices / initial_prices.sum()

initial_investment = args.capital * weights
initial_shares = initial_investment // initial_prices

# ----- Step 4: Portfolio Value Over Time -----
if not args.rebalance:
    portfolio_history = (data[tickers] * initial_shares).sum(axis=1)
else:
    print("🔁 Applying monthly rebalancing...")
    monthly = data[tickers].resample("M").first()
    shares = pd.DataFrame(index=monthly.index, columns=tickers)

    for date in monthly.index:
        prices = monthly.loc[date]
        weights = weights / weights.sum()  # Normalize in case of cap-weight drift
        investment = args.capital * weights
        shares.loc[date] = investment // prices

    shares = shares.ffill()
    monthly_value = (monthly * shares).sum(axis=1)
    portfolio_history = monthly_value.reindex(data.index, method="ffill")

# ----- Step 5: SPY Benchmark -----
spy_shares = args.capital // data["SPY"].iloc[0]
spy_history = data["SPY"] * spy_shares

# ----- Step 6: Plot -----
plt.figure(figsize=(12, 6))
portfolio_history.plot(label="Your Portfolio")
spy_history.plot(label="SPY (Cap-Weighted)")
plt.title(f"{args.type.capitalize()} Portfolio vs. SPY")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True)
plt.show()

# ----- Step 7: Performance Metrics -----
def metrics(returns):
    ann_return = np.mean(returns) * 252
    volatility = np.std(returns) * np.sqrt(252)
    sharpe = ann_return / volatility
    cumulative = (1 + returns).prod() - 1
    return round(ann_return, 4), round(volatility, 4), round(sharpe, 4), round(cumulative, 4)

p_returns = portfolio_history.pct_change().dropna()
s_returns = spy_history.pct_change().dropna()

p_metrics = metrics(p_returns)
s_metrics = metrics(s_returns)

print("\n📊 Performance Metrics")
print("Metric               Portfolio       SPY")
print(f"Annual Return       {p_metrics[0]:<15} {s_metrics[0]}")
print(f"Volatility          {p_metrics[1]:<15} {s_metrics[1]}")
print(f"Sharpe Ratio        {p_metrics[2]:<15} {s_metrics[2]}")
print(f"Cumulative Return   {p_metrics[3]:<15} {s_metrics[3]}")
