from Cart import Cart
from User import UserManagementSystem
from Database import Database
import re
import hashlib

# Menus
def main_menu(user_system, cart):
    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register (Customer only)")
        print("3. Exit")
        print("4. Show Available Logins")
        print("5. Item List")
        print("6. Add to Cart")
        print("7. Remove from Cart")
        print("8. View Cart")
        print("9. Calculate Checkout")
        choice = input("Choose an option: ")

        if choice == "1":
            user_details = login(db)  # Perform login and get user details
            if user_details:  # If login is successful
                second_menu(user_system, cart, user_details)
        elif choice == "2":
            register_Customer(user_system)
        elif choice == "4":
            show_available_logins(db)
        elif choice == "5":
            get_all_items()
        elif choice == "6":
            add_items_to_cart()

        elif choice == "7":
            remove_items_from_cart()
        elif choice == "8":
            cart.view_cart()
        elif choice == "9":
            cart.calculate_checkout()

        elif choice == "3":
            print("Exiting program. Goodbye!")
            
            break
            
        else:
            print("Invalid option. Please try again.")


def second_menu(user_system, cart, user_details):
    while True:
        print("\n--- User Menu ---")
        print("1. Show Account Details")
        print("2. Item List")
        print("3. Add to Cart")
        print("4. Remove from Cart")
        print("5. View Cart")
        print("6. Calculate Checkout")
        print("7. Logout and Return to Main Menu")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            print("Account Details:")
            print(f"Account ID: {user_details['account_id']}")
            print(f"Name: {user_details['name']}")
            if user_details["type"] == "employee":
                print("You are logged in as an Employee.")
            elif user_details["type"] == "customer":
                print("You are logged in as a Customer.")

        elif choice == "2":
            db.get_all_items()
        elif choice == "3":
            get_all_items()

        elif choice == "4":
            remove_items_from_cart()
        elif choice == "5":
            cart.view_cart()
        elif choice == "6":
            cart.calculate_checkout()
        elif choice == "7":
            user_system.logout()
            break
        elif choice == "8":
            print("Exiting program. Goodbye!")
            exit()
        else:
            print("Invalid option. Please try again.")



def login(db):
    """
    Handle the login process.
    """
    print("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_details = db.verify_login(username, password)

    if user_details:
        if user_details['type'] == 'customer':
            print(f"Welcome, {user_details['name']}! You are logged in as a Customer.")
            print(f"Email: {user_details['email']}")
            print(f"Status: {user_details['status']}")
        elif user_details['type'] == 'employee':
            print(f"Welcome, {user_details['name']}! You are logged in as an Employee.")
            print(f"Email: {user_details['email']}")
            print(f"Role: {user_details['role']}")
        return user_details  # Return user details to determine access
    else:
        print("Invalid username or password. Please try again.")
        return None
def show_available_logins(db):
    """
    Display available logins for customers and employees.
    """
    print("\n--- Available Logins ---")
    
    # Fetch customers
    customers = db.get_available_logins("Customers")
    if customers:
        print("\n--- Customers ---")
        for customer in customers:
            print(f"Username: {customer['username']}, Password: {customer['password']}")
    else:
        print("\nNo customers found.")
    
    # Fetch employees
    employees = db.get_available_logins("Employees")
    if employees:
        print("\n--- Employees ---")
        for employee in employees:
            print(f"Username: {employee['username']}, Password: {employee['password']}")
    else:
        
        print("\nNo employees found.")

#US1
def register_Customer(user_system):
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            # Validate the password
            validation_error = validate_password(password)
            if validation_error:
                print(f"Error: {validation_error}")
                return
            
            email = input("Enter your email: ")
            gdpr_terms = input("Do you accept the GDPR terms? (yes/no): ").lower() == "yes"
            if not gdpr_terms:
                print("You must accept GDPR terms to register.")
                return

            user_system.register_customer(username, password, email, gdpr_terms)

       

def get_all_items():
        products = db.get_all_products()
        services = db.get_all_services()
        db.add_product(1, 1, 3, 4, 10, "abc", "dbc", 0)
        print("\n--- Item List ---")
        print("\nProducts:")
        if not products:
            print("No products available.")
        else:
            for product in products:
                print(f"{product['item_id']}: {product['name']} - ${product['sales_price']:.2f} - {product['item_type']}")

        print("\nServices:")
        if not services:
            print("No services available.")
        else:
            for service in services:
                print(f"{service['item_id']}: {service['name']} - ${service['sales_price']:.2f} - {service['item_type']}")

#US2
def get_item_by_name(item_name):
    product = db.get_product_by_name(item_name)
    if product:
        print("\n--- Product Found ---")
        print(f"{product['item_id']}: {product['name']} - ${product['sales_price']:.2f} - {product['item_type']}")
        return

    service = db.get_service_by_name(item_name)
    if service:
        print("\n--- Service Found ---")
        print(f"{service['item_id']}: {service['name']} - ${service['sales_price']:.2f} - {service['item_type']}")
        return

    print(f"No product or service found with the name '{item_name}'.")

def add_items_to_cart():
 # Fetch all items to validate the name
        all_items = db.get_all_products() + db.get_all_services()
        all_item_names = [item["name"] for item in all_items]

        item_name = input("Enter the name of the item to add: ")
        if item_name not in all_item_names:
            print(f"Error: '{item_name}' is not a valid item name.")

        quantity = int(input("Enter quantity: "))    
        cart.add_to_cart(item_name, quantity)
 
def remove_items_from_cart():
     # Fetch all items to validate the name
        all_items = db.get_all_products() + db.get_all_services()
        all_item_names = [item["name"] for item in all_items]

        item_name = input("Enter the name of the item to remove: ")
        if item_name not in all_item_names:
            print(f"Error: '{item_name}' is not a valid item name.")

        quantity = int(input("Enter quantity: "))
        cart.remove_from_cart(item_name, quantity)

#US6/7
def print_suppliers_for_best(item_name):
    suppliers= db.get_all_suppliers_for_item(item_name)
    for suppliers in suppliers:
        print(suppliers)

#US9
def get_products_min_stock():
    products_stock=db.get_products_below_min_stock_with_suppliers()
    for product in products_stock:
        print(product)

@staticmethod
def validate_password(password):
    """Validate the password against specified rules."""
    if not (4 <= len(password) <= 16):
        return "Password must be between 4 and 16 characters."
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number."
    if re.search(r"[-_.;]", password):
        return "Password must not contain special characters (-_.;)."
    return None

def set_password(self, password):
    """Validate and hash the password before assigning it to the user."""
    validation_error = self.validate_password(password)
    if validation_error:
        raise ValueError(validation_error)
    self.password = self.hash_password(password)

#US10
def get_aisles_high_disc():
    aisles = db.get_aisles_for_high_discount_products()
    if aisles:
        print("\nAisles with products having high order counts and a discount greater than 20%:")
        for aisle in aisles:
            print(f"Zone_ID: {aisle['Zone_ID']}, Product: {aisle['Product_Name']}, Orders: {aisle['Order_Count']}, Capacity: {aisle['Capacity']}")
    else:
        print("No aisles found with the specified criteria.")



#US11
def get_orders_11():
    specific_date = input("Enter the name of the product or service: ")

    orders = db.get_orders_by_day_and_time(specific_date)
    if orders:
        print(f"\nOrders scheduled for delivery on {specific_date}:")
        for order in orders:
            print(f"Order ID: {order['Order_ID']}, Delivery Address: {order['Delivery_Address']}, Status: {order['Shipping_Status']}")
    else:
        print(f"No orders found for delivery on {specific_date}.")
# Main Program
if __name__ == "__main__":
    user_system = UserManagementSystem()
    cart = Cart()
    db=Database()

    main_menu(user_system, cart)
    # Example usage
    item_name = input("Enter the name of the product or service: ")
    get_item_by_name(item_name)

