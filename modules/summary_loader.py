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
                                  'Total change [%]': 0.0, 'Purchase value': 0.0,
                                  'Current value': 0.0, 'Total profit in PLN': 0.0,
                                  'Total change [%] in PLN': 0.0, 'Purchase value in PLN': 0.0,
                                  'Current value in PLN': 0.0})

        return timeframe

    except Exception as e:
        print(f"Error in summary_timeframe: {e}")
        return pd.DataFrame()


def load_summary(all_stocks):
    try:
        summary_timeframe = (
            pd.concat([info['Timeframe'] for stock in all_stocks for info in stock['Informations']])
            .groupby('Date', as_index=False)
            .agg({
                'Total profit': 'sum',
                'Purchase value': 'sum',
                'Current value': 'sum',
                'Total profit in PLN': 'sum',
                'Purchase value in PLN': 'sum',
                'Current value in PLN': 'sum',
            })
        )
        summary_timeframe['Total change [%]'] = (
                (summary_timeframe['Current value'] / summary_timeframe['Purchase value'] - 1) * 100).round(2)

        summary_timeframe['Total change [%] in PLN'] = (
                (summary_timeframe['Current value in PLN'] / summary_timeframe['Purchase value in PLN'] - 1) * 100).round(2)

        return summary_timeframe[summary_timeframe['Total profit'] != 0.0]

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
