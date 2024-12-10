# Budget Tracker

# Imported libraries
import json
import os
import time
from datetime import datetime, timedelta
import csv

# Initializing with JSON file
DATA_FILE = "budget_data.json"

# Created global variables
total_income = 0
total_expenses = 0
balance = total_income - total_expenses

# Created global dictionaries
income_list = {}
expense_list = {}

# CSV Functions

def export_data_to_csv():
    with open("budget_report.csv", 'w', newline="") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Type", "Amount", "Description", "Timestamp", "Date"])

        # Write income data with timestamp
        for amount, details in data["income_list"].items():
            description = details["description"]
            timestamp = details["timestamp"]
            writer.writerow(["Income", amount, description, timestamp])
        
        # Write expense data with timestamp
        for amount, details in data["expense_list"].items():
            description = details["description"]
            timestamp = details["timestamp"]
            writer.writerow(["Expense", amount, description, timestamp])
        
        # Write bill data (no timestamp, but adding a due date if needed)
        for name, details in data["bill_calendar"].items():
            due_date = details["due_date"].strftime('%y-%m-%d')
            amount = details["amount"]
            writer.writerow(["Bill", amount, name, "", due_date])
        
        # Write savings account data (no timestamp, only goal and remaining balance)
        for account, details in data["savings_accounts"].items():
            remaining_balance = details["remaining_balance"]
            writer.writerow(["Savings", remaining_balance, account])

    print("Data exported to budget_report.csv")

# JSON Functions

# Load data form JSON file if it exists, else initialize empty data structure
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            if "last_startup" in data:
                data["last_startup"] = datetime.strptime(data["last_startup"], "%Y-%m-%d %H:%M:%S")
            return data

    else:
        return {
            "balance": 0,
            "total_income": 0,
            "total_expenses": 0,
            "income_list": {},
            "expense_list": {},
            "bill_calendar": {},
            "savings_accounts": {},
            "last_startup": datetime.min,
            }

# Save data to JSON file    
def save_data(data):
    # Add the startup time
    data["last_startup"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4) # Indent added for looks

# Delete Functions

def delete_income(amount, description):
    global total_income, balance

    # Check to see if selected income is in list, delete if True
    if amount in data["income_list"] and data["income_list"][amount] == description:
        data["income_list"].pop(amount)
        total_income -= amount
        balance -= amount
        save_data(data) # Save data to JSON file
        print(f"Income '{description} of ${amount:.2f} deleted.")

    else:
        print("Income entry not found.")

    # Prompts for menu or exit
    return_to_menu_or_exit()

def delete_expense(amount, description):
    global total_expenses, balance

    # Check to see if selected expense is in list, delete if True
    if amount in data["expense_list"] and data["expense_list"][amount] == description:
        data["expense_list"].pop(amount)
        total_expenses -= amount
        balance -= amount
        save_data(data) # Save data to JSON file
        print(f"Expense '{description}' of ${amount:.2f} deleted.")

    else:
        print("Expense entry not found.")

    return_to_menu_or_exit()

def delete_bill(name):

    # Check for bill, delete if True
    if name in data["bill_calendar"]:
        data["bill_calendar"].pop(name)
        save_data(data) # Save data to JSON file
        print(f"Bill '{name}' deleted.")

    else:
        print("Bill not found.")

    return_to_menu_or_exit()

def delete_savings_account(account_name):
    global total_income, balance

    # Check for savings account, delete if True
    if account_name in data["savings_accounts"]:
        saved_amount = data["savings_accounts"][account_name]["goal"] - data["savings_accounts"][account_name]["remaining_balance"]
        total_income += saved_amount
        balance += saved_amount
        data["income_list"][saved_amount] = f"Saved amount from {account_name} savings account."
        data["savings_accounts"].pop(account_name)
        save_data(data) # Save data to JSON file
        print(f"Savings account '{account_name}' deleted.")
        time.sleep(0.5) # Add delay for easy readability
        print(f"Saved amount of ${saved_amount:.2f} added to income.")

    else:
        print("Savins account not found.")

    return_to_menu_or_exit()

# Display Functions

def display_income():
    print("\nIncome List:")
    
    # Check for income list in JSON file
    if not data["income_list"]:
        print("No income records.")

    else:
        # Prints income in date order
        for i, (amount, description, date) in enumerate(data["income_list"].items(), start=1):
            print(f"{i}. Amount: ${amount:.2f}, Description: {description}, Date: {date}")
    time.sleep(1) # Add delay for easy readability
    
    # Provide chance to delete an entry
    choice = input("\nWould you like to delete an income entry? (yes/no): ").strip().lower()
    
    if choice == "yes":
        index = int(input("Enter the number of the income entry you want to delete: ")) - 1
        if 0 <= index < len(data["income_list"]):
            amount, description = list(data["income_list"].items())[index]
            delete_income(amount, description)
        else:
            print("Invalid entry number.")
    
    return_to_menu_or_exit()

def display_expenses():
    print("\nExpense List:")
    
    # Check for expense list in JSON file
    if not data["expense_list"]:
        print("No expense records.")
    
    else:
        # Prints expenses in date order
        for i, (amount, description) in enumerate(data["expense_list"].items(), start=1):
            print(f"{i}. Amount: ${amount:.2f}, Description: {description}")
    
    # Provide chance to delete an entry
    choice = input("\nWould you like to delete an expense entry? (yes/no):").strip().lower()
    
    if choice == "no":
        index = int(input("Enter the number of the expense entry you want to delete: ")) - 1
        if 0 <= index < len(data["expense_list"]):
            amount, description = list(data["expense_list"].items())[index]
            delete_expense(amount, description)
        else:
            print("Invalid entry number.")
    
    return_to_menu_or_exit()

# General Functions

def return_to_menu_or_exit():
    while True:
        
        choice = input("Would you like to return to the main menu, or exit? (Enter 'menu' or 'exit'): ")
        
        if choice.lower() == "menu":
            main_menu()
            break
        elif choice.lower() == "exit":
            print("Exiting the program...")
            exit()
    
    else:
        print("Invalid choice. Please try again: ")

def add_income(amount = 0, description = "item"):
    global income_list, total_income, balance

    # Adds timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["income_list"][amount] = {"description": description, "timestamp": timestamp}

    # Add amount to variables
    total_income += amount
    balance += amount
    
    save_data(data)
    time.sleep(1)
    
    # Output Summary
    print("\nIncome Summary:")
    time.sleep(0.5)
    print(display_income())
    time.sleep(0.5)
    print(f"{description} successfully added to your income. Your new balance is {balance:.2f}.")
    time.sleep(1)
    
    return_to_menu_or_exit()

def add_expense(amount = 0, description = "item"):
    global expense_list, total_expenses, balance

    # Adds timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["expense_list"][amount] = {"description": description, "timestamp": timestamp}
    
    # Add/Subtract amount from variables
    total_expenses += amount
    balance -= amount
    
    save_data(data)
    time.sleep(1)
    
    # Output Summary
    print("\nExpense Summary:")
    time.sleep(0.5)
    print(display_expenses())
    time.sleep(0.5)
    print(f"{description} successfully added to your expenses. Your new balance is {balance:.2f}.")
    
    return_to_menu_or_exit()

def view_balance():
    global balance

    print(f"Your balance is {balance:.2f}.")

    return_to_menu_or_exit()

def view_summary():
    
    # Prints full summary
    print("\nComplete Budget Summary:")
    print(view_balance())
    print(display_income())
    print(display_expenses())
    print(view_bills())
    print(view_savings_accounts())
    
    return_to_menu_or_exit()

# Bill Calendar Functions

bill_calendar = {} # Bills dictionary

def add_bill(name, date_str, amount, recurring=False, interval=None):
    
    # Convert the date string to a datetime object
    due_date = datetime.strptime(date_str, '%Y-%m-%d') # Format YYYY, MM, DD
    
    # Bill entry structure
    bill_entry = {
        "amount": amount,
        "due_date": due_date,
        "recurring": recurring,
        "interval": interval, # Can we weekly or monthly
        "next_due": due_date if recurring else None # Start with initial due date
    }
    data["bill_calendar"][name] = bill_entry
    
    save_data(data)
    time.sleep(1)
    
    print(f"Your bill '{name}' has been successfully added to your bill calendar!")
    
    return_to_menu_or_exit()

def process_recurring_bills(last_startup):
    today = datetime.now()
    processed_bills = [] # List to store messages for processed bills
    
    for name, bill in data["bill_calendar"].items():
        if bill["recurring"] and bill["next_due"] and bill["next_due"] <= today:
            if bill["next_due"] >= last_startup:
                # Create a unique identifier for the recurring bill
                expense_identifier = f"{name}_{bill["next_due"].strftime('%Y-%m-%d')}"
                
                # Check if this bill entry already exists in the expense list
                already_added = any(
                    entry["description"] == expense_identifier for entry in data["expense_list"].values()
                    )
                
                if not already_added:
                    # Add bill to expenses with the unique identifier
                    add_expense(bill["amount"], expense_identifier)
                    
                    # Deduct from balance
                    global balance
                    balance -= bill["amount"]
                    
                    # Update the next due date based on interval
                    if bill["interval"] == "weekly":
                        bill["next_due"] += timedelta(weeks=1)
                    elif bill["interval"] == "monthly":
                        # To increment by a month, adjust the month value
                        next_month = bill["next_due"].month % 12 + 1
                        year = bill["next_due"].year + (1 if next_month == 1 else 0)
                        bill["next_due"] = bill["next_due"].replace(year=year, month=next_month)
                    
                    # Add message to processed bills list
                    processed_bills.append(
                        f"Processed recurring bill '{name}' for {bill['amount']:.2f}. Next due on {bill["next_due"].strftime('%Y-%m-%d')}"
                        )
    
    save_data(data)
    
    return processed_bills

def view_bills():
    # Sorted bills in due date order
    sorted_bills = sorted(data["bill_calendar"].items(), key=lambda x: x[1]["due_date"])
    print("Bill Calendar:")
    
    if not sorted_bills:
        print("No bills available.")
    else:
        for name, details in sorted_bills:
            due_date = details["due_date"]
            amount = details["amount"]
            print(f"Bill: {name}, Due: {due_date.strftime('%Y-%m-%d')}, Amount: ${amount:.2f}")
    
    # Provides chance to delete bill
    choice = input("\n Would you like to delete a bill? (yes/no): ").strip().lower()
    if choice == "yes":
        name = input("Enter the name of the bill you want to delete: ")
        delete_bill(name)
    
    return_to_menu_or_exit()

def view_upcoming_bills():
    # Get today's date and the date 15 days from now
    today = datetime.now()
    upcoming_date = today + timedelta(days=15)

    # Sort and filter bills within the next 15 days
    sorted_bills = sorted(
        ((name,details) for name, details in data["bill_calendar"].items() if today <= details["due_date"] <= upcoming_date),
        key=lambda x: x[1]["due_date"]
        )

    # Display the sorted bills
    print("Upcoming Bills (Next 15 Days):")
    if not sorted_bills:
        print("No bills due in the next 15 days.")
    else:
        for name, details in sorted_bills:
            due_date = details["due_date"]
            amount = details["amount"]
            print(f"Bill: {name}, Due: {due_date.strftime('%Y-%m=%d')}, Amount: {amount:.2f}")
    
    return_to_menu_or_exit()

# Savings Account Functions

savings_accounts = {} # Dictionary to store savings accounts

def add_savings_account(account_name, goal_amount, contribution_per_period):
    # Initialize remaining balance as the goal amount (since nothing has been contributed yet)
    remaining_balance = goal_amount

    # Calculate how many periods (in months) are needed to reach the goal
    time_needed = remaining_balance / contribution_per_period
    
    # Store the account details in the dictionary
    savings_accounts[account_name] = {
        'goal': goal_amount,
        'remaining_balance': remaining_balance,
        'contribution': contribution_per_period,
        'time_needed': time_needed
    }
    
    save_data(data)
    time.sleep(1)
    
    print(f"Savings account '{account_name}' created!")
    time.sleep(0.5)
    print(f"It will take {time_needed} months to save {goal_amount} with contributions of {contribution_per_period} per month.")
    
    return_to_menu_or_exit()

def view_savings_accounts():
    print("\nSavings Accounts:")
    
    # Check if there are any to view
    if not data["savings_accounts"]:
        print("No savings accounts available.")
    else:
        # Sets the structure for viewing
        for account_name, details in data["savings_accounts"].items():
            print(f"Account Name: {account_name}")
            print(f" - Goal Amount: {details['goal']:.2f}")
            print(f" - Remaining Balance: {details['remaining_balance']:.2f}")
            print(f" - Contribution per Month: {details['contribution']:.2f}")
            print(f" - Time Needed to Reach Goal: {details['time_needed']} months")
            print() # Blank space between accounts
    
    # Provides a chance to delete account
    choice = input("\nWould you like to delete a savings account? (yes/no): ").strip().lower()
    
    if choice == "yes":
        account_name = input("Enter the name of the savings account you want to delete: ")
        delete_savings_account(account_name)
    
    return_to_menu_or_exit()

def transfer_to_savings(account_name, transfer_amount):
    # Check if the account exists
    if account_name in savings_accounts:
        # Ensure that the transfer amount does not exceed the available income
        global total_income, total_expenses # To indicate the global variables and not new variables
        
        if transfer_amount > total_income:
            print(f"Error: Insufficient Funds")
        
        # Deduct the transfer amount from income
        total_income -= transfer_amount
        print(f"${transfer_amount} transferred from income.")
        
        # Add the transfer amount to expenses
        total_expenses += transfer_amount
        expense_list[account_name] = transfer_amount
        print(f"${transfer_amount} added to expenses.")
        
        # Subtract the transfer amount from the savings account's remaining balance
        savings_accounts[account_name]['remaining_balance'] -= transfer_amount
        
        # Check if the goal has been reached or exceeded
        if savings_accounts[account_name]['remaining_balance'] <= 0:
            savings_accounts[account_name]['remaining_balance'] = 0
            print(f"Congratulations! You've reached your savings goal for '{account_name}!")
        
        # Recalculate the time needed to reach the savings goal based on the new remaining balance
        remaining_balance = savings_accounts[account_name]['remaining_balance']
        contribution_per_period = savings_accounts[account_name]['contribution']
        savings_accounts[account_name]['time_needed'] = remaining_balance / contribution_per_period if remaining_balance > 0 else 0
        
        # Save the data to the JSON file
        save_data(data)
        print(f"${transfer_amount} successfully transferred to the savings account '{account_name}'.")
        print(f"New remaining balance: {remaining_balance}")
        print(f"New time to reach goal: {savings_accounts[account_name]['time_needed']} per month.")
    else:
        print(f"Savings account '{account_name}' not found.")
    return_to_menu_or_exit()

def transfer_from_savings(account_name, transfer_amount):
    # Check for account
    if account_name in savings_accounts:
        global total_income, total_expenses
        
        # Checks for sufficient funds
        if transfer_amount > (account_name['goal'] - account_name['remaining_balance']):
            print(f"Error: Insufficient Funds")
        
        # Transfer added to total balance
        balance += transfer_amount
        print(f"{transfer_amount} transferred from income.")
        
        # Transfer added to income list
        income_list[account_name] = transfer_amount
        print(f"{transfer_amount} added to income.")
        
        # Savings account remaining balance recalculated
        savings_accounts[account_name]['remaining_balance'] += transfer_amount
        
        # Contributions per period recalculated
        remaining_balance = savings_accounts[account_name]['remaining_balance']
        contribution_per_period = savings_accounts[account_name]['contribution']
        savings_accounts[account_name]['time_needed'] = remaining_balance / contribution_per_period
        
        save_data(data)
       
        print(f"${transfer_amount} successfully transferred to your available balance.")
        print(f"New remaining balance: {remaining_balance}")
        print(f"New time to reach goal: {savings_accounts[account_name]['time_needed']} per month.")
    
    else:
        print(f"Savings account '{account_name}' not found.")
    
    return_to_menu_or_exit()

# Menu

def main_menu():
    global data
    
    # Loads JSON file
    data = load_data()
    
    # Pulls last startup time from JSON file
    last_startup = data["last_startup"]
    
    print("\nBudget Tracker\n")
    
    # Lists the processed recurring bills between startup times
    processed_bills = process_recurring_bills(last_startup)
    if processed_bills:
        print("\nProcessed Recurring Bills Since Last Startup:")
        for message in processed_bills:
            print(message)
        print("\n")
    else:
        print("\nNo recurring bills processed since last startup.\n")
    
    #Updates startup time
    data["last_startup"] = datetime.now()
    save_data(data)
    
    # Menu options
    while True:
        print("\nMain Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance and Summary")
        print("4. Add Bill to Calendar")
        print("5. View Bills/Upcoming Bills")
        print("6. Create Savings Account")
        print("7. View Savings Account Details")
        print("8. Add to Savings")
        print("9. Transfer from Savings")
        print("10. Exit")

        # Initial user input
        choice = input("What would you like to do?: ")

        if choice == "1":
            amount = float(input("Amount (in USD): $"))
            description = input("Provide a brief, 1-3 word description: ")
            add_income(amount, description)
        
        elif choice == "2":
            amount = float(input("Amount (in USD): $"))
            description = input("Provide a brief, 1-3 word description: ")
            add_expense(amount, description)
        
        elif choice == "3":
            print("1. View Balance")
            print("2. View Summary")
            choice2 = input("Choose 1 or 2: ")
            
            if choice2 == "1":
                view_balance()
            elif choice2 == "2":
                view_summary()
        
        elif choice == "4":
            name = input("What is the name for this bill? ")
            date_str = input("What is the due date? Enter YYYY, DD, MM: ")
            amount = input("What is the amount (in USD)? $")
            is_recurring = input("Is this a recurring bill? (yes/no): ").strip().lower() == "yes"
            interval = None
            
            if is_recurring:
                interval = input("How often does it recur? (weekly/monthly): ").strip().lower()
            add_bill(name, date_str, amount, recurring=is_recurring, interval=interval)
        
        elif choice == "5":
            print("1. View Bills")
            print("2. View Upcoming Bills")
            choice3 = input("Choose 1 or 2: ")
            
            if choice3 == "1":
                view_bills()
            elif choice3 == "2":
                view_upcoming_bills()
        
        elif choice == "6":
            account_name = input("What would you like to name this account? ")
            goal_amount = input("What is the amount (in USD) you'd like to save? $")
            contribution_per_period = input("How much would you like to save (in USD) towards this goal, per month? $")
            add_savings_account(account_name, goal_amount, contribution_per_period)
        
        elif choice == "7":
            view_savings_accounts()
        
        elif choice == "8":
            account_name = input("What account would you like to transfer money to? ")
            transfer_amount = input("What amount (in USD) would you like to transfer? $")
            transfer_to_savings(account_name, transfer_amount)
        
        elif choice == "9":
            account_name = input("What account would you like to transfer money out of? ")
            transfer_amount = input("What amount (in USD) would you like to transfer to your available balance? $")
            transfer_from_savings(account_name, transfer_amount)
        
        elif choice == "10":
            print("Exiting from program...")
            exit()
    
    else:
        print("Invalid choice. Please try again: ")

# Run Budget Tracker
main_menu()

# NOTES
#
# 
# 
#
#