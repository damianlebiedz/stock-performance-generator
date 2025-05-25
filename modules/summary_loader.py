import pandas as pd
import logging
import yfinance as yf
import os
from datetime import timedelta, datetime
from tqdm import tqdm
from modules.controller import currency_of_portfolio


logging.basicConfig(
    filename='output/errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)


def summary_timeframe_loader(df):
    try:
        start_date = min(df['Open time'])
        end_date = max(df['Close time'])
        business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')
        timeframe = pd.DataFrame({'Date': business_days,
                                  f'Total change [%] in {currency_of_portfolio}': 0.0,
                                  f'Purchase value in {currency_of_portfolio}': 0.0,
                                  f'Current value in {currency_of_portfolio}': 0.0})
        return timeframe

    except Exception as e:
        print(f"Error in stock_timeframe: {e}")
        return pd.DataFrame()


def download_price(ticker, date):
    data = yf.download(
        ticker,
        start=date.strftime('%Y-%m-%d'),
        end=(date + timedelta(days=1)).strftime('%Y-%m-%d'),
        auto_adjust=False,
        progress=False
    )
    stock_price = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else data['Close'].iloc[
        0].item()

    return stock_price


volume = 0
exchange_rate_for_purchase_value = {}

def load_single_position(timeframe, position):
    global volume
    global exchange_rate_for_purchase_value

    try:
        filtered_timeframe = timeframe[
            (timeframe['Date'] >= position['Open time']) &
            (timeframe['Date'] <= position['Close time'])
        ]
        volume += position['Volume']

        if filtered_timeframe.empty:
            print(f"No matching dates for position {position['Formatted Symbol']}")
            return timeframe

        first_index = filtered_timeframe.iloc[0].name
        last_index = filtered_timeframe.iloc[-1].name

        volume = position['Volume']
        open_price = position['Open price']
        close_price = position['Close price']
        ticker = position['Formatted Symbol']

        try:
            symbol = yf.Ticker(ticker)
            currency = symbol.info.get('currency')
            exchange_rate_ticker = f"{currency}{currency_of_portfolio}=X"
        except Exception as e:
            logging.error(f"Error during yt.Ticker({ticker}): {e}")
            raise

        for index, row in filtered_timeframe.iterrows():
            date = row['Date']

            if currency == currency_of_portfolio:
                exchange_rate = 1
            else:
                try:
                    exchange_rate = download_price(exchange_rate_ticker, date)
                except Exception as e:
                    logging.error(f"Error retrieving data for {exchange_rate_ticker} on {date}: {e}")
                    timeframe.drop(index, inplace=True)
                    continue

            purchase_value = open_price * volume

            if index == first_index:
                if currency == currency_of_portfolio:
                    exchange_rate_for_purchase_value = 1
                else:
                    exchange_rate_for_purchase_value = exchange_rate

                sale_value = purchase_value

            elif index == last_index and not pd.isna(close_price):
                sale_value = close_price * volume

            else:
                try:
                    if currency == 'GBp':
                        stock_price = download_price(ticker, date) * 0.01
                    else:
                        stock_price = download_price(ticker, date)

                    sale_value = stock_price * volume

                except Exception as e:
                    logging.error(f"Error retrieving data for {ticker} on {date}: {e}")
                    timeframe.drop(index, inplace=True)
                    continue

            purchase_value_in_currency = purchase_value * exchange_rate_for_purchase_value
            sale_value_in_currency = sale_value * exchange_rate

            timeframe.loc[index, f'Purchase value in {currency_of_portfolio}'] += purchase_value_in_currency
            timeframe.loc[index, f'Current value in {currency_of_portfolio}'] += sale_value_in_currency


    except Exception as e:
        print(f"Error in load_single_position: {e}")
        return pd.DataFrame()


def load_and_format_positions(positions):
    try:
        timeframe = summary_timeframe_loader(positions)

        for _, position in tqdm(positions.iterrows(), desc='Loading timeframe', total=len(positions)):
            load_single_position(timeframe, position)
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            timeframe.to_excel(f"output/{timestamp} during {position['Formatted Symbol']}.xlsx")

        timeframe[f'Total change [%] in {currency_of_portfolio}'] = round(
            (timeframe[f'Current value in {currency_of_portfolio}'] / timeframe[f'Purchase value in {currency_of_portfolio}'] - 1) * 100, 2)

        return timeframe

    except Exception as e:
        print(f"Error in stock_history: {e}")
        return pd.DataFrame()
