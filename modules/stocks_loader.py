import pandas as pd
import yfinance as yf
from datetime import timedelta


def stock_timeframe(ticker, df):
    try:
        filtered_df = df[df['Formatted Symbol'] == f'{ticker}']
        start_date = min(filtered_df['Open time'])
        end_date = max(filtered_df['Close time'])
        business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')  # nie działa dla crypto!
        timeframe = pd.DataFrame(
            {'Date': business_days, 'Volume': 0.0, 'Profit': 0.0, 'Profit cumulated': 0.0, 'Daily change': 0.0,
             'Total change': 0.0})  # dodać in PLN (ryzyko walutowe) każdego profitu

        return timeframe

    except Exception as e:
        print(f"Error in stock_timeframe: {e}")
        return pd.DataFrame()

def load_position(stock_timeframe, position):  # obsługa df pozycji, zwracanie do danych o spółce śrendiej ceny zakupu i kursu
    try:
        filtered_timeframe = stock_timeframe[
            (stock_timeframe['Date'] >= position['Open time']) & (stock_timeframe['Date'] <= position['Close time'])]
        for index, row in filtered_timeframe.iterrows():
            try:
                date = row['Date']
                data = yf.download(position['Formatted Symbol'], start=date.strftime('%Y-%m-%d'),
                                   end=(date + timedelta(days=1)).strftime('%Y-%m-%d'), auto_adjust=False)
                stock_price = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else data['Close'].iloc[
                    0].item()

                # exchange_rate = load_exchange_rates(stock['Currency'], date)
                # if isinstance(exchange_rate, pd.Series):
                #     exchange_rate = exchange_rate.iloc[0]

                purchase_value = float(position['Open price'].replace(',', '.'))
                sale_value = stock_price
                profit = sale_value - purchase_value
                stock_timeframe.loc[index, 'Profit'] += profit

            except Exception as e:
                # print(f"Error retrieving data for {position['Formatted Symbol']} on {date}: {e}")
                # return None
                stock_timeframe.drop(index, inplace=True)  # Usuń wiersz w przypadku błędu
                continue

    except Exception as e:
        print(f"Error in load_position: {e}")
        return pd.DataFrame()

def stock_history(ticker, df):
    try:
        timeframe = stock_timeframe(ticker, df)
        positions = stock_positions(ticker, df)

        for _, stock in positions.iterrows():
            timeframe.loc[(timeframe['Date'] >= stock['Open time']) &
                          (timeframe['Date'] <= stock['Close time']), 'Volume'] += 1.0
            load_position(timeframe, stock)

        return timeframe

    except Exception as e:
        print(f"Error in stock_history: {e}")

def stock_positions(ticker, df):
    try:
        positions = df[df['Formatted Symbol'] == ticker]
        return positions

    except Exception as e:
        print(f"Error in stock_positions: {e}")
        return pd.DataFrame()

def stock_information(ticker, df):
    informations = []
    try:
        timeframe = stock_history(ticker, df)
        positions = stock_positions(ticker, df)
        # fast_info = yf.Ticker(ticker).fast_info #uzupełnić potrzebne
        mean_price = ...
        mean_exchange_ratio = ...
        informations.append({'Fast info': ..., 'Timeframe': timeframe, 'Positions': positions, 'Mean price': mean_price,
                             'Mean exchange ratio': mean_exchange_ratio})

        return informations

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
                print(f"Error in all_stocks_history in {ticker}: {e}")
                continue

        return stocks

    except Exception as e:
        print(f"Error in all_stocks_history: {e}")
        return pd.DataFrame()