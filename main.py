from modules.data_loader import *
from modules.stocks_loader import *
from modules.summary_loader import *
from modules.plot_generator import *

if __name__ == "__main__":
    closed_positions = load_file("data/CLOSED POSITIONS.csv")
    open_positions = load_file("data/OPEN POSITIONS.csv")

    df = merge_df(closed_positions, open_positions)
    format_df(df)

    unique_tickers = df['Formatted Symbol'].unique()

    all_stocks = all_stocks_information(unique_tickers, df)
    summary = load_summary(all_stocks)

    stock_plot(all_stocks)
    summary_plot(summary)