import pandas as pd
from Components.data_manager import load_transactions

#   Indlæser alle transaktioner og returnerer dem som en pandas DataFrame.
#   Sikrer at dato og beløb konverteres korrekt. Bruges i analyser og grafer.
def get_transactions_df():
    data = load_transactions()
    if not data:
        return pd.DataFrame(columns=["date", "type", "category", "amount"])

    df = pd.DataFrame(data)
    df["category"] = df["category"].str.capitalize()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["amount", "date"])

#   Finder og returnerer en sorteret liste over alle unikke måneder i data.
#   Bruges i GUI til at vælge måned for filtrerede grafer.
def get_available_months():
    df = get_transactions_df()
    if df.empty:
        return []

    months = df["date"].dt.to_period("M").astype(str).unique()
    return sorted(months)