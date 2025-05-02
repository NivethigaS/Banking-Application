import os
from datetime import datetime

#========================CREATE ACCOUNT NUMBER==============================##
def generate_account_number():
    filename = "account_number.txt"

    if not os.path.exists("account_number.txt"):
        with open("account_number.txt", "w") as file:
            file.write("100100")

    with open("account_number.txt", "a") as file:
        last_number = int(file.read().strip())

    new_number = last_number + 1

    with open("account_number.txt", "r") as file:
            file.write(str(new_number))    

    return str(new_number)    
            

#=======================ADMIN REGISTRATION===================================##
def register_admin():
    if not os.path.exists("admin.txt"):
        with open("admin.txt","w") as file:
            file.write(f"001 | Admin | admin01 | pass@01\n")
        print("Admin Details Created Successfully.")
        print("Admin User ID: 001")

    else:
        print("Admin already registered.")    
        print("----------------------------------")
   
#========================ADMIN LOGIN=========================================##
def view_all_account():
    print("\n------All Customer Accounts-----")
    if not os.path.exists("accounts.txt"):
        print("No accounts to display.")
        return
    
    with open("accounts.txt", "r") as file:
        for line in file:
            acc_no, name, balance = line.strip().split(" | ")
            print(f"Account: {acc_no}, Name: {name}, Balance: {balance}")


def view_all_customers():
    print("\n------All Customer Details-----")
    if not os.path.exists("user.txt"):
        print("No customers found.")
        return
    
    with open("user.txt", "r") as file:
        for line in file:
            user_id, name, acc_no, NIC_Number, address, balance, username, password = line.strip().split(" | ")
            print(f"User ID: {user_id}")
            print(f"Name: {name}")
            print(f"Account Number: {acc_no}")
            print(f"NIC: {NIC_Number}")
            print(f"Address: {address}")
            print(f"Balance: {balance}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            

def admin_login():
    username= input("Enter Admin Username: ")
    password= input("Enter Admin Password: ")

    try:
        with open("admin.txt", "r") as file:
            data = file.readline().strip()
            admin_ID, role, saved_username, saved_password = data.split(" | ")

            if username == saved_username and password ==saved_password:
                print("Login Successful, Welcome Admin! ")

                while True:
                    print("\n--- Admin Menu ---")
                    print("1. View All Accounts")
                    print("2. View All Customers")
                    print("3. Logout")
                    admin_choice = input("Enter choice: ")
                    if admin_choice == "1":
                        view_all_account()
                    elif admin_choice == "2":
                        view_all_customers()
                    elif admin_choice == "3":
                        break    
                    else:
                        print("Invalid choice.")

            else:
                print("Invalid username or password. ") 

    except FileNotFoundError:
        print("Admin not registered yet.")  


#===========================CREATE NEW CUSTOMER======================================##
def create_new_customer():
    name = input("Enter Customer Name: ")
    account_number = generate_account_number()

    try:
        balance = float(input("Enter Initial Balance: "))
    except ValueError:
        print("Invalid amount! Please enter a number. ")
        return
        
    NIC_Number = input("Enter IC number: ")
    address =input("Enter your address: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        with open("user.txt", "r") as file:
            for line in file:
                details = line.strip().split(" | ")
                if len(details) >= 7:
                    existing_username = details[6]
                    if username == existing_username:
                        print("Username already taken!")
                        return
    except FileNotFoundError:
        pass 

    user_id = "CUS" + str(account_number)[-3:]

    with open("user.txt", "a") as file:
        file.write(f"{user_id} | {name} | {account_number} | {NIC_Number} | {address} | {balance} | {username} | {password}\n")

    with open("accounts.txt", "a") as file:
        file.write(f"{account_number} | {name} | {balance}\n")
       
    print("User Created Successfully!") 
    print("Customer USer ID:", user_id)
    print("Account Number: ", account_number)


#=============================CUSTOMER LOGIN======================================#
def customer_login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if not os.path.exists("user.txt"):
        print("No Customers registered yet.")
        return
    
    with open("user.txt", "r") as file:
        for line in file:
            details = line.strip().split(" | ")
            if len(details) >= 8:
                user_id, name, acc_no, balance, NIC_Number, address, saved_user, saved_pass = details
                if username == saved_user and password == saved_pass:
                    print(f"\nWelcome {name}!")
                    customer_menu(acc_no)
                    return
            
    print("Invalid username or password.")
                    

#=======================DEPOSIT FUNCTON========================================#
def deposit(account_number):
    try:
        amount = float(input("Enter amount to deposit: "))
    except ValueError:
        print("Invalid amount.")
        return
        
    updated = False
    new_balance = 0
    lines =[]

    if not os.path.exists("accounts.txt"):
        print("No account data found.")
        return

    with open("accounts.txt", "r") as file:
        for line in file:
            acc_no, name, balance = line.strip(). split(" | ")
            if acc_no == account_number:
                new_balance =float(balance) + amount
                updated_line = f"{acc_no} | {name} | {new_balance}\n"
                lines.append(updated_line) 
                updated = True
            else:
                lines.append(line)    

    with open ("accounts.txt", "w") as file:
        file.writelines(lines)

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open("transactions.txt", "a") as file:
        file.write(f"{account_number} | Deposi | {amount} | {timestamp}\n")

    if updated:
        print("Deposit Successful! Your current balance is:", new_balance )       

    else:
        print("Account not found.")        

#============================WITHDRAW FUNCTION====================================#
def withdraw(account_number):
    try:
        amount = float(input("Enter amount to withdraw: "))
    except ValueError:
        print("Invalid amount: ")
        return
        
    found = False
    updated_lines =[]
    new_balance = 0

    with open("accounts.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
            acc_no, name, balance = line.strip().split(" | ")

            if acc_no == account_number:
                found = True
                balance = float(balance)
                if balance >= amount:
                    new_balance = balance - amount
                    line = f"{acc_no} | {name} | {new_balance}\n"
                    print("Withdraw Successful! Your Current Balance is: ", new_balance)
                    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    with open("transactions.txt", "a") as file:
                        file.write(f"{account_number} | Withdraw | {amount} | {timestamp}\n")
                else:
                    print("Insufficient balance.")    
            updated_lines.append(line)
        
    if found:
        with open("accounts.txt", "w") as file:
            file.writelines(updated_lines)

    else:
        print("Account not found.")        

#======================CHECK BALANCE================================#
def check_balance(account_number):
    with open("accounts.txt", "r") as file:
        for line in file:
            acc_no, name, balance = line.strip().split(" | ")
            if acc_no == account_number:
                print(f"Current balance: {balance}")
                break

#=============================TRANSACTION HISTORY====================#
def view_transactions(account_number):
    print("\n Transaction History: ")
    if not os.path.exists("transactions.txt"):
        print("No transactions found.")
        return
    
    found = False
    with open ("transactions.txt", "r") as file:
        for line in file:
            acc_no, t_type, amut, timestamp = line.strip().split(" | ")
            if acc_no == account_number:
                print(f"{timestamp} - {t_type}: {float(amut)}")
                found = True
    if not found:
        print("No transactions for this account.") 
        return       

#====================================DELETE ACCOUNT======================#
def delete_account(account_number, username, password):
    found = False

    if os.path.exists("user.txt"):
        with open("user.txt", "r") as file:
            users = file.readlines()
    
    with open("user.txt", "w") as file:
        for line in users:
            details = line.strip().split(" | ")
            if len(details) >=8:
                user_id, name, account_no, balance, NIC_Number, address, user_name, pwd = details    
                if account_no == account_number and user_name == username and pwd == password:
                    found = True
                    continue

            file.write(line)

    if found:
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as file:
                accounts = file.readlines()
            with open("accounts.txt", "w") as file:
                for line in accounts:
                    acc_no, user_name, pwd = line.strip().split(" | ")
                    if account_no != account_number:
                        file.write(line)
        print("Your account has been deleted successfully.")
    
    else:
        print("Account not found.")

#=========================CUSTOMER MENU====================================#
def customer_menu(account_number):
    while True:
        print("\n------Customer Menu-----")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4.View Transactions")
        print("5. Delete Account")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice =="1":
            deposit(account_number)

        elif choice =="2":
            withdraw(account_number)

        elif choice =="3":
            check_balance(account_number)

        elif choice =="4":
            view_transactions(account_number)

        elif choice =="5":
            print("\nPlease confirm account details to delete.")

            acc_no = input("Enter account number: ")
            user_name = input("Enter username: ")
            pwd = input("Enter password: ") 

            if acc_no == account_number:
                delete_account(acc_no, user_name, pwd)
            else:
                print("Account number doesn't match.")    
            

        elif choice =="6":
            break

        else:
            print("Invalid choice. Try again.")                   


#==============================MAIN MENU==============================================##
def main_menu():
    register_admin()

    while True:
        print("------------------------")
        print("\n WELCOME TO MINI BANKING APP")
        print("------------------------")
        print("1.Login")
        print("2.Exit")

        choice = input("Enter your choice: ")

        if choice =="1":
            print("\n---- Login Menu----")
            print("1. Admin Login")
            print("2. Customer Login")
            role = input("Login as: ")

            if role =="1":
                admin_login()
            elif role =="2":
                print("\n--Customer Type--") 
                print("1.New Customer")   
                print("2. Existing Customer")
                cust_type = input("Enter choice: ")

                if cust_type =="1":
                    create_new_customer()
                elif cust_type =="2":
                    customer_login()
                else:
                    print("Invalud choice.")
            else:
                print("Invalid login role selected.")

        elif choice =="2":
            print("Thank you! for using the App..")      
            break
        else:
            print("Invalid choice. Try again.") 

main_menu()   
                     
            



                                                         





























































 