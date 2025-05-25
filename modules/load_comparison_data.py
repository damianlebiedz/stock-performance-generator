import logging
from modules.controller import comparison_ticker
from modules.summary_loader import download_price

purchase_value = {}

def load_comparison_asset(ticker, summary):
    global purchase_value
    for index, row in summary.iterrows():
        date = row['Date']
        first_index = summary.index[0]
        try:
            stock_price = download_price(ticker, date)

            if index == first_index:
                purchase_value = stock_price
            summary.loc[index, f'Total change [%] of {comparison_ticker}'] = (
                    (stock_price / purchase_value - 1) * 100)

        except Exception as e:
            logging.error(f"Error retrieving data for {ticker} on {date}: {e}")
            summary.loc[index, f'Total change [%] of {comparison_ticker}'] = None
            continue