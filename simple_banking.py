# if the user asks for Balance, you should read the balance of the account from the database and output it into the console.
#
# Add income item should allow us to deposit money to the account.
#
# Do transfer item should allow transferring money to another account. You should handle the following errors:
#
# If the user tries to transfer more money than he/she has, output: Not enough money!
# If the user tries to transfer money to the same account, output the following message: You can't transfer money to the same account!
# If the receiver's card number doesn’t pass the Luhn algorithm, you should output: Probably you made a mistake in the card number. Please try again!
# If the receiver's card number doesn’t exist, you should output: Such a card does not exist.
# If there is no error, ask the user how much money they want to transfer and make the transaction.
# If the user chooses the Close account item, you should delete that account from the database.
#

import random
import sqlite3

accounts = []

db = sqlite3.connect("card.s3db")
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS card "
            "(id INTEGER,"
            " number TEXT,"
            " pin TEXT,"
            " balance INTEGER DEFAULT 0)")
db.commit()


class Account:

    def __init__(self, card=None):
        account_cards = [number for number in
                         cur.execute("SELECT number FROM card").fetchall()]
        if card:
            info = cur.execute("SELECT number, pin, balance"
                               " FROM card WHERE (number = ?)", (card, ))\
                .fetchone()
            if info:
                self.card_number, self.pin, self.balance = info

        else:
            while True:
                self.card_number = "400000" \
                                       + str(random.randint(0, 999999999)).rjust(9, "0")
                self.card_number += check_sum(self.card_number, check_validity=False)
                if self.card_number not in account_cards:
                    break
            self.pin = str(random.randint(0, 9999)).rjust(4, "0")
            self.balance = 0

    def validate_login(self, card, pin):
        if self.pin == pin and self.card_number == card:
            return True

    def deposit(self, amount):
        if int(amount) > 0:
            self.balance += int(amount)
            cur.execute("UPDATE card SET balance = ? WHERE (number = ?)",
                        (self.balance, self.card_number))
            db.commit()

    def withdraw(self, amount):
        if self.balance >= int(amount):
            self.balance -= int(amount)
            cur.execute("UPDATE card SET balance = ? WHERE (number = ?)",
                        (self.balance, self.card_number))
            db.commit()

    def transfer(self, target, amount):
        if self.balance >= int(amount):
            self.balance -= int(amount)
            target.balance += int(amount)
            cur.execute("UPDATE card SET balance = ? WHERE (number = ?)",
                        (self.balance, self.card_number))
            cur.execute("UPDATE card SET balance = ? WHERE (number = ?)",
                        (target.balance, target.card_number))

            db.commit()


def check_sum(card_number, check_validity=True):
    mutated_card = ""
    if check_validity:
        card_number = card_number[:-1]
    for i in range(0, len(card_number)):
        if i % 2 == 0:
            if int(card_number[i]) * 2 > 9:
                mutated_card += str((int(card_number[i]) * 2) - 9)
            else:
                mutated_card += str(int(card_number[i]) * 2)
        else:
            mutated_card += card_number[i]
    sum_card = sum(int(i) for i in mutated_card)
    if sum_card % 10 == 0:
        return "0"
    return str(10 - (sum_card % 10))


def bank_system():

    def validate_input(inp):
        try:
            int(inp)
            return True
        except ValueError:
            return False

    def check_card(card):
        if db.execute("SELECT number "
                      "FROM card "
                      "WHERE number = ?", (card, )).fetchone():
            return Account(card)
        else:
            return None

    def logged_in(customer):
        menu_text = "1. Balance\n2. Add income" \
                    "\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit"
        valid_options = ["0", "1", "2", "3", "4", "5"]
        while True:
            print(menu_text)
            choice = input()
            if choice not in valid_options:
                print(menu_text)
                choice = input()
            if choice in valid_options:
                if choice == valid_options[0]:
                    print("Bye!")
                    break
                if choice == valid_options[1]:
                    print(f"Balance: {customer.balance}")
                if choice == valid_options[2]:
                    print("Add income: ")
                    amount = input()
                    if validate_input(amount):
                        customer.deposit(int(amount))
                        print("Income was added!")
                    else:
                        print("Enter a valid sum")
                if choice == valid_options[3]:
                    print("Transfer")
                    print("Enter card number:")
                    target_input = input()
                    if check_sum(target_input, True) == target_input[-1]:
                        target = check_card(target_input)
                        if target:
                            print("Enter how much money you want to transfer:")
                            transfer_amount = input()
                            if validate_input(transfer_amount):
                                if customer.balance >= int(transfer_amount):
                                    customer.transfer(target, transfer_amount)
                                    print("Success!")
                                else:
                                    print("Not enough money!")

                            else:
                                print("Enter a valid sum")
                        else:
                            print("Such a card does not exist.")
                    else:
                        print("Probably you made a mistake in the card number."
                              " Please try again!")

                if choice == valid_options[4]:
                    db.execute("DELETE FROM card WHERE number = ?",
                               (customer.card_number,))
                    db.commit()
                    print("The account has been closed!")
                    login_menu()
                    break
                if choice == valid_options[5]:
                    print("You have successfully logged out!")
                    break

    def login_menu():
        menu_text = "1. Create an account\n2. Log into account\n0. Exit\n"

        while True:
            valid_options = ["0", "1", "2"]
            choice = input(menu_text)
            if choice not in valid_options:
                choice = input(menu_text)

            if choice in valid_options:
                if choice == valid_options[0]:
                    print("Bye!")
                    break
                if choice == valid_options[1]:
                    account = Account()
                    print("Your card has been created")
                    print("Your card number:")
                    print(f"{account.card_number}")
                    print("Your card PIN:")
                    print(f"{account.pin}")
                    save = db.cursor()
                    save.execute("INSERT INTO card (number, pin)"
                                 " VALUES (?, ?)",
                                 (account.card_number, account.pin))
                    db.commit()

                if choice == valid_options[2]:
                    print("Enter your card number:")
                    card_n = input()
                    print("Enter your PIN:")
                    card_pin = input()
                    customer = check_card(card_n)
                    if customer:
                        if customer.validate_login(card_n, card_pin):
                            print("You have successfully logged in!")
                            logged_in(customer)
                        else:
                            print("Wrong card number or PIN!")
                    else:
                        print("Wrong card number or PIN!")

    login_menu()
    db.close()


if __name__ == "__main__":
    bank_system()

