from modules.data_loader import load_file, merge_df, format_df, load_currencies, load_timeframe, load_stock_history
from modules.plot_generator import plot_daily_performance

if __name__ == "__main__":
    closed_positions = load_file("data/CLOSED POSITIONS.csv")
    open_positions = load_file("data/OPEN POSITIONS.csv")

    df = merge_df(closed_positions, open_positions)
    format_df(df)

    currencies = load_currencies(df)
    timeframe = load_timeframe(df)

    load_stock_history(timeframe, df)
    print(timeframe)
    print(timeframe.dtypes)

    plot_daily_performance(timeframe)