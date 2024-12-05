from Cart import Cart
from User import UserManagementSystem
from Database import Database
import re

def login(db):
    """
    Handle the login process.
    """
    print("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Verify credentials with the database
    user_details = db.verify_login(username, password)

    if user_details:
        print(f"Welcome {user_details['name']}!")
        return user_details  # Return user details to determine access
    else:
        print("Invalid username or password. Please try again.")
        return None
    
# Menus
def main_menu(user_system, cart):
    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register (Customer only)")
        print("3. Exit")
        print("4. Show Available Logins")
        choice = input("Choose an option: ")

        if choice == "1":
            user_details = login(db)  # Perform login and get user details
            if user_details:  # If login is successful
                second_menu(user_system, cart, user_details)
        elif choice == "2":
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

        elif choice == "3":
            print("Exiting program. Goodbye!")
            
            break
        elif choice == "4":
            show_available_logins(db)
            
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
            get_all_items()
        elif choice == "3":
            add_items_to_cart()

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

def get_all_items():
        products = db.get_all_products()
        services = db.get_all_services()

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
 
# Main Program
if __name__ == "__main__":
    user_system = UserManagementSystem()
    cart = Cart()
    db=Database()

    main_menu(user_system, cart)