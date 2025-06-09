import csv
import os

filnavn = "data/transactions.csv"
fieldnames = ["date", "type", "category", "amount"]

#   Gemmer én transaktion i CSV-filen.
#   Opretter mappen hvis den ikke findes og tilføjer kolonneoverskrifter hvis filen er tom.
def save_transaction(transaction):
    os.makedirs(os.path.dirname(filnavn), exist_ok=True)

    with open(filnavn, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(transaction)

#   Indlæser alle transaktioner fra CSV-filen og returnerer som en liste af dictionaries.
#   Hvis filen ikke findes, returneres en tom liste.
def load_transactions():
    if not os.path.exists(filnavn):
        return []

    with open(filnavn, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

#   Test: Udskriv alle transaktioner hvis filen køres direkte
if __name__ == "__main__":
    data = load_transactions()
    for t in data:
        print(t)