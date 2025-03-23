import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from modules.data_loader import map_exchange_rate

def calculate_daily_portfolio_profit(open_positions, closed_positions):
    open_positions['Open time'] = pd.to_datetime(open_positions['Open time'], format='%d.%m.%Y %H:%M')
    closed_positions['Close time'] = pd.to_datetime(closed_positions['Close time'], format='%d.%m.%Y %H:%M')

    start_date = min(open_positions['Open time'].iloc[0], closed_positions['Open time'].iloc[0])
    end_date = datetime.now().replace(microsecond=0)

    business_days = pd.date_range(start=start_date.date(), end=end_date.date(), freq='B')
    portfolio_profit_df = pd.DataFrame({'Date': business_days, 'Profit': 0.0})
    exchange_rates_history = {}

    for current_date in portfolio_profit_df['Date']:
        exchange_rates = fetch_hist_exchange_rates(str(current_date))
        exchange_rates_history = pd.DataFrame({'Date': current_date, 'Exchange ratios': exchange_rates})
        #print(exchange_rates_history)

    for current_date in portfolio_profit_df['Date']:
        daily_profit = calculate_daily_profit(closed_positions, open_positions, exchange_rates_history, str(current_date))
        portfolio_profit_df.loc[portfolio_profit_df['Date'] == current_date, 'Profit'] = daily_profit

    return portfolio_profit_df

def fetch_hist_exchange_rates(current_date):
    try:
        currencies = ["USD", "EUR", "GBP"]
        exchange_rates = {}
        current_date = current_date.split()[0]

        for cur in currencies:
            ticker = f"{cur}PLN=X"
            data = yf.download(ticker, period="1d", start=current_date,
                               end=(datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)).strftime(
                                   '%Y-%m-%d'))
            exchange_rates[cur] = data["Close"].iloc[-1].item() if not data.empty else None

        exchange_rates["PLN"] = 1.0
        return exchange_rates

    except Exception as e:
        print(f"Error in fetch_hist_exchange_rates: {e}")
        return {}

#BŁAD - do zrobienia
def calculate_daily_profit(closed_positions, open_positions, exchange_rates_history, current_date):
    daily_profit = 0
    try:
        current_date = current_date.split()[0]
        exchange_rates = exchange_rates_history[f'{current_date}']

        # Obliczanie zysków dla otwartych pozycji aktywnych w danym dniu
        for _, row in open_positions.iterrows():
            if row['Open time'].date() <= current_date.date() and (
                    pd.isna(row['Close time']) or row['Close time'].date() > current_date.date()):
                # Pobranie kursu wymiany dla waluty aktywa
                exchange_rate = map_exchange_rate(row['Currency'], exchange_rates)
                close_price = row['Close price'] if row['Close price'] is not None else row['Open price']
                profit = (close_price * row['Volume'] * exchange_rate) - row['Purchase value']
                daily_profit += profit

        # Obliczanie zysków dla zamkniętych pozycji zamkniętych w danym dniu
        for _, row in closed_positions.iterrows():
            if row['Close time'].date() == current_date.date():
                daily_profit += row['Profit']

        return daily_profit

    except Exception as e:
        print(f"Error in calculate_daily_profit: {e}")
        return {}