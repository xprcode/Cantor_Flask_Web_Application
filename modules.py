from flask import redirect, render_template, session
from wtforms import StringField, IntegerField, BooleanField, SelectField, RadioField, DateField, PasswordField, EmailField
from flask_wtf import FlaskForm 
from wtforms.validators import DataRequired, ValidationError, Email, NumberRange



class LoginForm(FlaskForm):
    name = StringField('Enter you name: ', validators=[DataRequired()])
    password = PasswordField('Enter password: ', validators=[DataRequired()])
    remember = BooleanField('Rememeber me')
    

class RegistrationForm(FlaskForm):

    def my_username_validator(form, field):
        username = field.data
        if len(username) < 6:
            raise ValidationError(('Username must be at least 6 characters long'))
        if not username.isalnum():
            raise ValidationError(('Username may only contain letters and numbers'))
        
    def my_password_validator(form, field):
        password = field.data
        if len(password) < 8:
            raise ValidationError('Password must have at least 8 characters including 1 capital letter, 1 special sign and 1 digit')
        
        digit = sum(1 for char in password if char.isdigit())
        capital = sum(1 for char in password if char.isupper())
        special = sum(1 for char in password if char.isascii() and not char.isalnum())

        if digit < 1 or capital < 1 or special < 1:
            raise ValidationError('Password must have at least 8 characters including 1 capital letter, 1 special sign, and 1 digit')
        
    name = StringField('Enter you name: ', validators=[DataRequired(), my_username_validator])
    password = PasswordField('Enter password: ', validators=[DataRequired(), my_password_validator])
    re_password = PasswordField('Confirm password: ', validators=[DataRequired()])
    email = EmailField('Enter email: ', validators=[DataRequired(), Email()])

class BuyForm(FlaskForm):
    currency = StringField('Currency test ', validators=[DataRequired()])
    amount = IntegerField('Amount: ', validators=[DataRequired(), NumberRange(min=0, max=None)])


    

