import pandas as pd
import yfinance as yf
from datetime import datetime

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

def format_symbol_for_yf(symbol):
    if symbol.endswith('.UK'):
        return symbol[:-3] + '.L'
    elif symbol.endswith('.US'):
        return symbol[:-3]
    return symbol

def map_exchange_rate(currency, exchange_rates):
    if currency == 'US':
        return exchange_rates.get('USD', None)
    elif currency == 'UK':
        return exchange_rates.get('GBP', None)
    else:
        return exchange_rates.get(currency, None)

def fetch_exchange_rates():
    try:
        currencies = ["USD", "EUR", "GBP"]
        exchange_rates = {}

        for cur in currencies:
            ticker = f"{cur}PLN=X"
            data = yf.download(ticker, period="1d")
            exchange_rates[cur] = data["Close"].iloc[-1].item() if not data.empty else None

        exchange_rates["PLN"] = 1.0
        return exchange_rates

    except Exception as e:
        print(f"Error in fetch_exchange_rates: {e}")
        return {}

def load_open_positions(file_path, exchange_rates):
    try:
        df = pd.read_csv(file_path, sep=';')
        df['Formatted Symbol'] = df['Symbol'].apply(format_symbol_for_yf)

        for symbol in df['Formatted Symbol'].unique():
            ticker = yf.Ticker(symbol)
            close_price = ticker.fast_info.regular_market_previous_close
            df.loc[df['Formatted Symbol'] == symbol, 'Close price'] = close_price

        df['Currency'] = df['Symbol'].apply(lambda x: x.split('.')[-1] if '.' in x else 'PLN')
        df['Exchange ratio'] = df['Currency'].apply(map_exchange_rate, args=(exchange_rates,))

        for col in ['Open price', 'Close price', 'Purchase value', 'Volume', 'Exchange ratio']:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

        df['Current value'] = df['Close price'] * df['Volume'] * df['Exchange ratio']
        df['Profit'] = df['Current value'] - df['Purchase value']

        df['Close time'] = datetime.now().replace(microsecond=0)

        print("Open positions loaded successfully")
        return df

    except Exception as e:
        print(f"Error in load_open_positions: {e}")
        return pd.DataFrame()