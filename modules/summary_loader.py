import pandas as pd
from modules.exchange_rates import load_exchange_rates
import logging
import yfinance as yf
from datetime import timedelta
from tqdm import tqdm


def summary_timeframe_loader(df):
    try:
        start_date = min(df['Open time'])
        end_date = max(df['Close time'])
        business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')
        timeframe = pd.DataFrame({'Date': business_days, 'Total change [%]': 0.0, 'Total change [%] in PLN': 0.0,
                                  'Purchase value': 0.0, 'Purchase value in PLN': 0.0, 'Current value': 0.0,
                                  'Current value in PLN': 0.0})
        return timeframe

    except Exception as e:
        print(f"Error in stock_timeframe: {e}")
        return pd.DataFrame()


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

        for index, row in filtered_timeframe.iterrows():
            date = row['Date']
            exchange_rate = load_exchange_rates(ticker, date)
            purchase_value = open_price * volume

            if index == first_index:
                exchange_rate_for_purchase_value = load_exchange_rates(ticker, date)
                sale_value = purchase_value

            elif index == last_index and not pd.isna(close_price):
                sale_value = close_price * volume

            else:
                try:
                    data = yf.download(
                        ticker,
                        start=date.strftime('%Y-%m-%d'),
                        end=(date + timedelta(days=1)).strftime('%Y-%m-%d'),
                        auto_adjust=False,
                        progress=False
                    )
                    stock_price = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else \
                    data['Close'].iloc[0].item()

                    sale_value = stock_price * volume

                except Exception as e:
                    logging.error(f"Error retrieving data for {ticker} on {date}: {e}")
                    timeframe.drop(index, inplace=True)
                    continue

            purchase_value_in_pln = purchase_value * exchange_rate_for_purchase_value
            sale_value_in_pln = sale_value * exchange_rate

            timeframe.loc[index, 'Purchase value'] += purchase_value
            timeframe.loc[index, 'Current value'] += sale_value

            timeframe.loc[index, 'Purchase value in PLN'] += purchase_value_in_pln
            timeframe.loc[index, 'Current value in PLN'] += sale_value_in_pln


    except Exception as e:
        print(f"Error in load_single_position: {e}")
        return pd.DataFrame()


def load_and_format_positions(positions):
    try:
        timeframe = summary_timeframe_loader(positions)

        for _, position in tqdm(positions.iterrows(), desc='Loading timeframe', total=len(positions)):
            load_single_position(timeframe, position)

        timeframe['Total change [%]'] = round(
            (timeframe['Current value'] / timeframe['Purchase value'] - 1) * 100, 2)

        timeframe['Total change [%] in PLN'] = round(
            (timeframe['Current value in PLN'] / timeframe['Purchase value in PLN'] - 1) * 100, 2)

        return timeframe

    except Exception as e:
        print(f"Error in stock_history: {e}")