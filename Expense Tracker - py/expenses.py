import json

PREBUILT_CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"]


def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)


def resolve_category(choice):
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(PREBUILT_CATEGORIES):
            return PREBUILT_CATEGORIES[index]

    category = choice.strip().title()
    if category in PREBUILT_CATEGORIES:
        return category

    raise ValueError("Invalid category")


def update_expense(expenses, index, field, value):
    if field in {"name", "description"}:
        expenses[index]["description"] = value
    elif field == "category":
        expenses[index]["category"] = value
    elif field == "amount":
        expenses[index]["amount"] = float(value)
    else:
        raise ValueError("Invalid field")


def display_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return

    for index, item in enumerate(expenses, start=1):
        print(f"{index}. {item['description']} [{item['category']}]: ${item['amount']:.2f}")


def main():
    expenses = load_expenses()

    while True:
        print("\n1. Add expense")
        print("2. View expenses")
        print("3. Total expenses")
        print("4. Edit expense")
        print("5. Delete expense")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            description = input("What did you buy? ")
            print("Choose a category:")
            for index, category in enumerate(PREBUILT_CATEGORIES, start=1):
                print(f"{index}. {category}")
            category_choice = input("Enter the number for the category: ")
            try:
                category = resolve_category(category_choice)
            except ValueError:
                print("Invalid category. Using 'Other'.")
                category = "Other"

            amount = float(input("How much did it cost? "))
            expenses.append({"description": description, "category": category, "amount": amount})
            save_expenses(expenses)
            print("Expense added.")

        elif choice == "2":
            display_expenses(expenses)

        elif choice == "3":
            total = sum(item["amount"] for item in expenses)
            print(f"Total expenses: ${total:.2f}")

        elif choice == "4":
            if not expenses:
                print("No expenses to edit.")
            else:
                display_expenses(expenses)
                expense_number = int(input("Enter the number of the expense to edit: ")) - 1
                if 0 <= expense_number < len(expenses):
                    field = input("What do you want to edit? (name/category/amount): ").strip().lower()
                    if field in {"name", "description"}:
                        new_value = input("Enter the new name: ")
                    elif field == "category":
                        print("Choose a category:")
                        for index, category in enumerate(PREBUILT_CATEGORIES, start=1):
                            print(f"{index}. {category}")
                        new_value = resolve_category(input("Enter the number for the category: "))
                    elif field == "amount":
                        new_value = float(input("Enter the new amount: "))
                    else:
                        print("Invalid field.")
                        continue

                    update_expense(expenses, expense_number, field, new_value)
                    save_expenses(expenses)
                    print("Expense updated.")
                else:
                    print("Invalid number.")

        elif choice == "5":
            if not expenses:
                print("No expenses to delete.")
            else:
                display_expenses(expenses)
                expense_number = int(input("Enter the number of the expense to delete: ")) - 1
                if 0 <= expense_number < len(expenses):
                    deleted = expenses.pop(expense_number)
                    save_expenses(expenses)
                    print(f"Deleted: {deleted['description']}")
                else:
                    print("Invalid number.")

        elif choice == "6":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()