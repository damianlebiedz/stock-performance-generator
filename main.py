import pandas as pd
from modules.data_loader import load_file, merge_df, format_df
from modules.stocks_loader import all_stocks_information
from modules.summary_loader import load_summary
from modules.generate_raport import save_combined_report


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    closed_positions = load_file("data/CLOSED POSITIONS.csv")
    open_positions = load_file("data/OPEN POSITIONS.csv")

    df = merge_df(closed_positions, open_positions)
    format_df(df)

    unique_tickers = df['Formatted Symbol'].unique()

    all_stocks = all_stocks_information(unique_tickers, df)
    summary = load_summary(all_stocks)

    save_combined_report(summary, all_stocks)
