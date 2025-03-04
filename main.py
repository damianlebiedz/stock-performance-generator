from modules.data_loader import load_closed_positions, load_open_positions, fetch_exchange_rates, fetch_market_data
from modules.portfolio_calculator import calculate_daily_performance, calculate_portfolio
from modules.plot_generator import plot_daily_performance, plot_portfolio

if __name__ == "__main__":
    closed_positions = load_closed_positions("data/CLOSED POSITIONS.csv")

    exchange_rates = fetch_exchange_rates()
    symbols = closed_positions["Symbol"].unique().tolist()
    market_data = fetch_market_data(symbols)

    open_positions = load_open_positions("data/OPEN POSITIONS.csv", market_data, exchange_rates)

    grouped_data = calculate_portfolio(open_positions)
    plot_portfolio(grouped_data)

    daily_performance = calculate_daily_performance(closed_positions, open_positions)
    plot_daily_performance(daily_performance)