import json


class Product:
    product_id_counter = 1  # Class-level counter for unique IDs

    def __init__(self, name, price, physical_attributes):
        self.name = name
        self.price = price
        self.id = Product.product_id_counter
        Product.product_id_counter += 1
        self.physical_attributes = physical_attributes

    def save_physical_attributes_to_json(self, file_name):
        """Save the physical attributes to a JSON file."""
        try:
            with open(file_name, "w") as json_file:
                json.dump(self.physical_attributes, json_file, indent=4)
            print(f"Physical attributes of '{self.name}' saved to {file_name}.")
        except Exception as e:
            print(f"Error saving attributes to JSON: {e}")

    def load_physical_attributes_from_json(self, file_name):
        """Load the physical attributes from a JSON file."""
        try:
            with open(file_name, "r") as json_file:
                self.physical_attributes = json.load(json_file)
            print(f"Physical attributes loaded from {file_name}.")
        except Exception as e:
            print(f"Error loading attributes from JSON: {e}")

    def display_product(self, user_role):
        """Display product information based on the user's role."""
        print(f"\nProduct Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        if user_role == "Employee":
            print(f"Product ID: {self.id}")
        print(f"Physical Attributes: {self.physical_attributes}")
