import pandas as pd
import yfinance as yf
from datetime import timedelta
# from modules.exchange_rates import load_currencies, load_exchange_rates


def stock_timeframe(positions):
    try:
        start_date = min(positions['Open time'])
        end_date = max(positions['Close time'])
        business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')
        timeframe = pd.DataFrame({'Date': business_days, 'Volume': 0.0, 'Total profit': 0.0,
                                  'Total change [%]': 0.0, 'Purchase value': 0.0, 'Current value': 0.0, 'Mean price': 0.0, 'Mean buy price': 0.0})
        return timeframe

    except Exception as e:
        print(f"Error in stock_timeframe: {e}")
        return pd.DataFrame()

def load_position(timeframe, position):
    try:
        filtered_timeframe = timeframe[(timeframe['Date'] >= position['Open time']) & (timeframe['Date'] <= position['Close time'])]

        for index, row in filtered_timeframe.iloc[1:].iterrows():
            try:
                date = row['Date']
                data = yf.download(position['Formatted Symbol'], start=date.strftime('%Y-%m-%d'),
                                   end=(date + timedelta(days=1)).strftime('%Y-%m-%d'), auto_adjust=False)
                stock_price = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else data['Close'].iloc[
                    0].item()

                # exchange_rate = load_exchange_rates(stock['Currency'], date)
                # if isinstance(exchange_rate, pd.Series):
                #     exchange_rate = exchange_rate.iloc[0]

                volume = position['Volume']
                purchase_value = position['Open price'] * volume
                sale_value = stock_price * volume
                profit = sale_value - purchase_value
                timeframe.loc[index, 'Purchase value'] += purchase_value
                timeframe.loc[index, 'Total profit'] += profit
                timeframe.loc[index, 'Current value'] += sale_value

            except Exception as e:
                print(f"Error retrieving data for {position['Formatted Symbol']} on {row['Date']}: {e}")
                timeframe.drop(index, inplace=True)
                continue

        first_index = filtered_timeframe.iloc[0].name
        purchase_value = position['Open price'] * position['Volume']

        timeframe.loc[first_index, 'Purchase value'] += purchase_value
        timeframe.loc[first_index, 'Current value'] += purchase_value

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
        # fast_info = yf.Ticker(ticker).fast_info
        information.append({'Timeframe': timeframe, 'Positions': positions})

        return information

    except Exception as e:
        print(f"Error in stock_information: {e}")
        return pd.DataFrame()


def all_stocks_information(unique_tickers, df):
    try:
        stocks = []
        for ticker in unique_tickers:
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