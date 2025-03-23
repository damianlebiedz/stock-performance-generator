from modules.data_loader import load_closed_positions, load_open_positions, fetch_exchange_rates
from modules.portfolio_calculator import calculate_daily_portfolio_profit
#from modules.plot_generator import plot_daily_performance, plot_portfolio

if __name__ == "__main__":
    closed_positions = load_closed_positions("data/CLOSED POSITIONS.csv")

    exchange_rates = fetch_exchange_rates()
    symbols = closed_positions["Symbol"].unique().tolist()

    open_positions = load_open_positions("data/OPEN POSITIONS.csv", exchange_rates)

    #BŁĄD - do zrobienia
    portfolio_profit_df = calculate_daily_portfolio_profit(open_positions, closed_positions)
    print(portfolio_profit_df)