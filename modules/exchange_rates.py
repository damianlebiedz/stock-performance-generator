import pandas as pd
import yfinance as yf
from datetime import timedelta


def load_currencies(df):
    try:
        currencies = []
        for currency in df['Currency'].unique():
            currencies.append(currency)
        return currencies

    except Exception as e:
        print(f"Error in load_currencies: {e}")
        return pd.DataFrame()


def load_exchange_rates(currency, date):
    ticker = f"{currency}PLN=X"
    data = yf.download(ticker, period="1d", start=date, end=date + timedelta(days=1), auto_adjust=False)
    exchange_rate = data["Close"].iloc[-1].item() if not data.empty else None
    return exchange_rate