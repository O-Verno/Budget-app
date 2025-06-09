import csv
import os


filnavn = "data/transactions.csv"
fieldnames = ["date", "type", "category", "amount"]

def save_transaction(transaction):
    
    os.makedirs(os.path.dirname(filnavn), exist_ok=True)

    with open(filnavn, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(transaction)

def load_transactions():
    
    if not os.path.exists(filnavn):
        return []  

    with open(filnavn, mode="r", newline="") as file:
        reader = csv.DictReader(file)  
        return [row for row in reader]  

        
if __name__ == "__main__":
    data = load_transactions()
    for t in data:
        print(t)
