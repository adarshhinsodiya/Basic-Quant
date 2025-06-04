# Algo Trading Project

This repository contains Python scripts for algorithmic trading, including a portfolio backtester and other related projects.

## Files:

- `portfolio_backtester.py`: This script is a comprehensive S&P 500 portfolio backtester. It allows you to simulate different portfolio types (equal-weighted or market-cap-weighted approximation), filter by sector, enable monthly rebalancing, and specify start/end dates and initial capital. It downloads historical data, constructs the portfolio, calculates its value over time, compares it against an SPY benchmark, and provides performance metrics such as annual return, volatility, Sharpe ratio, and cumulative return. The results are visualized with a plot.

- `project1.py`: This script helps you create an equal-weighted S&P 500 index fund. It takes your total portfolio value as input and calculates the number of shares of each S&P 500 constituent you should purchase to achieve an equal-weighted allocation. It fetches current stock prices and outputs the recommended allocation to a CSV file named `equal_weight_portfolio.csv`.

- `project2.py`: This script performs a backtest comparing an equal-weighted S&P 500 portfolio against the SPY ETF (a market-cap-weighted S&P 500 benchmark). It simulates a $100,000 investment over a specified period (e.g., 2020-2025) for both strategies. The script downloads historical data, calculates the portfolio values over time, visualizes their performance with a plot, and provides key performance metrics like annual return, volatility, Sharpe ratio, and cumulative return for both the equal-weighted portfolio and SPY.

- `.gitignore`: Specifies intentionally untracked files to ignore, such as virtual environments, data files, or other temporary files.

## Setup

To set up the project, ensure you have Python installed. You will also need to install the required Python libraries. It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (you might need to create a requirements.txt file first, or install them individually)
pip install pandas yfinance numpy matplotlib 

#example on how to run the portfolio_backtester.py script
python portfolio_backtester.py --type "cap" --top "500" --sector "Health Care" --rebalance --start "2020-01-01" --end "2025-06-03" --capital "500000"

#example on how to run the project1.py script
python project1.py

#example on how to run the project2.py script
python project2.py

