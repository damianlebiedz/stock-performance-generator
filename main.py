import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def load_closed_positions(file_path):
    return pd.read_csv(file_path, parse_dates=["data/CLOSED POSITION.csv"])

def load_open_positions(file_path):
    return pd.read_csv(file_path, parse_dates=["data/OPEN POSITION.csv"])

def fetch_market_data(symbols, start, end):
    data = yf.download(symbols, start=start, end=end)["Adj Close"]
    return data

def calculate_portfolio_value(closed_positions, open_positions, market_data):
    # TODO: Implementacja rekonstrukcji wartości portfela
    pass

def calculate_returns(portfolio_values):
    # TODO: Implementacja metryk zwrotu
    pass

def plot_performance(portfolio_values, sp500_data):
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_values.index, portfolio_values, label="Portfolio")
    plt.plot(sp500_data.index, sp500_data, label="S&P 500", linestyle="dashed")
    plt.legend()
    plt.title("Portfolio vs S&P 500")
    plt.xlabel("Data")
    plt.ylabel("Value")
    plt.savefig("performance.png")
    plt.show()

if __name__ == "__main__":
    closed_positions = load_closed_positions("data/CLOSED POSITION.csv.csv")
    open_positions = load_open_positions("data/OPEN POSITION.csv.csv")
    sp500_data = fetch_market_data(["^GSPC"], "2024-01-01", "2025-02-22")

    portfolio_values = calculate_portfolio_value(closed_positions, open_positions, sp500_data)
    calculate_returns(portfolio_values)
    plot_performance(portfolio_values, sp500_data)