import pandas as pd
from Components.data_manager import load_transactions

def get_transactions_df():
    data = load_transactions()
    if not data:
        return pd.DataFrame(columns=["date", "type", "category", "amount"])

    df = pd.DataFrame(data)
    df["category"] = df["category"].str.capitalize()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["amount", "date"])

def get_available_months():
    df = get_transactions_df()
    if df.empty:
        return []

    months = df["date"].dt.to_period("M").astype(str).unique()
    return sorted(months)
