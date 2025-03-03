import pandas as pd
from modules.data_loader import load_closed_positions, load_open_positions, fetch_exchange_rates, fetch_market_data
from modules.portfolio_calculator import calculate_daily_performance
from modules.plot_generator import plot_daily_performance

if __name__ == "__main__":
    closed_positions = load_closed_positions("data/CLOSED POSITION.csv")
    exchange_rates = fetch_exchange_rates()
    symbols = closed_positions["Symbol"].unique().tolist()
    market_data = fetch_market_data(symbols)

    open_positions = load_open_positions("data/OPEN POSITION.csv", market_data, exchange_rates)
    all_positions = pd.concat([closed_positions, open_positions])
    daily_performance = calculate_daily_performance(closed_positions, open_positions)
    plot_daily_performance(daily_performance)