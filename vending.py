from dataclasses import dataclass
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
        for i, item in enumerate(self.items):
            print(f"#{i+1} {item.name:20s} {item.price / 100.0:0.2f} €  (available: {item.amount})")

    def check_deposit(self, deposit):
        try:
            deposit = int(float(deposit) * 100)
        except TypeError:
            return False
        return deposit % 5 == 0

    def item_available(self, selection):
        try:
            selection = int(selection)
        except TypeError:
            print("Selection is not a number")
            return False

        if not (1 <= selection <= len(self.items)):
            print("Invalid selection")
            return False

        return self.items[selection -1 ].amount > 0

    def can_buy(self, selection, deposit):
        item = self.items[int(selection) - 1]
        deposit = float(deposit) * 100 # prices are in cents
        return deposit > item.price

    def buy(self, selection, deposit):

        self.items[int(selection) - 1].amount -= 1

        change = 0
        return change


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

            print("Your change is {change:0.2lf} €")


def main():
    inventory = Inventory(
        items= [
            Item(name="Water", amount=10, price=50),
            Item(name="Coke", amount=10, price=120),
            Item(name="Diet Coke", amount=10, price=120),
            Item(name="Ice Tea", amount=10, price=100),
            Item(name="Chokolade", amount=10, price=150),
            Item(name="Candy", amount=10, price=95),
            Item(name="Chips", amount=10, price=250),
            Item(name="Espresso", amount=10, price=120),
            Item(name="Coffee", amount=10, price=150),
        ])

    print(inventory.items)
    inventory.run()



if __name__ == "__main__":
    main()
