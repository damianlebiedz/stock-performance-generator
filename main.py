# import pandas as pd

from modules.data_loader import load_file, merge_df, format_df, load_report_from_xlsx
from modules.stocks_loader import all_stocks_information
from modules.summary_loader import load_summary
from modules.generate_raport import save_combined_report
from modules.controller import XStation5


if __name__ == "__main__":
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    if XStation5 is True:
        load_report_from_xlsx()

    elif XStation5 is False:
        closed_positions = load_file("data/CLOSED POSITIONS.csv")
        open_positions = load_file("data/OPEN POSITIONS.csv")
    else:
        raise Exception("Set XStation5 flag in modules/controller.py file.")

    # closed_positions = load_file("data/CLOSED POSITIONS.csv")
    # open_positions = load_file("data/OPEN POSITIONS.csv")
    #
    # df = merge_df(closed_positions, open_positions)
    # format_df(df)
    #
    # unique_tickers = df['Formatted Symbol'].unique()
    #
    # all_stocks = all_stocks_information(unique_tickers, df)
    # summary = load_summary(all_stocks)
    #
    # save_combined_report(summary, all_stocks)
