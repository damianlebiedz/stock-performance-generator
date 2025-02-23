import pandas as pd

def load_closed_positions(file_path):
    df = pd.read_csv(file_path, parse_dates=["Data"])
    return df

def load_open_positions(file_path, market_data):
    df = pd.read_csv(file_path, parse_dates=["Data"])

    for symbol in df["Symbol"].unique():
        if symbol in market_data.columns:
            df.loc[df["Symbol"] == symbol, "Close price"] = market_data[symbol].iloc[-1]

    df["Sale value"] = df["Close price"] * (df["Purchase value"] / df["Open price"])
    return df