from modules.data_loader import *
from modules.stocks_loader import *
from modules.summary_loader import *
# from modules.plot_generator import *
# from modules.report_generator import *
# from dash import Dash


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    closed_positions = load_file("data/CLOSED POSITIONS.csv")
    open_positions = load_file("data/OPEN POSITIONS.csv")

    df = merge_df(closed_positions, open_positions)
    format_df(df)

    # unique_tickers = df['Formatted Symbol'].unique()
    unique_tickers = ['CCJ', 'UEC']

    all_stocks = all_stocks_information(unique_tickers, df)
    # summary = load_summary(all_stocks)

    print(all_stocks)
    # print(summary)

    # stock_plot(all_stocks)
    # summary_plot(summary)

    # app = generate_summary_report(summary)
    # app.run(debug=True, port=8050)