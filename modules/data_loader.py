import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def load_closed_positions(file_path):
    try:
        df = pd.read_csv(file_path, sep=';', parse_dates=['Open time', 'Close time'], dayfirst=True)
        df['Purchase value'] = df['Purchase value'].str.replace(',', '.').astype(float)
        df['Sale value'] = df['Sale value'].str.replace(',', '.').astype(float)
        df['Profit'] = df['Sale value'] - df['Purchase value']
        print("Closed positions loaded successfully")
        return df

    except Exception as e:
        print(f"Error in load_closed_positions: {e}")
        return pd.DataFrame()

def load_open_positions(file_path, market_data, exchange_rates):
    try:
        df = pd.read_csv(file_path, sep=';')
        print("Nazwy kolumn w df:", df.columns)

        df['Formatted Symbol'] = df['Symbol'].apply(format_symbol_for_yf)
        print("Sformatowane symbole:", df['Formatted Symbol'].unique())

        for symbol in df['Formatted Symbol'].unique():
            print(f"Processing symbol: {symbol}")
            if symbol in market_data.index:
                print(f"  Match found in market_data")
                ticker = yf.Ticker(symbol)
                close_price = ticker.fast_info.previous_close
                df.loc[df['Formatted Symbol'] == symbol, 'Close price'] = close_price
            else:
                print(f"  No match found in market_data")
                df.loc[df['Formatted Symbol'] == symbol, 'Close price'] = df.loc[df['Formatted Symbol'] == symbol, 'Open price']

        df['Currency'] = df['Symbol'].apply(lambda x: x.split('.')[-1] if '.' in x else 'PLN')
        print("Waluty:", df['Currency'].unique())

        df['Exchange ratio'] = df['Currency'].apply(map_exchange_rate, args=(exchange_rates,))

        for col in ['Open price', 'Close price', 'Purchase value', 'Volume', 'Exchange ratio']:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

        df['Sale value'] = df['Close price'] * df['Volume'] * df['Exchange ratio']
        df['Profit'] = df['Sale value'] - df['Purchase value']

        print("Open positions loaded successfully")
        return df

    except Exception as e:
        print(f"Error in load_open_positions: {e}")
        return pd.DataFrame()

def fetch_exchange_rates():
    try:
        currencies = ["USD", "EUR", "GBP", "CHF", "JPY", "CAD", "AUD"]
        tickers = [f"{cur}PLN=X" for cur in currencies]
        rates = yf.download(tickers, period="1d")

        exchange_rates = {cur: rates[("Close", f"{cur}PLN=X")].iloc[-1] for cur in currencies}
        exchange_rates["PLN"] = 1.0
        print("Exchange rates fetched successfully:", exchange_rates)
        return exchange_rates

    except Exception as e:
        print(f"Error in fetch_exchange_rates: {e}")
        return {}

def format_symbol_for_yf(symbol):
    if symbol.endswith('.UK'):
        return symbol[:-3] + '.L'
    elif symbol.endswith('.US'):
        return symbol[:-3]
    return symbol

def fetch_market_data(symbols, days_back=5):
    try:
        formatted_symbols = [format_symbol_for_yf(symbol) for symbol in symbols]
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        market_data = yf.download(formatted_symbols, start=start_date, end=end_date)["Close"]
        last_available_close = market_data.iloc[-1]
        print("Market data fetched successfully")
        return last_available_close

    except Exception as e:
        print(f"Error in fetch_market_data: {e}")
        return pd.Series()

def map_exchange_rate(currency, exchange_rates):
    if currency == 'US':
        return exchange_rates.get('USD', None)
    elif currency == 'UK':
        return exchange_rates.get('GBP', None)
    else:
        return exchange_rates.get(currency, None)