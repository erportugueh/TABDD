# main.py
from Cart import Cart
from DataBase import Database
def display_menu():
    """Display the main menu."""
    print("\n--- Main Menu ---")
    print("1. Login")
    print("2. Register as Customer")
    print("3. Exit")

def display_user_menu(user):
    """Display the menu for logged-in users."""
    print(f"\n--- Welcome {user.username} ({user.role}) ---")
    print("1. Print My Details")
    print("2. Show Products")
    print("3. Add Product to Cart")
    print("4. Remove porduct from Cart")
    print("5. View Cart")
    print("6. Checkout")
    print("7. Logout and Return to Main Menu")
    print("8. Exit")

def handle_login(db):
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = db.login_user(username, password)  # Attempt to log in
    if user:
        print(f"Login successful! Welcome {user.username}.")
        user_menu(db, user)  # Pass the logged-in user to the user menu
    else:
        print("Invalid credentials.")

def handle_register(db):
    """Handle customer registration logic (only customers can register)."""
    print("\n--- Register ---")
    
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    
    print(db.create_customer(username, password, email))

def user_menu(db, user):
    """Display the user menu where logged-in users can interact with their profile."""
    cart=Cart()
    while True:
        display_user_menu(user)
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print(f"\n--- My Details ---")
            print(f"Username: {user.username}")
            print(f"Role: {user.role}")
            print(f"Email: {user.email}")
            if user.role == "Employee":
                print(f"Employee ID: {user.employee_id}")
                
            print(f"\n--- End of Details ---")
        elif choice == "2":
            print("\n--- Product List ---")
            db.display_products(user.role)

        elif choice == "3":
            try:
                product_id = int(input("Enter Product ID to add: "))
                quantity = int(input("Enter quantity: "))
                product = db.get_product_by_id(product_id)
                if product:
                    cart.add_to_cart(product, quantity)
                else:
                    print("Invalid Product ID.")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        elif choice == "4":
            try:
                product_id = int(input("Enter Product ID to remove: "))
                quantity = int(input("Enter quantity: "))
                product = db.get_product_by_id(product_id)
                if product:
                    cart.remove_from_cart(product, quantity)
                else:
                    print("Invalid Product ID.")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        elif choice == "5":
            cart.view_cart()
        elif choice == "6":
            cart.calculate_checkout()
        
        
        elif choice == "7":
            print("Logging out and returning to the main menu.")
            break  # Exit the user menu and return to the main menu
        
        elif choice == "8":
            print("Exiting the system.")
            exit()  # Exit the entire program
        
        else:
            print("Invalid choice. Please try again.")


def main():
    db = Database()

    while True:
        display_menu()

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            handle_login(db)
        elif choice == "2":
            handle_register(db)  # This will only allow customer registration
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
