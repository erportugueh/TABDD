from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm
from .models import Customer, Employee
from datetime import datetime
from . import db
from flask_login import login_user, login_required, logout_user
from flask_login import current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods= ['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
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
            # Query the latest Customer_ID and increment by 1
            latest_customer = db.session.query(Customer).order_by(Customer.customer_id.desc()).first()
            next_customer_id = (latest_customer.customer_id + 1) if latest_customer else 1

            # Generate ACCOUNT_ID
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
                status='new',  # Default status
                accepted_date=datetime.utcnow()  # Default to current date
            )
            # Set password hash
            new_customer.password = password1

            try:
                # Add and commit the new customer
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully, You can now Login', 'success')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created! Error', 'danger')

            # Reset the form fields
            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
            form.address.data = ''
            form.postal_code.data = ''
            form.nif.data = ''
            form.gdpr_terms.data = ''
        else:
            flash('Passwords do not match!', 'danger')
    else:
        # Debugging: Print validation errors to the console
        print("Form validation failed.")
        print("Errors:", form.errors)

    return render_template('signup.html', form=form)

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()
        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Incorrect Email or Password')
        else:
            employee = Employee.query.filter_by(email=email).first()
            if employee:
                if employee.password == password:
                    login_user(employee)
                    return redirect('/')
                else:
                    flash('Incorrect Email or Password')
            else:
                flash('Account does not exist please Sign Up')
    else:
        # Debugging: Print validation errors to the console
        print("Form validation failed.")
        print("Errors:", form.errors)

    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')

