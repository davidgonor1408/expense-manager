import time
import numpy as np
import pandas as pd

EXPENSE_ID = "expense_id"
PRICE = "price"
DESCRIPTION = "description"
CSV_FILE = 'out.csv'


class ExpenseManager:
    def __init__(self):
        self.expenses = {}
        try:
            df = pd.read_csv(CSV_FILE, index_col=0)
            for ind, row in df[[PRICE, DESCRIPTION]].iterrows():
                self.expenses[ind] = {PRICE: row[PRICE], DESCRIPTION: row[DESCRIPTION]}
        except FileNotFoundError:
            pass
        self.MANAGER_ACTIONS = {
            "Add a new expense": self.add_new_expense,
            "Edit an existing expense": self.edit_expense,
            "List expenses": self.list_expenses,
        }
    
    def add_new_expense(self, ts=None):
        price = float(input("Price: "))
        desc = input("Description: ")
        new_expense = {
            PRICE: price,
            DESCRIPTION: desc
        }
        if not ts:
            ts = int(time.time())
        self.expenses[ts] = new_expense
        print(f"{ts}: {new_expense}")
        df = pd.DataFrame.from_dict(self.expenses, orient='index')
        df.to_csv('out.csv', header=[PRICE, DESCRIPTION])

    def edit_expense(self):
        expense_id = int(input("Expense ID: "))
        while expense_id not in self.expenses:
            if expense_id == 0:
                return
            expense_id = int(input("Expense ID: "))
        self.add_new_expense(ts=expense_id)

    def list_expenses(self):
        print(self.expenses)


if __name__ == '__main__':
    print("Welcome to your expense manager")
    print("Please select an action:")
    em = ExpenseManager()
    actions_list = list(em.MANAGER_ACTIONS.keys())
    while True:
        for index, action in enumerate(actions_list):
            print(f"{index + 1}: {action}")
        print("0: Quit")
        try:
            user_action = int(input())
            if user_action == 0:
                break
            em.MANAGER_ACTIONS[actions_list[user_action - 1]]()
        except (ValueError, IndexError):
            print("ERROR - Invalid Input")
            continue
