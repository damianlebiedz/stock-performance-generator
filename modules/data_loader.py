import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

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

    cleaned_open_positions = clean_csv_file(open_positions, 9)
    cleaned_closed_positions = clean_csv_file(closed_positions, 11)

    cleaned_open_positions.to_csv(os.path.join("output", "OPEN POSITIONS.csv"), index=False)
    cleaned_closed_positions.to_csv(os.path.join("output", "CLOSED POSITIONS.csv"), index=False)


def clean_csv_file(input_path, skiprows):
    cleaned_csv = input_path.iloc[skiprows:].reset_index(drop=True)
    cleaned_csv.iloc[:, 0] = cleaned_csv.iloc[:, 0].astype(str)
    first_col_split = cleaned_csv.iloc[:, 0].str.split(',', expand=True)
    cleaned_csv = cleaned_csv.drop(cleaned_csv.columns[0], axis=1)
    pd.concat([first_col_split, cleaned_csv], axis=1)

    return cleaned_csv


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
        df['Open time'] = pd.to_datetime(df['Open time'], dayfirst=True).dt.normalize()

        df['Close time'] = pd.to_datetime(df['Close time'], dayfirst=True, errors='coerce').dt.normalize()
        df['Close time'].fillna(pd.Timestamp.now().normalize(), inplace=True)

    except Exception as e:
        print(f"Error in format_df: {e}")
        return pd.DataFrame()
