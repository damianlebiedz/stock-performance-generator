import yfinance as yf
from datetime import timedelta
from modules.controller import format_currency_for_yf
import time
from requests.exceptions import SSLError, ConnectionError


def load_exchange_rates(symbol, date, retries=3, delay=2):
    currency = format_currency_for_yf(symbol)
    ticker = f"{currency}PLN=X"

    for attempt in range(retries):
        try:
            data = yf.download(
                ticker,
                start=date.strftime('%Y-%m-%d'),
                end=(date + timedelta(days=1)).strftime('%Y-%m-%d'),
                auto_adjust=False,
                progress=False,
                threads=False,
            )

            exchange_rate = data['Close'].iloc[0] if isinstance(data['Close'].iloc[0], float) else data['Close'].iloc[
                0].item()

            return exchange_rate

        except (SSLError, ConnectionError) as e:
            print(f"Network issue for {ticker} on {date}, attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return 0

        except Exception as e:
            print(f"Other error for {ticker} on {date}: {e}")
            return 0
