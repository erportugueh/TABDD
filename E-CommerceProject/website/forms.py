from flask_wtf import FlaskForm  # Import Flask-WTF for form handling
from mongoengine import EmailField  # Import EmailField from MongoEngine (although not used in this code)
from wtforms import StringField, IntegerField, FloatField, PasswordField, BooleanField, SubmitField  # Import form fields
from wtforms.validators import DataRequired, Length, NumberRange, Email  # Import validators for form fields

# Form for user sign-up
class SignUpForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(max=50)])  # Username field with validation
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email field with validation
    password1 = PasswordField('Password', validators=[DataRequired()])  # Password field
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])  # Confirmation password field
    address = StringField('Address', validators=[DataRequired(), Length(max=50)])  # Address field
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=15)])  # Postal code field
    nif = StringField('NIF', validators=[DataRequired(), Length(max=15)])  # NIF (tax ID) field
    gdpr_terms = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])  # GDPR terms checkbox
    submit = SubmitField('Sign Up')  # Submit button

# Form for user login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])  # Email field for login
    password = PasswordField('Enter Your Password', validators=[DataRequired()])  # Password field for login
    submit = SubmitField('Log in')  # Submit button

# Form for employee sign-up
class EmployeeSignUpForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(max=50)])  # Username field
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email field with validation
    password1 = PasswordField('Password', validators=[DataRequired()])  # Password field
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])  # Confirmation password field
    role = StringField('Role', validators=[DataRequired(), Length(max=25)])  # Role field with validation
    submit = SubmitField('Sign Up')  # Submit button
