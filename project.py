import pandas as pd
import yfinance as yf
import math

# Step 1: Get S&P 500 tickers from Wikipedia
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
table = pd.read_html(sp500_url)
tickers = table[0]['Symbol'].tolist()

# Some tickers have a dot in them (e.g., BRK.B), replace with '-' for Yahoo Finance
tickers = [ticker.replace('.', '-') for ticker in tickers]

# Step 2: Input your portfolio value
portfolio_value = float(input("Enter the value of your portfolio (e.g., 10000): "))
equal_weight = portfolio_value / len(tickers)

# Step 3: Fetch all stock prices (this is where your line goes)
prices_df = yf.download(tickers, period="1d")["Close"].iloc[-1]

# Step 4: Calculate number of shares to buy for each stock
shares_to_buy = {}
for ticker in tickers:
    try:
        price = prices_df[ticker]
        quantity = math.floor(equal_weight / price)
        shares_to_buy[ticker] = quantity
    except KeyError:
        print(f"Price not found for {ticker}, skipping.")

# Step 5: Output the result
output_df = pd.DataFrame(list(shares_to_buy.items()), columns=["Ticker", "Shares to Buy"])
output_df.to_csv("equal_weight_portfolio.csv", index=False)
print("\nPortfolio allocation saved to equal_weight_portfolio.csv")
