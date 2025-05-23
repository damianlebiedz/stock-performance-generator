import pandas as pd
from modules.data_loader import load_file, merge_df, format_df, load_report_from_xlsx
from modules.generate_raport import save_combined_report
from modules.controller import comparison_ticker
from modules.load_comparison_data import load_comparison_asset
from modules.summary_loader import load_and_format_positions


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    while True:
        print('Are you using XStation5 report? (Y/n): ')
        x = input()
        if x == 'Y' or x == 'y':
            open_positions, closed_positions = load_report_from_xlsx()
            break
        elif x == 'N' or x == 'n':
            closed_positions = load_file("data/CLOSED POSITIONS.csv")
            open_positions = load_file("data/OPEN POSITIONS.csv")
            break

    positions = merge_df(closed_positions, open_positions)
    format_df(positions)

    summary = load_and_format_positions(positions)
    load_comparison_asset(comparison_ticker, summary)
    save_combined_report(summary)
