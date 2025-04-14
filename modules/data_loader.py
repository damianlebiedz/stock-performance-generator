import pandas as pd
from modules.controllers.formatting_controller import format_symbol_for_yf, format_currency_for_yf


def load_file(file_path):
    try:
        df = pd.read_csv(file_path, sep=';')
        return df

    except Exception as e:
        print(f"Error in load_file: {e}")
        return pd.DataFrame()


def merge_df(file_1, file_2): #sprawdzić wyjątki
    try:
        df = pd.concat([file_1, file_2], ignore_index=True)
        return df
    except Exception as e:
        print(f"Error in merge_df: {e}")
        return pd.DataFrame()


def format_df(df):  # sprawdzić wszystkie przypadki złego formatu, zrobić wyjątki
    try:
        df['Formatted Symbol'] = df['Symbol'].apply(format_symbol_for_yf)
        df['Currency'] = df['Symbol'].apply(format_currency_for_yf)
        df['Open time'] = pd.to_datetime(df['Open time'], dayfirst=True).dt.normalize()

        df['Close time'] = pd.to_datetime(df['Close time'], dayfirst=True, errors='coerce').dt.normalize()
        df['Close time'].fillna(pd.Timestamp.now().normalize(), inplace=True)

    except Exception as e:
        print(f"Error in format_df: {e}")
        return pd.DataFrame()