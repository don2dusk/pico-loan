import db
import datetime
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt

def toDecimal(value: float) -> float:
    if value < 1:
        return value
    else:
        return value/100
    

def get_rate(name: str) -> float:
    rateQuery = db.User.select().where(db.User.name == name).get();
    rate: float = rateQuery.rate
    return rate


def register_user(name: str, amount_loaned: float, rate: float) -> None: # creates a new user
    newUser = db.User.create(name=name, balance=amount_loaned, amount_loaned=amount_loaned, rate=rate)
    print("User created successfully!")

def get_total_value(item):
    return item[1]

def company_average_income() -> None: # returns monthly average income the company receives
    income_table: list = []
    total_list: list = []
    for i in range(1, 13):
        query = db.Payment.select().where(db.Payment.month_paid == i)
        length: int = 1 if len(list(query)) == 0 else len(list(query))
        income: float = 0.0
        for amount in query:
            income += amount.amount_paid
        
        month: str = datetime.date(2024, i, 1).strftime('%B')
        total_list.append([month, income])
        income_table.append([month, income/length])
    
    print(tabulate(income_table, headers=['Month', 'Average Income'], floatfmt=('.2f'), tablefmt='grid'))

    max_value = max(total_list, key=get_total_value)

    print(f"Highest earning month: {max_value[0]}")

def company_total_loan() -> float: # Returns the total amount loaned
    total: float = 0.0
    query: list[db.User] = db.User.select()
    for loan in query:
        total += loan.amount_loaned
    return total

def compound_interest(name: str, amount_loaned: float, rate: float) -> float:
    print(rate)
    interest: float = ((amount_loaned ** (1 + rate)) - amount_loaned) / 12
    balance_query = db.User.select().where(db.User.name == name)
    for user in balance_query:
        user.balance -= amount_loaned
        user.balance += interest
        user.save()
    return interest


def user_exists(username: str) -> bool:
    try:
        db.User.select().where(db.User.name == username).get()
        return True
    except:
        return False
    
def get_balance(name: str) -> float:
    query = db.User.select().where(db.User.name == name).get()
    current_balance: float = query.balance

    return current_balance

def make_payment(name: str, month_paid: int, amount: float) -> None:
    current_balance: float = get_balance(name)
    db.Payment.create(user=name, amount_paid=amount, month_paid=month_paid, balance=current_balance)
    print(f"Payment of ${amount} successful!")

def regression_analysis():
    months: list = []
    future_months: list = []
    money_loaned: list = []
    for i in range(1, 13):
        query = db.Payment.select().where(db.Payment.month_paid == i)
        income: float = 0.0
        for amount in query:
            income += amount.amount_paid
        if income == 0.0:
            future_months.append(i)
        else:
            months.append(i)
            money_loaned.append(income)
    
    months_reg = np.array(months)
    money_loaned_reg = np.array(money_loaned)
    future_months_reg = np.array(future_months)

    slope, intercept = np.polyfit(months, money_loaned, 1)

    predicted_money = slope * future_months_reg + intercept
    
    print("Regression Formula: Money Loaned = {:.2f} * Months + {:.2f}".format(slope, intercept))

    plt.scatter(months, money_loaned_reg, color='blue')
    plt.plot(months, slope * months_reg + intercept, color='red', linestyle='--')
    plt.scatter(future_months_reg, predicted_money, color='green', marker='x')
    plt.xlabel('Months')
    plt.ylabel('Money Loaned')
    plt.title('Regression Analysis: Months vs Money Loaned')
    plt.legend(['Regression Line', 'Current Data', 'Predicted Data'])
    plt.grid(True)
    plt.show()
