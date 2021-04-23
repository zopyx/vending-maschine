from dataclasses import dataclass
from decimal import Decimal
import collections
import typing

@dataclass
class Item:
    name: str
    amount: int
    price: int   # euro cents


@dataclass
class Inventory:
    items: typing.List[Item]

    def print_items(self):
        """ Print items, their amount and price"""
        for i, item in enumerate(self.items):
            print(f"#{i+1} {item.name:20s} {item.price:0.2f} €  (available: {item.amount})")

    def check_deposit(self, deposit):
        """ Deposit must be a multiple of 0.05 euro cent"""
        try:
            deposit = int(Decimal(deposit) * 100)
        except Exception:
            return False

        if deposit <= 0:
            print("Improper deposit value")
            return False

        return deposit % 5 == 0

    def item_available(self, selection):
        """ Check if item is available """

        try:
            selection = int(selection)
        except ValueError:
            print("Selection is not a number")
            return False

        if not (1 <= selection <= len(self.items)):
            print("Invalid selection")
            return False

        return self.items[selection -1].amount > 0

    def can_buy(self, selection, deposit):
        """ Check deposit against item price """
        item = self.items[int(selection) - 1]
        deposit = Decimal(deposit)  # prices are in cents
        return deposit >= item.price

    def buy(self, selection, deposit):

        # decrease amount
        self.items[int(selection) - 1].amount -= 1

        # calculate change (coin values given in euro cent)
        coins = [100, 50, 20, 10, 5]
        diff = Decimal(deposit) - self.items[int(selection) - 1].price 

        change = []
        remaining = diff * 100
        while remaining != 0:
            for coin in coins:
                while True:
                    if remaining  >= coin:
                        remaining -= coin
                        change.append(coin / 100.0)
                    else:
                        break

        return collections.Counter(change)


    def run(self):

        while True:
            print()
            self.print_items()

            print()
            print("Your choice:")

            deposit = input("Deposit (in €): ")
            if not self.check_deposit(deposit):
                print("Invalid deposit - a deposit must be given a multiple of 0.05 €")
                continue

            selection = input("Selection: ")
            if not self.item_available(selection):
                print("Item is not available")
                continue

            if not self.can_buy(selection, deposit):
                print("Not enough deposit")
                continue

            change = self.buy(selection, deposit)
            if change:
                print(f"Your change in Coins is {change} ")
                for k, v in change.items():
                    print(f"{v} x {k} €")
            else:
                print("No change")


def main():
    inventory = Inventory(
        items= [
            Item(name="Water", amount=10, price=Decimal("0.50")),
            Item(name="Coke", amount=10, price=Decimal("1.20")),
            Item(name="Diet Coke", amount=10, price=Decimal("1.20")),
            Item(name="Ice Tea", amount=10, price=Decimal("1.00")),
            Item(name="Chokolade", amount=10, price=Decimal("1.50")),
            Item(name="Candy", amount=10, price=Decimal("0.95")),
            Item(name="Chips", amount=10, price=Decimal("2.50")),
            Item(name="Espresso", amount=10, price=Decimal("1.20")),
            Item(name="Coffee", amount=10, price=Decimal("1.50")),
        ])

    inventory.run()

if __name__ == "__main__":
    main()
