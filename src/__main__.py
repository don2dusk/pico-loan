import fun
import db

name: str = "" # updates when user "logs in/registers"
foo: str = "y"
# Check if user exists, if not register user

db.init()
option = int(input("Welcome to Pico Investments! Please select what you want to do:\n1. Borrow Money\n2. Get summary\n"))
if option == 1:
    name = input("Enter your name: ")
    if not fun.user_exists(name):
        print("User does not exist! Creating user now...\n")
        amount = float(input("Enter the amount you want to borrow: $"))
        rate = float(input("Enter the rate you have been given: "))
        fun.register_user(name, amount, fun.toDecimal(rate))
    else:
        while foo == "y":
            print(f"You have ${fun.get_balance(name)} left to pay back\n")
            foo = input("Are you ready to make a payment? [y/n]: ")
            if foo == 'y':
                month = int(input("Enter the month (in digits) that you are paying for: "))
                amount = float(input("Enter the amount you are paying: $"))
                fun.compound_interest(name=name, amount_loaned=amount, rate=fun.get_rate(name))
                fun.make_payment(name=name, month_paid=month, amount=amount)
                foo = input("Do you want to perform another payment? [y/n]: ")
            else:
                exit()
elif option == 2:
    anotherOption = int(input("Choose an option:\n1. Show average income per month and highest earning month\n2. Show total money that has been loaned out\n3. Regression Analysis\n"))
    if anotherOption == 1:
        fun.company_average_income()
        exit()
    elif anotherOption == 2:
        print(f"Total money loaned out by Pico: ${fun.company_total_loan()}")
        exit()
    elif anotherOption == 3:
        print("Regression Analysis:\nSee pyplot graph")
        fun.regression_analysis()
    else:
        print("Invalid option!")
        exit()
else:
    print("Invalid option!")
    exit()

db.db.close()