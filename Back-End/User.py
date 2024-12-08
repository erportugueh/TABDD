from datetime import datetime
import hashlib
from Database import Database

db=Database()

# Superclass: User
class User:
    def __init__(self, username, password, email, accountID):
        self.username = username
        self.password = password
        self.email = email
        self.accountID = accountID

    def __str__(self):
        return f"User({self.username}, Email: {self.email}, AccountID: {self.accountID})"


# Subclass: Employee
class Employee(User):
    def __init__(self, username, password, email, accountID, employee_id, role):
        super().__init__(username, password, email, accountID)
        self.employee_id = employee_id
        self.role = role

    def __str__(self):
        return f"Employee({self.username}, Role: {self.role}, Employee ID: {self.employee_id})"


# Subclass: Customer
class Customer(User):
    def __init__(self, username, password, email, accountID, customer_id, address, postal_code, nif,
                 gdpr_terms, accepted_date, points_balance, last_point_redeemed_date, status):
        super().__init__(username, password, email, accountID)
        self.customer_id = customer_id
        self.address = address
        self.postal_code = postal_code
        self.nif = nif
        self.gdpr_terms = gdpr_terms
        self.accepted_date = accepted_date
        self.points_balance = points_balance
        self.last_point_redeemed_date = last_point_redeemed_date
        self.status = status

    def __str__(self):
        return (f"Customer({self.username}, NIF: {self.nif}, Address: {self.address}, "
                f"Postal Code: {self.postal_code}, Points Balance: {self.points_balance}, "
                f"Status: {self.status})")
    
    
    
    
    
    
    def __init__(self):
        self.users = []  # List to store User objects

  

    def register_customer(self, username, password, email, accountID, customer_id, address, postal_code, nif,
                          gdpr_terms, accepted_date, points_balance, last_point_redeemed_date, status):
        customer = Customer(username, password, email, accountID, customer_id, address, postal_code, nif,
                            gdpr_terms, accepted_date, points_balance, last_point_redeemed_date, status)
        self.users.append(customer)
        print(f"Customer '{username}' registered successfully.")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                print(f"Login successful! Welcome, {username}.")
                return user
        print("Invalid username or password.")
        return None

    def display_users(self):
        print("Registered Users:")
        for user in self.users:
            print(user)



# User Management System
class UserManagementSystem:
    def __init__(self):
        self.users = []
        self.current_user = None

    def register_customer(self, username, password, email, gdpr_terms):
      

        accountID = len(self.users) + 1  # or use a better mechanism like fetching next ID from the DB
        password_hash = self.hash_password(password)
        current_dateTime = datetime.now()
        customer_data = {
            "name": username,
            "address": "abc",
            "postal_code": "0000-000",
            "nif": "124124",
            "email": email,
            "account_id": 1234,
            "password_hash": password_hash,
            "gdpr_terms": gdpr_terms,
            "accepted_date": "12-DEC-24",
            "points_balance": 0,
            "status": "new"
         }
        db.save_customer_to_db(customer_data)
        print(f"Customer '{username}' registered successfully.")

    @staticmethod
    def hash_password(password):
        """Hash the password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

   

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"Login successful! Welcome, {username}.")
                return True
        print("Invalid username or password.")
        return False

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")

    def show_account_details(self):
        if isinstance(self.current_user, Employee):
            print(f"Username: {self.current_user.username}, Email: {self.current_user.email}, "
                  f"Employee ID: {self.current_user.employee_id}")
        elif isinstance(self.current_user, Customer):
            print(f"Username: {self.current_user.username}, Email: {self.current_user.email}, "
                  f"Status: {self.current_user.status}")

    def display_users(self):
        for user in self.users:
            print(user)
