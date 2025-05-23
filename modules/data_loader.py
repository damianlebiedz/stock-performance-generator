import pandas as pd
import tkinter as tk
import os
from tkinter import filedialog
from modules.controller import format_symbol_for_yf


def load_report_from_xlsx():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
        title="Choose history of transactions file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    sheets = pd.Series(pd.ExcelFile(file, engine="openpyxl").sheet_names)
    matching_sheet_for_open = sheets[sheets.str.contains("OPEN POSITION")].iloc[0]
    open_positions = pd.read_excel(file, sheet_name=matching_sheet_for_open, engine="openpyxl")
    closed_positions = pd.read_excel(file, sheet_name="CLOSED POSITION HISTORY", engine='openpyxl')

    cleaned_open_positions = open_positions.iloc[10:].reset_index(drop=True)
    cleaned_closed_positions = closed_positions.iloc[12:].reset_index(drop=True)

    cleaned_open_positions = cleaned_open_positions.iloc[:-1, list(range(2, 7)) + [8]]
    cleaned_closed_positions = cleaned_closed_positions.iloc[:-1, list(range(2, 9)) + [11, 12]]

    cleaned_closed_positions.columns = ["Symbol", "Type", "Volume", "Open time", "Open price", "Close time",
                                        "Close price", "Purchase value", "Sale value"]
    cleaned_open_positions.columns = ["Symbol", "Type", "Volume", "Open time", "Open price", "Purchase value"]

    cleaned_open_positions = cleaned_open_positions.dropna()
    cleaned_closed_positions = cleaned_closed_positions.dropna()

    cleaned_open_positions.to_csv(os.path.join("data", "OPEN POSITIONS from XTB.csv"), index=False)
    cleaned_closed_positions.to_csv(os.path.join("data", "CLOSED POSITIONS from XTB.csv"), index=False)

    return cleaned_closed_positions, cleaned_open_positions


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


def format_df(df):
    try:
        df['Formatted Symbol'] = df['Symbol'].apply(format_symbol_for_yf)
        df['Open time'] = pd.to_datetime(df['Open time'], dayfirst=True).dt.normalize()

        df['Close time'] = pd.to_datetime(df['Close time'], dayfirst=True, errors='coerce').dt.normalize()
        df['Close time'] = df['Close time'].fillna(pd.Timestamp.now().normalize())

        for col in ['Open price', 'Close price', 'Purchase value', 'Sale value']:
            df[col] = df[col].apply(lambda x: str(x).replace(',', '.') if pd.notnull(x) else x)
            df[col] = df[col].astype(float)

    except Exception as e:
        print(f"Error in format_df: {e}")
        return pd.DataFrame()
