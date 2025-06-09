import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from Components.pandas import get_transactions_df

def plot_expenses_by_category():
    df = get_transactions_df()
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        print("Ingen udgifter at vise.")
        return

    category_totals = expenses.groupby("category")["amount"].sum()
    category_totals.plot.pie(
        autopct="%.1f%%", 
        title="Udgifter pr. kategori", 
        ylabel=""
    )
    plt.tight_layout()
    plt.show()

def plot_monthly_expenses():
    df = get_transactions_df()
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        print("Ingen udgifter at vise.")
        return

    expenses["month"] = expenses["date"].dt.to_period("M")
    monthly_totals = expenses.groupby("month")["amount"].sum()

    monthly_totals.plot(kind="bar", color="skyblue", figsize=(10, 5))
    plt.title("Udgifter pr. måned")
    plt.ylabel("Beløb (kr)")
    plt.xlabel("Måned")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_monthly_income():
    df = get_transactions_df()
    income = df[df["type"] == "income"]
    if income.empty:
        print("Ingen indtægter at vise.")
        return

    income["month"] = income["date"].dt.to_period("M")
    monthly_totals = income.groupby("month")["amount"].sum()

    monthly_totals.plot(kind="bar", color="lightgreen", figsize=(10, 5))
    plt.title("Indtægter pr. måned")
    plt.ylabel("Beløb (kr)")
    plt.xlabel("Måned")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_income_vs_expenses():
    
    df = get_transactions_df()
    df["month"] = df["date"].dt.to_period("M")

    pivot = df.pivot_table(index="month", columns="type", values="amount", aggfunc="sum").fillna(0)

    pivot.plot(kind="bar", figsize=(10, 6), color={"income": "lightgreen", "expense": "salmon"})
    plt.title("Indtægter vs. Udgifter pr. måned")
    plt.ylabel("Beløb (kr)")
    plt.xlabel("Måned")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()      


def plot_expenses_by_category_for_month(month_str):

    df = get_transactions_df()
    df["month"] = df["date"].dt.to_period("M").astype(str)

    filtered = df[(df["type"] == "expense") & (df["month"] == month_str)]

    if filtered.empty:
        print("Ingen udgifter i den valgte måned.")
        return

    totals = filtered.groupby("category")["amount"].sum()
    totals.plot.pie(autopct="%.1f%%", title=f"Udgifter i {month_str}", ylabel="")
    plt.tight_layout()
    plt.show()
