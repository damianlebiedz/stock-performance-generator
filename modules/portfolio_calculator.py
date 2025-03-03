import pandas as pd

def calculate_daily_performance(closed_positions, open_positions):
    closed_positions['Close time'] = pd.to_datetime(closed_positions['Close time'], format="%d.%m.%Y %H:%M",
                                                    dayfirst=True)
    open_positions['Open time'] = pd.to_datetime(open_positions['Open time'], format="%d.%m.%Y %H:%M", dayfirst=True)

    all_positions = pd.concat([
        closed_positions[['Close time', 'Profit']],
        open_positions[['Open time', 'Profit']].rename(columns={'Open time': 'Close time'})
    ])

    daily_performance = all_positions.groupby(all_positions['Close time'].dt.date)['Profit'].sum().cumsum()

    return daily_performance