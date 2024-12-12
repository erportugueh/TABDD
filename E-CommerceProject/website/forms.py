from flask_wtf import FlaskForm
from mongoengine import EmailField
from wtforms import StringField, IntegerField, FloatField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email

class SignUpForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Confirm Password', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(max=50)])  # New
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=15)])  # New
    nif = StringField('NIF', validators=[DataRequired(), Length(max=15)])  # New
    gdpr_terms = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])  # New
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

<<<<<<< Updated upstream
=======
class EmployeeSignUpForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired(), Length(max=15)])
    submit = SubmitField('Sign Up')
>>>>>>> Stashed changes
