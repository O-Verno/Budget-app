import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkcalendar import DateEntry    
from datetime import datetime
import pandas as pd
from Components.data_manager import save_transaction, load_transactions
from Components.analyzer import calculate_totals
from Components.pandas import ( get_available_months,
                               get_transactions_df)
from Components.visualizer import (
    plot_expenses_by_category,
    plot_monthly_expenses,
    plot_monthly_income,
    plot_income_vs_expenses,    
    plot_expenses_by_category_for_month
)


BUDGETS = {}


#   Viser gennemsnitligt forbrug pr. kategori baseret på alle måneder.
#   Beregner med pandas og viser resultatet i et messagebox popup.
def vis_gennemsnitligt_forbrug():

    df = get_transactions_df()
    if df.empty:
        messagebox.showinfo("Ingen data", "Der er ingen transaktioner.")
        return

    df["category"] = df["category"].str.capitalize()
    df["month"] = df["date"].dt.to_period("M")
    expenses = df[df["type"] == "expense"]

    monthly = expenses.groupby(["month", "category"])["amount"].sum()
    mean_per_category = monthly.groupby("category").mean()

    tekst = "Gennemsnitligt forbrug pr. måned:\n\n"
    for kategori, beløb in mean_per_category.items():
        tekst += f"{kategori}: {beløb:.2f} kr\n"

    messagebox.showinfo("Gennemsnitligt forbrug", tekst)

#   Sammenligner brugerens aktuelle måneds forbrug med gennemsnittet
#   pr. kategori, og viser forskellen som enten over eller under gennemsnittet.
def vis_afvigelser_fra_gennemsnit():

    df = get_transactions_df()
    if df.empty:
        messagebox.showinfo("Ingen data", "Der er ingen transaktioner.")
        return

    df["category"] = df["category"].str.capitalize()
    df["month"] = df["date"].dt.to_period("M")
    expenses = df[df["type"] == "expense"]

    monthly = expenses.groupby(["month", "category"])["amount"].sum()
    mean_per_category = monthly.groupby("category").mean()

    this_month = pd.Timestamp.now().to_period("M")
    current_month_data = monthly.loc[this_month] if this_month in monthly.index.levels[0] else pd.Series()

    if current_month_data.empty:
        messagebox.showinfo("Ingen data", "Ingen udgifter registreret i denne måned.")
        return

    tekst = f"Forbrug i {this_month} sammenlignet med gennemsnit:\n\n"
    for kategori, aktuelt in current_month_data.items():
        gennemsnit = mean_per_category.get(kategori, 0)
        forskel = aktuelt - gennemsnit
        status = "over" if forskel > 0 else "under"
        tekst += f"{kategori}: {aktuelt:.2f} kr (Gns: {gennemsnit:.2f} kr → {abs(forskel):.2f} kr {status})\n"

    messagebox.showinfo("Afvigelse fra gennemsnit", tekst)

#   Tjekker om brugerens forbrug i hver kategori overstiger den definerede budgetgrænse.
#   (OBS: Funktion er ikke færdigimplementeret – advarsler vises ikke endnu.)
def check_budget_status():

    df = get_transactions_df()
    expenses = df[df["type"] == "expense"]
    totals = expenses.groupby("category")["amount"].sum()

    for category, forbrug in totals.items():
        grænse = BUDGETS.get(category)
        if grænse and forbrug > grænse:
            ...  

    # Ekstra analyse (vises pt. kun i konsol)
    df["month"] = df["date"].dt.to_period("M")
    monthly = df[df["type"] == "expense"].groupby(["month", "category"])["amount"].sum()
    mean_per_category = monthly.groupby("category").mean()
    print(mean_per_category)


#   Henter data fra inputfelter i GUI, validerer og gemmer som ny transaktion i CSV.
#   Viser fejlbeskeder hvis input er ugyldigt.
def add_transaction():

    data = {
        "date": entry_date.get(),
        "type": var_type.get(),
        "category": entry_category.get(),
        "amount": entry_amount.get()
    }

    try:
        data["amount"] = float(data["amount"])
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Fejl", "Dato eller beløb er ugyldigt.")
        return

    save_transaction(data)
    messagebox.showinfo("OK", "Transaktionen er gemt.")
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

#   Viser alle transaktioner fra CSV i tekstfelt i GUI'en.
#   Hver transaktion vises som en formateret linje.
def show_transactions():

    transactions = load_transactions()
    text_display.delete("1.0", tk.END)

    if not transactions:
        text_display.insert(tk.END, "Ingen transaktioner fundet.\n")
        return

    for t in transactions:
        line = f"{t['date']} | {t['type']:7} | {t['category']:10} | {float(t['amount']):.2f} kr\n"
        text_display.insert(tk.END, line)

#   Viser en opsummering af økonomien:
#   - Samlet indtægt
#   - Samlet udgift
#   - Balance
#   Bruger `calculate_totals()` til at hente data (via pandas).
def show_summary():

    transactions = load_transactions()
    if not transactions:
        messagebox.showinfo("Ingen data", "Der er ingen transaktioner endnu.")
        return

    income, expense, balance = calculate_totals()

    summary_text = (
        f"Indtægter:  {income:.2f} kr\n"
        f"Udgifter:   {expense:.2f} kr\n"
        f"Balance:    {balance:.2f} kr"
    )
    messagebox.showinfo("Økonomisk oversigt", summary_text)



window = tk.Tk()
window.title("Økonomi App")
window.geometry("700x600")

BUDGETS.update({
    "Mad": 2000,
    "Transport": 1500,
    "Fritid": 1000,
    "Andet": 500
})

style = ttk.Style()
style.theme_use("clam")


notebook = ttk.Notebook(window)
notebook.pack(padx=10, pady=10, fill="both", expand=True)

tab_input = ttk.Frame(notebook)
tab_overview = ttk.Frame(notebook)
tab_graphs = ttk.Frame(notebook)


notebook.add(tab_input, text="Tilføj transaktion")
notebook.add(tab_overview, text="Oversigt")
notebook.add(tab_graphs, text="Grafer")


input_frame = ttk.Frame(tab_input, padding=20)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Tilføj ny transaktion", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

ttk.Label(input_frame, text="Dato (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_date = DateEntry(input_frame, date_pattern="yyyy-mm-dd", width=18)
entry_date.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Type:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
var_type = tk.StringVar(value="expense")
type_dropdown = ttk.Combobox(input_frame, textvariable=var_type, values=["expense", "income"], state="readonly", width=17)
type_dropdown.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Kategori:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_category = ttk.Entry(input_frame, width=20)
entry_category.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Beløb:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_amount = ttk.Entry(input_frame, width=20)
entry_amount.grid(row=4, column=1, padx=5, pady=5)

ttk.Button(input_frame, text="Gem transaktion", command=add_transaction).grid(row=5, column=0, columnspan=2, pady=(20, 0))



overview_canvas = tk.Canvas(tab_overview)
overview_scrollbar = ttk.Scrollbar(tab_overview, orient="vertical", command=overview_canvas.yview)
overview_scrollable_frame = ttk.Frame(overview_canvas)

overview_scrollable_frame.bind(
    "<Configure>",
    lambda e: overview_canvas.configure(
        scrollregion=overview_canvas.bbox("all")
    )
)

overview_canvas.create_window((0, 0), window=overview_scrollable_frame, anchor="nw")
overview_canvas.configure(yscrollcommand=overview_scrollbar.set)

overview_canvas.pack(side="left", fill="both", expand=True)
overview_scrollbar.pack(side="right", fill="y")

ttk.Label(overview_scrollable_frame, text="Transaktioner", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

ttk.Button(overview_scrollable_frame, text="Vis transaktioner", command=show_transactions).pack(pady=5)

text_display = tk.Text(overview_scrollable_frame, height=15, width=70, font=("Courier", 10))
text_display.pack(pady=5)

ttk.Button(overview_scrollable_frame, text="Vis opsummering", command=show_summary).pack(pady=5)
ttk.Button(overview_scrollable_frame, text="Tjek budgetstatus", command=check_budget_status).pack(pady=5)
ttk.Button(overview_scrollable_frame, text="Gennemsnitligt forbrug", command=vis_gennemsnitligt_forbrug).pack(pady=5)
ttk.Button(overview_scrollable_frame, text="Sammenlign med gennemsnit", command=vis_afvigelser_fra_gennemsnit).pack(pady=5)


graphs_frame = ttk.Frame(tab_graphs, padding=20)
graphs_frame.pack(pady=10)

ttk.Label(graphs_frame, text="Visualisering", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))


ttk.Button(graphs_frame, text="Udgifter pr. kategori", command=plot_expenses_by_category).pack(pady=5)
ttk.Button(graphs_frame, text="Indtægter pr. måned", command=plot_monthly_income).pack(pady=5)
ttk.Button(graphs_frame, text="Indtægter vs. udgifter", command=plot_income_vs_expenses).pack(pady=5)

ttk.Label(graphs_frame, text="Vælg måned:").pack(pady=(20, 5))
selected_month = tk.StringVar()
month_dropdown = ttk.Combobox(graphs_frame, textvariable=selected_month, state="readonly", width=15)
month_dropdown['values'] = get_available_months()
month_dropdown.pack()

 #  Viser pie chart over udgifter i den valgte måned fra dropdown.
 #  Bruger `plot_expenses_by_category_for_month()` fra visualizer.
def show_filtered_pie():

    month = selected_month.get()
    if not month:
        messagebox.showwarning("Ingen måned valgt", "Vælg en måned først.")
        return
    plot_expenses_by_category_for_month(month)


ttk.Button(graphs_frame, text="Vis udgifter for valgt måned", command=show_filtered_pie).pack(pady=5)

ttk.Label(overview_scrollable_frame, text="Opdater budget for kategori:", font=("Helvetica", 12)).pack(pady=(15, 5))

budget_category = tk.StringVar()
ttk.Entry(overview_scrollable_frame, textvariable=budget_category, width=20).pack(pady=2)

budget_amount = tk.StringVar()
ttk.Entry(overview_scrollable_frame, textvariable=budget_amount, width=20).pack(pady=2)

 #  Opdaterer budget for en valgt kategori.
 #  Validerer at beløb er et tal og viser en bekræftelse.
def update_budget():

    cat = budget_category.get()
    try:
        amount = float(budget_amount.get())
        BUDGETS[cat] = amount
        messagebox.showinfo("OK", f"Budget for '{cat}' sat til {amount:.2f} kr.")
        budget_category.set("")
        budget_amount.set("")
    except ValueError:
        messagebox.showerror("Fejl", "Beløbet skal være et tal.")

ttk.Button(overview_scrollable_frame, text="Gem budget", command=update_budget).pack(pady=5)

#  Viser alle gemte budgetgrænser i et messagebox-vindue.
def show_current_budgets():

    if not BUDGETS:
        messagebox.showinfo("Ingen budgetter", "Der er ingen budgetter endnu.")
        return

    tekst = "\n".join([f"{cat}: {amount:.2f} kr" for cat, amount in BUDGETS.items()])
    messagebox.showinfo("Aktuelle budgetter", tekst)

ttk.Button(overview_scrollable_frame, text="Vis aktuelle budgetter", command=show_current_budgets).pack(pady=5)
    
window.mainloop()
