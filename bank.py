from abc import ABC, abstractmethod

# Abstract base class for accounts (Abstraction)
class BankAccount(ABC):
    def __init__(self, account_number, account_holder, balance=0):
        self.__account_number = account_number
        self.__account_holder = account_holder
        self.__balance = balance

    # Encapsulation: Getters for private attributes
    def get_account_number(self):
        return self.__account_number

    def get_account_holder(self):
        return self.__account_holder

    def get_balance(self):
        return self.__balance

    # Encapsulation: Setter for updating balance
    def set_balance(self, balance):
        self.__balance = balance

    # Abstract method (Abstraction)
    @abstractmethod
    def withdraw(self, amount):
        pass

    # Common method for depositing money
    def deposit(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be greater than zero.")
            self.__balance += amount
            print(f"Deposit successful! New balance: {self.__balance}")
        except ValueError as e:
            print(f"Error: {e}")

    # Polymorphism: String representation for all accounts
    def __str__(self):
        return f"Account[{self.__account_number}]: {self.__account_holder}, Balance: {self.__balance}"

# SavingsAccount: Inherits from BankAccount
class SavingsAccount(BankAccount):
    def __init__(self, account_number, account_holder, balance=0, interest_rate=0.02):
        super().__init__(account_number, account_holder, balance)
        self.interest_rate = interest_rate

    # Overriding the withdraw method (Polymorphism)
    def withdraw(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be greater than zero.")
            if amount > self.get_balance():
                raise ValueError("Insufficient balance.")
            self.set_balance(self.get_balance() - amount)
            print(f"Withdrawal successful! New balance: {self.get_balance()}")
        except ValueError as e:
            print(f"Error: {e}")

    def apply_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.set_balance(self.get_balance() + interest)
        print(f"Interest applied! New balance: {self.get_balance()}")

# CurrentAccount: Inherits from BankAccount
class CurrentAccount(BankAccount):
    def __init__(self, account_number, account_holder, balance=0, overdraft_limit=500):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = overdraft_limit

    # Overriding the withdraw method with overdraft logic (Polymorphism)
    def withdraw(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be greater than zero.")
            if amount > self.get_balance() + self.overdraft_limit:
                raise ValueError("Overdraft limit exceeded.")
            self.set_balance(self.get_balance() - amount)
            print(f"Withdrawal successful! New balance: {self.get_balance()}")
        except ValueError as e:
            print(f"Error: {e}")

# Bank System for managing multiple accounts
class BankSystem:
    def __init__(self):
        self.accounts = {}

    # Create a new account
    def create_account(self, account_type, account_number, account_holder):
        if account_number in self.accounts:
            print("Account already exists!")
        else:
            if account_type == "savings":
                account = SavingsAccount(account_number, account_holder)
            elif account_type == "current":
                account = CurrentAccount(account_number, account_holder)
            else:
                print("Invalid account type!")
                return
            self.accounts[account_number] = account
            print(f"{account_type.capitalize()} account created successfully!")

    # Retrieve an account
    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    # Main system menu
    def run(self):
        while True:
            print("\n--- Bank Management System ---")
            print("1. Create Account")
            print("2. View Account Details")
            print("3. Deposit Money")
            print("4. Withdraw Money")
            print("5. Apply Interest (Savings Account)")
            print("6. Exit")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    account_type = input("Enter account type (savings/current): ").lower()
                    account_number = input("Enter account number: ")
                    account_holder = input("Enter account holder name: ")
                    self.create_account(account_type, account_number, account_holder)

                elif choice == 2:
                    account_number = input("Enter account number: ")
                    account = self.get_account(account_number)
                    if account:
                        print(account)
                    else:
                        print("Account not found!")

                elif choice == 3:
                    account_number = input("Enter account number: ")
                    account = self.get_account(account_number)
                    if account:
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    else:
                        print("Account not found!")

                elif choice == 4:
                    account_number = input("Enter account number: ")
                    account = self.get_account(account_number)
                    if account:
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    else:
                        print("Account not found!")

                elif choice == 5:
                    account_number = input("Enter account number: ")
                    account = self.get_account(account_number)
                    if isinstance(account, SavingsAccount):
                        account.apply_interest()
                    else:
                        print("Interest can only be applied to savings accounts.")

                elif choice == 6:
                    print("Exiting the system. Goodbye!")
                    break

                else:
                    print("Invalid choice. Please try again.")

            except ValueError as e:
                print(f"Error: Invalid input ({e})")

# Instantiate and run the system
if __name__ == "__main__":
    system = BankSystem()
    system.run()
