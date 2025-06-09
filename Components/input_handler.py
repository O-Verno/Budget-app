from datetime import datetime

def get_transaction_input():
    
    date = input("indtast dato (YYYY-MM-DD): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Ugyldig dato. Skriv YYYY-MM-DD")
        return None
    
    type_ = input("Er det en 'expense' eller 'income'? ").lower()
    if type_ not in ["expense", "income"]:
        print("Type skal være 'expense' eller 'income'.")
        return None
    
    category = input("Hvilken kategori? ")

    try:
        amount = float(input("Hvor meget (kr)? "))
    except ValueError:
        print("Beløb skal være et tal.")
        return None
    
    return {
        "date": date,
        "type": type_,
        "category": category,
        "amount": amount
    }