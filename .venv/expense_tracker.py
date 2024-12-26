from BudgetTracker import Expense
from datetime import datetime
import calendar
import time

def main():
    budget = 2000.0
    expense_file_path = "expenses.csv"

    while True:
        print("\nBudget Tracker Menu!")
        print("1. Add expense")
        print("2. View Summary")
        print("3. Adjust budget")
        print("4. Delete Expenses")
        print("5. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            expense = get_user_expense()
            save_expense_to_file(expense,expense_file_path)
        elif choice == "2":
            summarize_expense(expense_file_path, budget)
        elif choice == "3":
            budget = float(input("What is your new budget?"))
        elif choice == "4":
            delete_expenses(expense_file_path)
        elif choice == "5":
            print("Thank You!")
            break
        else:
            print("invalid option. 1-5 please")

    budget = first_of_month(expense_file_path,budget)
    #expense = get_user_expense()
    #save_expense_to_file(expense, expense_file_path)
    #summarize_expense(expense_file_path, budget)
    #weekly_budget_check(budget)

# Budget Work
def first_of_month(expense_file_path, budget):
    today = datetime.today()
    if today.day == 1:
        print("Resetting budget")
        budget = reset_budget(budget)

        with open(expense_file_path, "w") as f:
            f.write("")
    return budget

def weekly_budget_check(budget, target_day = calendar.FRIDAY):
    #target_day = calendar.FRIDAY
    today = datetime.today().weekday()
    if today == target_day:
        now = datetime.now()
        if now.weekday() == target_day:
            get_budget_change(budget)
        return budget


def get_budget_change(budget):
    increase_check = input("If your budget increased type 'y' if not 'n'")
    if increase_check == "y":
        budget_increase = float(input("How much extra money do you have a month now?"))
        budget = budget + budget_increase
    elif increase_check == "n":
        decrease_check = input("If your budget decreased type 'y' if not 'n'")
        if decrease_check == "y":
            budget_decrease = float(input("How much less money do you have a month now?"))
            budget = budget - budget_decrease


#Expense Work
def get_user_expense():
    print(f"Getting User Expense")
    e_name = input("Enter expense name:")
    e_amount = float(input("Enter expense amount:"))
    print(f"You've entered {e_name}, {e_amount}")
    e_categories = ["Food", "Home", "Work", "Fun", "Other"]

    while True:
        print("select category")

        for i, category_name in enumerate(e_categories):
            print(f" {i + 1}. {category_name} ")

        value_range = f"[1- {len(e_categories)}]"

        try:
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if 0 <= selected_index < len(e_categories):
                selected_category = e_categories[selected_index]
                new_expense = Expense(name=e_name, category=selected_category, amount=e_amount)
                return new_expense
            else:
                print("Invalid Category, try again")
        except ValueError:
            print("Invalid input. Please enter valid integer.")

def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")



def summarize_expense(expense_file_path, budget):
    expenses = []
    print(f" User Expenses!")
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(name=expense_name,amount=float(expense_amount),category=expense_category)
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        #check if key exists
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expense by category")
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")

    total_spent = sum([ex.amount for ex in expenses])
    print(f"You have spent ${total_spent:.2f} this month")

    remaining_budget = budget - total_spent
    print(f"Budget Remaining ${remaining_budget:.2f} left this month")
    # Get today's date
    today = datetime.today()

    # Get the last day of the current month
    last_day = calendar.monthrange(today.year, today.month)[1]
    last_date_of_month = datetime(today.year, today.month, last_day)

    # Calculate remaining days
    remaining_days = (last_date_of_month - today).days

    print(f"Remaining days in the current month: {remaining_days}")

    daily_budget = remaining_budget/remaining_days
    print(f"Recommended Budget Per Day!: $ {daily_budget:.2f}")

def view_expenses(expense_file_path):
    try:
        with open(expense_file_path, "r") as f:
            lines = f.readlines()
            if not lines:
                print("No expenses")
                return[]

            print("\nExpenses:")
            for index, line in enumerate(lines, start=1):
                print(f"{index}: {line.strip()}") #displays line#:
            return lines
    except FileNotFoundError:
        print("File not found")
        return[]

def delete_expenses(expense_file_path):
    lines = view_expenses(expense_file_path)
    if not lines:
        return

    while True:
        try:
            line_delete = int(input("\nEnter the line # of the expense you want to delete. 0 to cancel"))
            if line_delete == 0:
                return
            if 1 <= line_delete <= len(lines):
                break
            else:
                print("Invalid line #. Try again")
        except ValueError:
            print("Invalid input. Enter valid line #")

    del lines[line_delete - 1]
    with open(expense_file_path, "w") as f:
        f.writelines(lines)
    print(f"Expense {line_delete} deleted")
if __name__ == "__main__":
    main()