import pandas as pd
import yfinance as yf
from datetime import timedelta
from modules.exchange_rates import load_exchange_rates
import logging
from tqdm import tqdm


logging.basicConfig(
    filename='output/errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def stock_timeframe(positions):
    try:
        start_date = min(positions['Open time'])
        end_date = max(positions['Close time'])
        business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')
        timeframe = pd.DataFrame({'Date': business_days, 'Volume': 0.0, 'Total profit': 0.0,
                                  'Total change [%]': 0.0, 'Purchase value': 0.0, 'Current value': 0.0,
                                  'Mean price': 0.0, 'Mean buy price': 0.0, 'Exchange rate': 0.0,
                                  'Total profit in PLN': 0.0, 'Purchase value in PLN': 0.0,
                                  'Current value in PLN': 0.0, 'Mean price in PLN': 0.0,
                                  'Mean buy price in PLN': 0.0, 'Total change [%] in PLN': 0.0})
        return timeframe

    except Exception as e:
        print(f"Error in stock_timeframe: {e}")
        return pd.DataFrame()

exchange_rate_for_purchase_value = {}

def load_position(timeframe, position):
    global exchange_rate_for_purchase_value
    try:
        filtered_timeframe = timeframe[
            (timeframe['Date'] >= position['Open time']) &
            (timeframe['Date'] <= position['Close time'])
        ]

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
                profit = 0

            elif index == last_index and not pd.isna(close_price):
                sale_value = close_price * volume
                profit = sale_value - purchase_value

            else:
                try:
                    data = yf.download(
                        ticker,
                        start=date.strftime('%Y-%m-%d'),
                        end=(date + timedelta(days=1)).strftime('%Y-%m-%d'),
                        auto_adjust=False,
                        progress=False
                    )
                    stock_price = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else data['Close'].iloc[0].item()

                    sale_value = stock_price * volume
                    profit = sale_value - purchase_value

                except Exception as e:
                    logging.error(f"Error retrieving data for {ticker} on {date}: {e}")
                    timeframe.drop(index, inplace=True)
                    continue

            purchase_value_in_pln = purchase_value * exchange_rate_for_purchase_value
            sale_value_in_pln = sale_value * exchange_rate
            profit_in_pln = sale_value_in_pln - purchase_value_in_pln

            timeframe.loc[index, 'Purchase value'] += purchase_value
            timeframe.loc[index, 'Current value'] += sale_value
            timeframe.loc[index, 'Total profit'] += profit

            if timeframe.loc[index, 'Exchange rate'] == 0:
                timeframe.loc[index, 'Exchange rate'] = exchange_rate

            timeframe.loc[index, 'Purchase value in PLN'] += purchase_value_in_pln
            timeframe.loc[index, 'Current value in PLN'] += sale_value_in_pln
            timeframe.loc[index, 'Total profit in PLN'] += profit_in_pln

    except Exception as e:
        print(f"Error in load_position: {e}")
        return pd.DataFrame()

def stock_history(positions):
    try:
        timeframe = stock_timeframe(positions)

        for _, stock in positions.iterrows():
            timeframe.loc[(timeframe['Date'] >= stock['Open time']) &
                          (timeframe['Date'] <= stock['Close time']), 'Volume'] += stock['Volume']
            load_position(timeframe, stock)

        timeframe['Mean price'] = timeframe['Current value'] / timeframe['Volume']
        timeframe['Mean buy price'] = timeframe['Purchase value'] / timeframe['Volume']
        timeframe['Total change [%]'] = (
                (timeframe['Mean price'] / timeframe['Mean buy price'] - 1) * 100).round(2)

        timeframe['Mean price in PLN'] = timeframe['Current value in PLN'] / timeframe['Volume']
        timeframe['Mean buy price in PLN'] = timeframe['Purchase value in PLN'] / timeframe['Volume']
        timeframe['Total change [%] in PLN'] = (
                (timeframe['Mean price in PLN'] / timeframe['Mean buy price in PLN'] - 1) * 100).round(2)

        return timeframe

    except Exception as e:
        print(f"Error in stock_history: {e}")


def stock_positions(ticker, df):
    try:
        positions = df[df['Formatted Symbol'] == ticker].copy()

        for col in ['Open price', 'Close price', 'Purchase value', 'Sale value']:
            positions[col] = positions[col].str.replace(',', '.', regex=False).astype(float)

        return positions

    except Exception as e:
        print(f"Error in stock_positions: {e}")
        return pd.DataFrame()


def stock_information(ticker, df):
    information = []
    try:
        positions = stock_positions(ticker, df)
        timeframe = stock_history(positions)
        information.append({'Timeframe': timeframe, 'Positions': positions})

        return information

    except Exception as e:
        print(f"Error in stock_information: {e}")
        return pd.DataFrame()


def all_stocks_information(unique_tickers, df):
    try:
        stocks = []
        for ticker in tqdm(unique_tickers, desc='Loading stocks', total=len(unique_tickers)):
            try:
                informations = stock_information(ticker, df)
                stocks.append({'Ticker': ticker, 'Informations': informations})

            except Exception as e:
                print(f"Error in all_stocks_information in {ticker}: {e}")
                continue

        return stocks

    except Exception as e:
        print(f"Error in all_stocks_information: {e}")
        return pd.DataFrame()
