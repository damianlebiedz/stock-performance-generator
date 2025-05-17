import pandas as pd

from modules.controller import comparison_ticker
from modules.load_comparison_data import load_comparison_asset


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

        cleaned_summary = summary_timeframe[summary_timeframe['Total profit'] != 0.0]

        cleaned_summary[f'Total change [%] of {comparison_ticker}'] = None
        load_comparison_asset(comparison_ticker, cleaned_summary)

        return cleaned_summary

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()