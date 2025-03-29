import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def load_file(file_path):
    try:
        df = pd.read_csv(file_path, sep=';')
        return df

    except Exception as e:
        print(f"Error in load_file: {e}")
        return pd.DataFrame()

def merge_df(file_1, file_2):
    try:
        df = pd.concat([file_1, file_2], ignore_index=True)
        return df
    except Exception as e:
        print(f"Error in merge_df: {e}")
        return pd.DataFrame()

def format_symbol_for_yf(symbol):
    if symbol.endswith('.UK'):
        return symbol[:-3] + '.L'
    elif symbol.endswith('.US'):
        return symbol[:-3]
    elif symbol.endswith('.FR'):
        return symbol[:-3] + '.PA'
    return symbol

def format_currency_for_yf(symbol):
    if symbol.endswith('.UK'):
        return 'GBP'
    elif symbol.endswith('.US'):
        return 'USD'
    elif symbol.endswith('.FR' or '.DE'):
        return 'EUR'
    return symbol

def format_df(df):
    try:
        df['Formatted Symbol'] = df['Symbol'].apply(format_symbol_for_yf)
        df['Currency'] = df['Symbol'].apply(format_currency_for_yf)
        df['Open time'] = pd.to_datetime(df['Open time'], dayfirst=True).dt.normalize()
        df['Close time'].fillna(pd.Timestamp.now().normalize(), inplace=True)
        df['Close time'] = pd.to_datetime(df['Close time'], dayfirst=True, errors='coerce').dt.normalize()

    except Exception as e:
        print(f"Error in format_merged_df: {e}")
        return pd.DataFrame()

def load_currencies(df):
    try:
        currencies = []
        for currency in df['Currency'].unique():
            currencies.append(currency)
        return currencies

    except Exception as e:
        print(f"Error in load_currencies: {e}")
        return pd.DataFrame()

def load_timeframe(df):
    try:
        start_date = min(df['Open time'])
        end_date = datetime.now().replace(microsecond=0)
        business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')
        timeframe = pd.DataFrame({'Date': business_days, 'Profit': 0.0})

        return timeframe

    except Exception as e:
        print(f"Error in load_timeframe: {e}")
        return pd.DataFrame()

def load_exchange_rates(currency, date):
    ticker = f"{currency}PLN=X"
    data = yf.download(ticker, period="1d", start=date, end=date + timedelta(days=1), auto_adjust=False)
    exchange_rate = data["Close"].iloc[-1].item() if not data.empty else None
    return exchange_rate

def load_stock_history (timeframe, df):
    try:
        for index, row in timeframe.iterrows():
            date = row['Date'].date()
            total_profit = 0.0
            for _, stock in df.iterrows():
                open_time = stock['Open time'].date()
                close_time = stock['Close time'].date()
                if open_time <= date <= close_time:
                    try:
                        data = yf.download(stock['Formatted Symbol'], start=date, end=date + timedelta(days=1),
                                           auto_adjust=False)
                        stock_price = data['Close'].iloc[0].item()
                        exchange_rate = load_exchange_rates(stock['Currency'], date)
                        purchase_value = stock['Purchase value'].replace(',', '.')
                        purchase_value = pd.to_numeric(purchase_value, errors='coerce')
                        sale_value = stock_price * exchange_rate * stock['Volume']
                        profit = purchase_value - sale_value
                        total_profit += profit

                    except Exception as e:
                        print(f"Error retrieving data for {stock['Formatted Symbol']} on {date}: {e}")

            timeframe.loc[index, 'Profit'] += total_profit

    except Exception as e:
        print(f"Error in load_stock_history: {e}")