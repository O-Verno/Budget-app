from Components.input_handler import get_transaction_input
from Components.data_manager import save_transaction, load_transactions
from Components.analyzer import calculate_totals
from Components.visualizer import (
    plot_expenses_by_category,
    plot_monthly_expenses,
    plot_monthly_income,
    plot_income_vs_expenses
)

#   Kommandolinje-baseret hovedmenu til økonomi-appen.
#   Giver adgang til at tilføje transaktioner, vise opsummering og visualiseringer.
def main():
    while True:
        print("\n=== Økonomi App ===")
        print("1. Tilføj ny transaktion")
        print("2. Se transaktioner + opsummering")
        print("3. Vis udgifter som cirkeldiagram")
        print("4. Vis udgifter pr. måned (søjlediagram)")
        print("5. Vis indtægter pr. måned (søjlediagram)")
        print("6. Vis indtægter vs. udgifter pr. måned")
        print("7. Afslut")

        choice = input("Vælg en funktion (1-7): ")

        if choice == "1":
            # Hent input og gem transaktion
            transaction = get_transaction_input()
            if transaction:
                save_transaction(transaction)
                print("Transaktion gemt.")
            input("Tryk Enter for at vende tilbage til menuen...")

        elif choice == "2":
            # Vis alle transaktioner + opsummering
            transactions = load_transactions()
            if not transactions:
                print("Ingen transaktioner fundet.")
            else:
                for t in transactions:
                    print(f"{t['date']} | {t['type']:7} | {t['category']:10} | {float(t['amount']):.2f} kr")
                income, expense, balance = calculate_totals()
                print("\nOpsummering:")
                print(f"Indtægter:  {income:.2f} kr")
                print(f"Udgifter:   {expense:.2f} kr")
                print(f"Balance:    {balance:.2f} kr")
            input("Tryk Enter for at vende tilbage til menuen...")

        elif choice == "3":
            # Cirkeldiagram: udgifter pr. kategori
            plot_expenses_by_category()

        elif choice == "4":
            # Søjlediagram: udgifter pr. måned
            plot_monthly_expenses()

        elif choice == "5":
            # Søjlediagram: indtægter pr. måned
            plot_monthly_income()

        elif choice == "6":
            # Søjlediagram: indtægter vs. udgifter
            plot_income_vs_expenses()

        elif choice == "7":
            print("Tak for nu. Programmet afsluttes.")
            break

        else:
            print("Ugyldigt valg. Prøv igen.")


#   Starter programmet hvis filen køres direkte
if __name__ == "__main__":
    main()