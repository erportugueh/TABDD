from user import User, Employee, Customer
from Product import Product


class Database:
    def __init__(self):
        self.users = []  # List to store all users (both employees and customers)
        self.products = []  # List to store all products
        self.customer_id_counter = 2000  # Starting customer ID

        # Pre-create employees and customers
        self.create_employee("admin1", "Admin123", "admin1@email.com", 1001)
        self.create_employee("admin2", "Admin123", "admin2@email.com", 1002)
        self.create_employee("admin3", "Admin123", "admin3@email.com", 1003)

        self.create_customer("john_doe", "Password1", "john@email.com")
        self.create_customer("jane_smith", "Password2", "jane@email.com")
        self.create_customer("bob_jones", "Password3", "bob@email.com")
        self.create_customer("alice_brown", "Password4", "alice@email.com")
        self.create_customer("mike_williams", "Password5", "mike@email.com")

        # Pre-create products
        self.add_product("Laptop X1", 1500, {
            "model": "X1 Carbon",
            "year_of_creation": 2023,
            "description": "High-performance laptop for professionals.",
            "specifications": {
                "weight": "1.5kg",
                "dimensions": "14x9x0.7 inches",
                "color": "black"
            }
        })

        self.add_product("Smartphone Pro", 999, {
            "model": "Pro Max",
            "year_of_creation": 2022,
            "description": "Cutting-edge smartphone with excellent camera.",
            "specifications": {
                "weight": "200g",
                "dimensions": "6.5x3x0.3 inches",
                "color": "silver"
            }
        })

    # --- User Management ---
    def add_user(self, user):
        self.users.append(user)

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def create_employee(self, username, password, email, employee_id):
        if self.get_user_by_username(username):
            return "Error: User already exists."

        try:
            employee = Employee(username, password, email, employee_id)
            employee.set_password(password)
            self.add_user(employee)
            return f"Employee {username} created successfully!"
        except ValueError as e:
            return f"Error: {str(e)}"

    def create_customer(self, username, password, email):
        if self.get_user_by_username(username):
            return "Error: User already exists."

        try:
            customer_id = self.customer_id_counter
            self.customer_id_counter += 1
            customer = Customer(username, password, email, customer_id)
            customer.set_password(password)
            self.add_user(customer)
            return f"Customer {username} created successfully with ID {customer_id}!"
        except ValueError as e:
            return f"Error: {str(e)}"

    def login_user(self, username, password):
        user = self.get_user_by_username(username)
        hashed_password = User.hash_password(password)
        if user and user.password == hashed_password:
            return user
        else:
            return None

    # --- Product Management ---
    def add_product(self, name, price, physical_attributes):
        product = Product(name, price, physical_attributes)
        self.products.append(product)

    def display_products(self, user_role):
        for product in self.products:
            product.display_product(user_role)

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None