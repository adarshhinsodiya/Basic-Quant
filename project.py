import yfinance as yf
import pandas as pd
import math

def get_sp500_tickers():
    # Scrape S&P 500 tickers from Wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)
    df = table[0]
    return df['Symbol'].tolist()

def get_latest_prices(tickers):
    prices = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).history(period="1d")
            price = data['Close'].iloc[-1]
            prices[ticker] = price
        except Exception as e:
            print(f"Could not fetch price for {ticker}: {e}")
    return prices

def calculate_share_allocation(portfolio_value, prices):
    n = len(prices)
    equal_allocation = portfolio_value / n
    shares_to_buy = {}

    for ticker, price in prices.items():
        if price > 0:
            shares = math.floor(equal_allocation / price)
            shares_to_buy[ticker] = shares
        else:
            shares_to_buy[ticker] = 0

    return shares_to_buy

def main():
    try:
        portfolio_value = float(input("Enter your portfolio value in USD: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    print("Fetching S&P 500 tickers...")
    tickers = get_sp500_tickers()

    print("Fetching latest stock prices...")
    prices = get_latest_prices(tickers)

    print("Calculating share allocation...")
    allocation = calculate_share_allocation(portfolio_value, prices)

    # Print a preview
    df = pd.DataFrame(list(allocation.items()), columns=["Ticker", "Shares to Buy"])
    print(df[df["Shares to Buy"] > 0].sort_values("Shares to Buy", ascending=False).head(10))

    # Save to CSV
    df.to_csv("equal_weight_allocation.csv", index=False)
    print("Saved full allocation plan to 'equal_weight_allocation.csv'")

if __name__ == "__main__":
    main()
