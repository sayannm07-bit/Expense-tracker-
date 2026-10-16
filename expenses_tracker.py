import json
from pathlib import Path
from datetime import date, datetime

DATA_FILE = Path("transactions.json")


def load_transactions():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: saved transactions could not be read. Starting empty.")
        return []


transactions = load_transactions()


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        print("\nNo interactive input is available. Run this program in a console.")
        raise SystemExit


def save_transactions():
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Could not save transactions: {error}")


def add_transaction():
    kind = ask("Type (income/expense): ").lower()
    if kind not in ("income", "expense"):
        print("Type must be income or expense.")
        return

    try:
        amount = float(ask("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Amount must be a number greater than zero.")
        return

    category = ask("Category: ")
    if not category:
        print("Category cannot be empty.")
        return
    description = ask("Description (optional): ")
    entered_date = ask("Date YYYY-MM-DD (Enter for today): ")

    if not entered_date:
        entered_date = date.today().isoformat()
    try:
        datetime.strptime(entered_date, "%Y-%m-%d")
    except ValueError:
        print("Date must use YYYY-MM-DD.")
        return

    transactions.append({
        "type": kind,
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "date": entered_date
    })
    save_transactions()
    print("Transaction saved.")


def view_transactions(records=None):
    records = transactions if records is None else records
    if not records:
        print("No transactions found.")
        return
    print("\n--- TRANSACTIONS ---")
    for number, item in enumerate(records, start=1):
        print(
            f"{number}. {item['date']} | {item['type'].title()} | "
            f"{item['category']} | {item['description']} | "
            f"{item['amount']:.2f}"
        )


def show_summary():
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    print("\n--- SUMMARY ---")
    print(f"Total income:   {income:.2f}")
    print(f"Total expenses: {expenses:.2f}")
    print(f"Balance:        {income - expenses:.2f}")


def filter_by_date():
    target = ask("Date to find (YYYY-MM-DD): ")
    try:
        datetime.strptime(target, "%Y-%m-%d")
    except ValueError:
        print("Date must use YYYY-MM-DD.")
        return
    view_transactions([t for t in transactions if t["date"] == target])


def filter_by_category():
    target = ask("Category to find: ").casefold()
    view_transactions([
        t for t in transactions if t["category"].casefold() == target
    ])


def main():
    while True:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Financial summary")
        print("4. Filter by date")
        print("5. Filter by category")
        print("6. Exit")
        choice = ask("Choose 1-6: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            filter_by_date()
        elif choice == "5":
            filter_by_category()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
