
class Cart:
    def __init__(self):
        self.items = {}  # Stores items with their names as keys and quantities as values

    def add_to_cart(self, item_name, quantity):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        print(f"Added {quantity} of '{item_name}' to the cart.")

    def remove_from_cart(self, item_name, quantity):
        if item_name in self.items:
            if self.items[item_name] > quantity:
                self.items[item_name] -= quantity
                print(f"Removed {quantity} of '{item_name}' from the cart.")
            elif self.items[item_name] == quantity:
                del self.items[item_name]
                print(f"Removed all of '{item_name}' from the cart.")
            else:
                print(f"Cannot remove {quantity}; only {self.items[item_name]} available.")
        else:
            print(f"'{item_name}' is not in the cart.")

    def view_cart(self):
        if not self.items:
            print("The cart is empty.")
        else:
            print("\n--- Cart Contents ---")
            for item_name, quantity in self.items.items():
                print(f"- {item_name}: {quantity}")

    def calculate_checkout(self, db):
        if not self.items:
            print("The cart is empty. Nothing to calculate.")
        total = 0
        print("\n--- Checkout ---")
        for item_name, quantity in self.items.items():
            # Fetch the price of the item from the database
            item_price = db.get_item_price(item_name)
            if item_price is not None:
                item_total = item_price * quantity
                total += item_total
                print(f"{item_name} (x{quantity}): ${item_total:.2f}")
            else:
                print(f"Error: Price not found for {item_name}.")
        print(f"\nTotal checkout amount: ${total:.2f}")