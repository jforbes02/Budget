from BudgetTracker import Expense

def main():
    expense = get_user_expense()
    expense_file_path = "expenses.csv"
    #save expense to file
    save_expense_to_file(expense, expense_file_path)
    #read file and summarize expenses
    summarize_expense(expense_file_path)
    pass

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
    print(f"Saving expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    pass
def summarize_expense(expense_file_path):
    expenses=[]
    print(f" User Expenses")
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip.split(",")
            line_expense = Expense(name=expense_name,amount=expense_amount,category=expense_category)
            print(line_expense)
            expenses.append(line_expense)
    print(expenses)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        #check if key exists
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

        print("Expense by category")
        #for key, amount in amount_by_category.items():
        #    print(f" {key}: ${amount:.2f}")

if __name__ == "__main__":
    main()