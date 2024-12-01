class Cart:
    def __init__(self):
        self.items = {}  # Initialize an empty dictionary to store cart items

    def add_to_cart(self, product, quantity):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity
        print(f"Added {quantity} x {product.name} to the cart.")

    def remove_from_cart(self, product, quantity):
        if product in self.items:
            if self.items[product] > quantity:
                self.items[product] -= quantity
                print(f"Removed {quantity} x {product.name} from the cart.")
            else:
                print(f"Removed {self.items[product]} x {product.name} from the cart.")
                del self.items[product]
        else:
            print(f"{product.name} is not in the cart.")

    def calculate_checkout(self):
        total = sum(product.price * quantity for product, quantity in self.items.items())
        print("Cart Total: ${:.2f}".format(total))
        return total

    def view_cart(self):
        print("\n--- Cart Items ---")
        for product, quantity in self.items.items():
            print(f"{quantity} x {product.name} - ${product.price:.2f} each")
        print("------------------")