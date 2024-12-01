import hashlib
import re


class User:
    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    @staticmethod
    def hash_password(password):
        """Hash the password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

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


class Employee(User):
    def __init__(self, username, password, email, employee_id):
        super().__init__(username, password, email, "Employee")
        self.employee_id = employee_id


class Customer(User):
    def __init__(self, username, password, email, customer_id):
        super().__init__(username, password, email, "Customer")
        self.customer_id = customer_id
