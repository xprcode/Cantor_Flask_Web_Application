"""Module representing the LoginForm class for the Flask application.

This module defines the LoginForm class, which is a FlaskForm used for 
handling user login form on the online cantor website. It includes 
fields for entering the user's name, password, and a checkbox for 
remembering the user's session.

"""
from flask_wtf import FlaskForm
from wtforms import StringField,  BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Class representing the user login form on the online cantor website.

    Attributes:
        name (StringField): Field for entering the user's name.
        password (PasswordField): Field for entering the user's password.
        remember (BooleanField): Checkbox for remembering the user's session.

    """
    name = StringField('Enter you name: ', validators=[DataRequired()])
    password = PasswordField('Enter password: ', validators=[DataRequired()])
    remember = BooleanField('Rememeber me')
    