import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE = "Expenses.json"

def load():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def add():
    data = load()
    date = input("Enter date (dd-mm-yyyy): ").strip()
    category = input("Enter category: ").strip()
    try:
        amount = float(input("Enter amount: ").strip())
    except ValueError:
        print("Invalid amount, try again")
        return
    description = input("Enter description: ").strip()

    data.append({
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    })

    save(data)
    print("Expense added!\n")

def summary():
    data = load()
    month = input("Enter month (mm-yyyy): ").strip()
    total = 0
    category_totals = {}

    for e in data:
        if len(e["date"]) >= 7 and e["date"][3:] == month:
            total += e["amount"]
            cat = e["category"]
            category_totals[cat] = category_totals.get(cat, 0) + e["amount"]

    print(f"\nTotal spending for {month}: {total}")

    if category_totals:
        highest = max(category_totals, key=category_totals.get)
        print(f"Highest spending category: {highest} ({category_totals[highest]})\n")
    else:
        print("No data for this month\n")

    return category_totals

def chart(category_totals):
    if not category_totals:
        print("No data to display in chart")
        return

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    colors = ["skyblue", "orange", "violet", "gold", "lightcoral", "turquoise"]

    plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors)
    plt.title("Category-wise Expense Breakdown")
    plt.show()

def run():
    while True:
        print("\n--- Smart Expense Tracker ---")
        print("1. Add expense")
        print("2. Monthly summary")
        print("3. Exit")

        ch = input("Choose (number or word): ").strip().lower()

        if ch == "1" or ch == "add":
            add()
        elif ch == "2" or ch == "summary":
            s = summary()
            ans = input("See chart? y/n: ").strip().lower()
            if ans == "y":
                chart(s)
        elif ch == "3" or ch == "exit":
            print("Goodbye!")
            break
        else:
            print("Wrong choice, please try again.\n")

run()
