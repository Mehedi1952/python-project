from abc import ABC, abstractmethod
import hashlib

# Abstract base class for accounts (Abstraction)
class BankAccount(ABC):
    def __init__(self, account_number, account_holder, balance=0):
        self.__account_number = account_number
        self.__account_holder = account_holder
        self.__balance = balance

    # Getters for private attributes
    def get_account_number(self):
        return self.__account_number

    def get_account_holder(self):
        return self.__account_holder

    def get_balance(self):
        return self.__balance

    # Setter for updating balance
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

# User Authentication and Bank System for managing multiple accounts
class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.users = {}  # {username: {password_hash, account_number}}

    # Hash password using SHA-256
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Create a new account
    def create_account(self, account_type, account_number, account_holder, password):
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
            password_hash = self.hash_password(password)
            self.users[account_holder] = {'password': password_hash, 'account_number': account_number}
            print(f"{account_type.capitalize()} account created successfully!")

    # User login
    def login(self, username, password):
        if username in self.users:
            stored_password = self.users[username]['password']
            if stored_password == self.hash_password(password):
                return self.users[username]['account_number']
            else:
                print("Invalid password!")
        else:
            print("User does not exist!")
        return None

    # Retrieve an account
    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    # Bank-to-Bank transaction
    def transfer(self, from_account_number, to_account_number, amount):
        try:
            from_account = self.get_account(from_account_number)
            to_account = self.get_account(to_account_number)
            if not from_account or not to_account:
                raise ValueError("Invalid account numbers.")
            if amount <= 0:
                raise ValueError("Transfer amount must be greater than zero.")
            if from_account.get_balance() < amount:
                raise ValueError("Insufficient balance.")
            from_account.set_balance(from_account.get_balance() - amount)
            to_account.set_balance(to_account.get_balance() + amount)
            print(f"Transfer successful! New balance of {from_account_number}: {from_account.get_balance()}")
        except ValueError as e:
            print(f"Error: {e}")

    # Main system menu
    def run(self):
        while True:
            print("\n--- Bank Management System ---")
            print("1. Create Account")
            print("2. Login")
            print("3. View Account Details")
            print("4. Deposit Money")
            print("5. Withdraw Money")
            print("6. Apply Interest (Savings Account)")
            print("7. Transfer Money")
            print("8. Exit")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    account_type = input("Enter account type (savings/current): ").lower()
                    account_number = input("Enter account number: ")
                    account_holder = input("Enter account holder name: ")
                    password = input("Enter password: ")
                    self.create_account(account_type, account_number, account_holder, password)

                elif choice == 2:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    account_number = self.login(username, password)
                    if account_number:
                        while True:
                            print(f"\nWelcome {username}! Your account: {account_number}")
                            print("1. View Account Details")
                            print("2. Deposit Money")
                            print("3. Withdraw Money")
                            print("4. Apply Interest (Savings Account)")
                            print("5. Transfer Money")
                            print("6. Logout")

                            try:
                                sub_choice = int(input("Enter your choice: "))
                                if sub_choice == 1:
                                    account = self.get_account(account_number)
                                    print(account)

                                elif sub_choice == 2:
                                    amount = float(input("Enter amount to deposit: "))
                                    account = self.get_account(account_number)
                                    account.deposit(amount)

                                elif sub_choice == 3:
                                    amount = float(input("Enter amount to withdraw: "))
                                    account = self.get_account(account_number)
                                    account.withdraw(amount)

                                elif sub_choice == 4:
                                    account = self.get_account(account_number)
                                    if isinstance(account, SavingsAccount):
                                        account.apply_interest()

                                elif sub_choice == 5:
                                    to_account_number = input("Enter recipient account number: ")
                                    amount = float(input("Enter amount to transfer: "))
                                    self.transfer(account_number, to_account_number, amount)

                                elif sub_choice == 6:
                                    print("Logged out successfully!")
                                    break

                                else:
                                    print("Invalid choice.")

                            except ValueError as e:
                                print(f"Error: {e}")

                elif choice == 8:
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
