import json
import os
import random


class BankSystem:

    def __init__(self, filename="bank_data.json"):
        self.filename = filename
        self.accounts = self.load_data()

    def load_data(self):
        """Load account details from JSON file if available."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_data(self):
        """Save account details to JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.accounts, file, indent=4)

    def generate_account_number(self):
        """Generate a unique 6-digit account number."""
        while True:
            acc_num = str(random.randint(100000, 999999))
            if acc_num not in self.accounts:
                return acc_num

    def create_account(self):
        """Create a new bank account."""
        print("\n--- Create Account ---")
        name = input("Enter account holder name: ").strip()

        while True:
            try:
                pin = input("Set a 4-digit PIN: ").strip()
                if len(pin) == 4 and pin.isdigit():
                    break
                print("Invalid PIN. Must be exactly 4 digits.")
            except ValueError:
                print("Invalid input.")

        while True:
            try:
                initial_deposit = float(
                    input("Enter initial deposit amount ($): ")
                )
                if initial_deposit >= 0:
                    break
                print("Initial deposit cannot be negative.")
            except ValueError:
                print("Please enter a valid number.")

        acc_num = self.generate_account_number()
        self.accounts[acc_num] = {
            "name": name,
            "pin": pin,
            "balance": initial_deposit,
            "transactions": [f"Account opened with deposit: ${initial_deposit:.2f}"],
        }

        self.save_data()
        print(
            f"\nAccount created successfully!"
        )
        print(f"Account Number: {acc_num}")

    def authenticate(self, acc_num, pin):
        """Verify account number and PIN."""
        if acc_num in self.accounts and self.accounts[acc_num]["pin"] == pin:
            return True
        return False

    def deposit(self):
        """Deposit funds into an account."""
        print("\n--- Deposit Money ---")
        acc_num = input("Enter account number: ").strip()
        pin = input("Enter PIN: ").strip()

        if self.authenticate(acc_num, pin):
            try:
                amount = float(input("Enter deposit amount ($): "))
                if amount > 0:
                    self.accounts[acc_num]["balance"] += amount
                    self.accounts[acc_num]["transactions"].append(
                        f"Deposited: ${amount:.2f}"
                    )
                    self.save_data()
                    print(
                        f"Successfully deposited ${amount:.2f}. New Balance: ${self.accounts[acc_num]['balance']:.2f}"
                    )
                else:
                    print("Deposit amount must be greater than zero.")
            except ValueError:
                print("Invalid amount format.")
        else:
            print("Invalid Account Number or PIN.")

    def withdraw(self):
        """Withdraw funds from an account."""
        print("\n--- Withdraw Money ---")
        acc_num = input("Enter account number: ").strip()
        pin = input("Enter PIN: ").strip()

        if self.authenticate(acc_num, pin):
            try:
                amount = float(input("Enter withdrawal amount ($): "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                elif amount > self.accounts[acc_num]["balance"]:
                    print("Insufficient funds.")
                else:
                    self.accounts[acc_num]["balance"] -= amount
                    self.accounts[acc_num]["transactions"].append(
                        f"Withdrew: ${amount:.2f}"
                    )
                    self.save_data()
                    print(
                        f"Successfully withdrew ${amount:.2f}. Remaining Balance: ${self.accounts[acc_num]['balance']:.2f}"
                    )
            except ValueError:
                print("Invalid amount format.")
        else:
            print("Invalid Account Number or PIN.")

    def transfer(self):
        """Transfer funds between accounts."""
        print("\n--- Transfer Funds ---")
        sender_acc = input("Enter your account number: ").strip()
        pin = input("Enter PIN: ").strip()

        if self.authenticate(sender_acc, pin):
            receiver_acc = input("Enter receiver account number: ").strip()

            if receiver_acc not in self.accounts:
                print("Receiver account not found.")
                return

            if sender_acc == receiver_acc:
                print("Cannot transfer money to the same account.")
                return

            try:
                amount = float(input("Enter amount to transfer ($): "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                elif amount > self.accounts[sender_acc]["balance"]:
                    print("Insufficient balance.")
                else:
                    # Execute Transfer
                    self.accounts[sender_acc]["balance"] -= amount
                    self.accounts[receiver_acc]["balance"] += amount

                    self.accounts[sender_acc]["transactions"].append(
                        f"Transferred ${amount:.2f} to Acc #{receiver_acc}"
                    )
                    self.accounts[receiver_acc]["transactions"].append(
                        f"Received ${amount:.2f} from Acc #{sender_acc}"
                    )

                    self.save_data()
                    print(
                        f"Successfully transferred ${amount:.2f} to Account #{receiver_acc}."
                    )
            except ValueError:
                print("Invalid amount format.")
        else:
            print("Invalid Account Number or PIN.")

    def check_balance(self):
        """Display balance and account information."""
        print("\n--- Account Details & Balance ---")
        acc_num = input("Enter account number: ").strip()
        pin = input("Enter PIN: ").strip()

        if self.authenticate(acc_num, pin):
            acc = self.accounts[acc_num]
            print(f"\nAccount Holder: {acc['name']}")
            print(f"Account Number: {acc_num}")
            print(f"Current Balance: ${acc['balance']:.2f}")
            print("\nRecent Transactions:")
            for txn in acc["transactions"][-5:]:  # Display last 5
                print(f" - {txn}")
        else:
            print("Invalid Account Number or PIN.")


def main():
    bank = BankSystem()

    while True:
        print("\n" + "=" * 35)
        print("    BANKING MANAGEMENT SYSTEM    ")
        print("=" * 35)
        print("1. Create New Account")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Transfer Funds")
        print("5. Check Balance & History")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.deposit()
        elif choice == "3":
            bank.withdraw()
        elif choice == "4":
            bank.transfer()
        elif choice == "5":
            bank.check_balance()
        elif choice == "6":
            print("\nThank you for using the Banking Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1 to 6.")


if __name__ == "__main__":
    main()