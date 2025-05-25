from modules.data_loader import load_file, merge_df, format_df, load_report_from_xlsx
from modules.generate_raport import save_combined_report
from modules.controller import comparison_ticker
from modules.load_comparison_data import load_comparison_asset
from modules.summary_loader import load_and_format_positions


def main():
    try:
        while True:
            print('Are you using XStation5 report? (Y/n):')
            x = input()
            if x.lower() == 'y':
                open_positions, closed_positions = load_report_from_xlsx()
                break
            elif x.lower() == 'n':
                closed_positions = load_file("data/CLOSED POSITIONS.csv")
                open_positions = load_file("data/OPEN POSITIONS.csv")
                break
            else:
                print("Please type 'Y' or 'n'.")

        positions = merge_df(closed_positions, open_positions)
        format_df(positions)

        summary = load_and_format_positions(positions)
        load_comparison_asset(comparison_ticker, summary)
        save_combined_report(summary)

    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
