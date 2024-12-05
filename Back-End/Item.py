import json
from datetime import date


# Superclass Item
class Item:
    def __init__(self, item_id, name, description, brand, item_type, primary_supplier_id, purchase_price, sales_price):
        self.item_id = item_id  # PK
        self.name = name
        self.description = description
        self.brand = brand
        self.item_type = item_type
        self.primary_supplier_id = primary_supplier_id  # FK
        self.purchase_price = purchase_price
        self.sales_price = sales_price

    def __str__(self):
        return f"Item({self.item_id}): {self.name}, Type: {self.item_type}, Price: ${self.sales_price:.2f}"


# Subclass Product
class Product(Item):
    def __init__(self, item_id, name, description, brand, item_type, primary_supplier_id, purchase_price, sales_price,
                 warehouse_id, zone_id, quantity_in_stock, minimum_stock, price, category, subcategory,
                 technical_information_file, physical_attributes, start_date, end_date, is_current):
        super().__init__(item_id, name, description, brand, item_type, primary_supplier_id, purchase_price, sales_price)
        self.warehouse_id = warehouse_id  # FK
        self.zone_id = zone_id
        self.quantity_in_stock = quantity_in_stock
        self.minimum_stock = minimum_stock
        self.price = price
        self.category = category
        self.subcategory = subcategory
        self.technical_information = self._load_technical_info(technical_information_file)  # Load JSON
        self.physical_attributes = physical_attributes
        self.start_date = start_date
        self.end_date = end_date
        self.is_current = is_current

    def _load_technical_info(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)  # Parse the JSON file
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: File {file_path} contains invalid JSON.")
            return {}

    def __str__(self):
        return (f"Product({self.item_id}): {self.name}, Category: {self.category}, Subcategory: {self.subcategory}, "
                f"Stock: {self.quantity_in_stock}, Price: ${self.price:.2f}, Technical Info: {self.technical_information}, "
                f"Current: {self.is_current}")


# Subclass Service
class Service(Item):
    def __init__(self, item_id, name, description, brand, item_type, primary_supplier_id, purchase_price, sales_price,
                 service_id, max_execution_hours, execution_time, responsible_employee_id, price, start_date, end_date,
                 is_valid):
        super().__init__(item_id, name, description, brand, item_type, primary_supplier_id, purchase_price, sales_price)
        self.service_id = service_id  # FK
        self.max_execution_hours = max_execution_hours
        self.execution_time = execution_time
        self.responsible_employee_id = responsible_employee_id  # FK
        self.price = price
        self.start_date = start_date
        self.end_date = end_date
        self.is_valid = is_valid

    def __str__(self):
        return (f"Service({self.item_id}): {self.name}, Execution Time: {self.execution_time} hours, "
                f"Price: ${self.price:.2f}, Valid: {self.is_valid}")