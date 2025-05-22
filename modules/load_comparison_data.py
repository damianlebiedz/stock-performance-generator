import yfinance as yf
import logging
from datetime import timedelta
from modules.controller import comparison_ticker

purchase_value = {}

def load_comparison_asset(ticker, summary):
    global purchase_value
    for index, row in summary.iterrows():
        date = row['Date']
        first_index = summary.index[0]
        try:
            data = yf.download(
                ticker,
                start=date.strftime('%Y-%m-%d'),
                end=(date + timedelta(days=1)).strftime('%Y-%m-%d'),
                auto_adjust=False,
                progress=False
            )
            stock_price = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else data['Close'].iloc[
                0].item()
            if index == first_index:
                purchase_value = stock_price
            summary.loc[index, f'Total change [%] of {comparison_ticker}'] = (
                    (stock_price / purchase_value - 1) * 100)


        except Exception as e:
            logging.error(f"Error retrieving data for {ticker} on {date}: {e}")
            summary.loc[index, f'Total change [%] of {comparison_ticker}'] = None
            continue