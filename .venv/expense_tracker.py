import customtkinter as ctk
from BudgetTracker import Expense
from datetime import datetime
import calendar


class BudgetTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ultimate Budget Tracker!")
        self.geometry("600x600")

        self.budget = 2000.0
        self.expense_file_path = "expenses.csv"

        self.create_widgets()
    def create_widgets(self):
    #header
        self.head_label = ctk.CTkLabel(self, text="Ultimate Budget Tracker", font=("Arial", 24))
        self.head_label.pack(pady=10)
    #Expense Name
        self.name_label = ctk.CTkLabel(self, text="Expense Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self, width=300)
        self.name_entry.pack(pady=5)
    #Expense Amount
        self.amount_label = ctk.CTkLabel(self, text="$Amount$:")
        self.amount_label.pack(pady=5)
        self.amount_entry = ctk.CTkEntry(self, width=300)
        self.amount_entry.pack(pady=5)
    #Categories
        self.category_label = ctk.CTkLabel(self, text="Select Category:")
        self.category_label.pack(pady=5)
        self.category_var = ctk.StringVar(value="Food")
        self.categories = ["Food", "Home", "Work", "Fun", "Other"]
        self.category_menu = ctk.CTkOptionMenu(self, variable=self.category_var, values=self.categories)
        self.category_menu.pack(pady=5)

    #Submit
        self.add_button = ctk.CTkButton(self, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=10)
    #Summary
        self.summary_button = ctk.CTkButton(self, text="Show Summary", command=self.summarize_expense)
        self.summary_button.pack(pady=10)

        self.summary_textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.summary_textbox.pack(pady=20)

def main():
    budget = 2000.0
    expense = get_user_expense()
    expense_file_path = "expenses.csv"
    save_expense_to_file(expense, expense_file_path)
    summarize_expense(expense_file_path, budget)

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

if __name__ == "__main__":
    main()