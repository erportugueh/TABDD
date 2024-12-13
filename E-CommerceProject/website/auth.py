from flask import Blueprint, render_template, flash, redirect  # Import necessary Flask components
from .forms import LoginForm, SignUpForm, EmployeeSignUpForm  # Import custom forms
from .models import Customer, Employee  # Import Customer and Employee models
from datetime import datetime  # Import datetime for timestamping
from . import db  # Import the database instance
from flask_login import login_user, login_required, logout_user  # Import Flask-Login functions

# Define the 'auth' blueprint
auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()  # Instantiate the signup form

    if form.validate_on_submit():  # Check if form submission is valid
        # Retrieve form data
        username = form.username.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data
        address = form.address.data
        postal_code = form.postal_code.data
        nif = form.nif.data
        gdpr_terms = form.gdpr_terms.data

        # Ensure passwords match
        if password1 == password2:
            # Fetch the latest customer ID and calculate the next ID
            latest_customer = db.session.query(Customer).order_by(Customer.customer_id.desc()).first()
            next_customer_id = (latest_customer.customer_id + 1) if latest_customer else 1

            # Generate a unique account ID using username and NIF
            name_part = username[:3].upper() if len(username) >= 3 else username.upper()
            nif_part = nif[:3] if len(nif) >= 3 else nif
            account_id = f"{next_customer_id}{name_part}{nif_part}"

            # Create a new Customer object
            new_customer = Customer(
                email=email,
                name=username,
                address=address,
                postal_code=postal_code,
                nif=nif,
                account_id=account_id,
                gdpr_terms=gdpr_terms,
                status='new',  # Default status for new customers
                accepted_date=datetime.utcnow()  # Set accepted date to current timestamp
            )
            new_customer.password = password1  # Set the customer's password

            try:
                # Add and commit the new customer to the database
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully, You can now Login', 'success')
                return redirect('/login')  # Redirect to login page
            except Exception as e:
                print(e)  # Print error to console for debugging
                flash('Account Not Created! Error', 'danger')  # Display error message to user

            # Clear form fields after failure
            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
            form.address.data = ''
            form.postal_code.data = ''
            form.nif.data = ''
            form.gdpr_terms.data = ''
        else:
            flash('Passwords do not match!', 'danger')  # Notify user of password mismatch
    else:
        # Debugging: Print validation errors
        print("Form validation failed.")
        print("Errors:", form.errors)

    return render_template('signup.html', form=form)  # Render signup template with form

@auth.route('/employee-sign-up', methods=['GET', 'POST'])
def employee_sign_up():
    form = EmployeeSignUpForm()  # Instantiate the employee signup form

    if form.validate_on_submit():  # Check if form submission is valid
        # Retrieve form data
        username = form.username.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data
        role = form.role.data  # Retrieve the role input

        # Ensure passwords match
        if password1 == password2:
            # Fetch the latest employee ID and calculate the next ID
            latest_employee = db.session.query(Employee).order_by(Employee.employee_id.desc()).first()
            next_employee_id = (latest_employee.employee_id + 1) if latest_employee else 1

            # Generate a unique account ID for the employee
            name_part = username[:3].upper() if len(username) >= 3 else username.upper()
            account_id = f"EMP{next_employee_id:03d}{name_part}"

            # Create a new Employee object
            new_employee = Employee(
                email=email,
                name=username,
                account_id=account_id,
                role=role,  # Assign the role to the employee
            )
            new_employee.password = password1  # Set the employee's password

            try:
                # Add and commit the new employee to the database
                db.session.add(new_employee)
                db.session.commit()
                flash('Employee Account Created Successfully, You can now Login', 'success')
                return redirect('/login')  # Redirect to login page
            except Exception as e:
                print(e)  # Print error to console for debugging
                flash('Employee Account Not Created! Error', 'danger')  # Display error message to user

            # Clear form fields after failure
            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
            form.role.data = ''
        else:
            flash('Passwords do not match!', 'danger')  # Notify user of password mismatch
    else:
        # Debugging: Print validation errors
        print("Form validation failed.")
        print("Errors:", form.errors)

    return render_template('signup_employee.html', form=form)  # Render employee signup template with form

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instantiate the login form

    if form.validate_on_submit():  # Check if form submission is valid
        email = form.email.data  # Retrieve email input
        password = form.password.data  # Retrieve password input

        # Check if the email belongs to a customer
        customer = Customer.query.filter_by(email=email).first()
        if customer:
            if customer.verify_password(password=password):  # Verify customer password
                login_user(customer)  # Log in the customer
                return redirect('/')  # Redirect to homepage
            else:
                flash('Incorrect Email or Password')  # Notify user of incorrect credentials
        else:
            # Check if the email belongs to an employee
            employee = Employee.query.filter_by(email=email).first()
            if employee:
                if employee.verify_password(password=password):  # Verify employee password
                    login_user(employee)  # Log in the employee
                    return redirect('/')  # Redirect to homepage
                else:
                    flash('Incorrect Email or Password')  # Notify user of incorrect credentials
            else:
                flash('Account does not exist. Please Sign Up')  # Notify user of non-existent account
    else:
        # Debugging: Print validation errors
        print("Form validation failed.")
        print("Errors:", form.errors)

    return render_template('login.html', form=form)  # Render login template with form

@auth.route('/logout', methods=['GET', 'POST'])
@login_required  # Ensure user is logged in before accessing this route
def log_out():
    logout_user()  # Log out the current user
    return redirect('/')  # Redirect to homepage