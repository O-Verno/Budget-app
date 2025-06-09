from Components.data_manager import save_transaction
from Components.pandas import get_transactions_df


def calculate_totals():
    df = get_transactions_df()

    if df.empty:
        return 0.0, 0.0, 0.0

    grouped = df.groupby("type")["amount"].sum()

    income = grouped.get("income", 0.0)
    expense = grouped.get("expense", 0.0)
    balance = income - expense

    return income, expense, balance
    