import pandas as pd


def load_summary_timeframe(all_stocks):
    try:
        start_date = min(
            info['Timeframe']['Date'].min() for stock in all_stocks for info in stock['Informations']
        )
        end_date = max(
            info['Timeframe']['Date'].max() for stock in all_stocks for info in stock['Informations']
        )
        business_days = pd.date_range(start=start_date.date(), end=end_date.date())
        timeframe = pd.DataFrame({'Date': business_days, 'Total profit': 0.0,
                                  'Total change': 0.0})  # dodać in PLN (ryzyko walutowe) każdego profitu

        return timeframe

    except Exception as e:
        print(f"Error in summary_timeframe: {e}")
        return pd.DataFrame()


def load_summary(all_stocks):
    summary_timeframe = load_summary_timeframe(all_stocks)
    try:
        for stock in all_stocks:
            for info in stock['Informations']:
                timeframe = info['Timeframe']

                for index, row in timeframe.iterrows():
                    date = row['Date']
                    profit = row['Total profit']

                    summary_timeframe.loc[summary_timeframe['Date'] == date, 'Total profit'] += profit

        filtered_summary_timeframe = summary_timeframe[summary_timeframe['Total profit'] != 0.0]

        return filtered_summary_timeframe

    except Exception as e:
        print(f"Error in load_summary: {e}")
        return pd.DataFrame()