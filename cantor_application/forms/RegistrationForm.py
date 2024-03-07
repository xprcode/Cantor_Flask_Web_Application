"""Module representing the RegistrationForm class for the Flask application.

This module defines the RegistrationForm class, which is a FlaskForm used for 
handling user registration on the online cantor website. It includes fields 
for entering the user's name, password, confirming the password, and email. 
Additionally, it provides custom validators for username and password fields.

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, ValidationError, Email
from .password_validators.password_validators import PasswordValidator

class RegistrationForm(FlaskForm):
    """Class representing the user registration form on the online cantor website.

    Attributes:
        name (StringField): Field for entering the user's name.
        password (PasswordField): Field for entering the user's password.
        re_password (PasswordField): Field for confirming the user's password.
        email (EmailField): Field for entering the user's email address.

    Methods:
        my_username_validator: Custom validator for the username field.
        my_password_validator: Custom validator for the password field.
    """
    def my_username_validator(form, field):
        """Custom validator for the username field.

        Args:
            form: The form being validated.
            field: The field containing the username.

        Raises:
            ValidationError: If the username is not valid.
        """
        username = field.data
        if len(username) < 6:
            raise ValidationError(('Username must be at least 6 characters long'))
        if not username.isalnum():
            raise ValidationError(('Username may only contain letters and numbers'))

    def my_password_validator(form, field):
        """Custom validator for the password field.

        Args:
            form: The form being validated.
            field: The field containing the password.

        Raises:
            ValidationError: If the password is not valid.
        """
        password_to_check = field.data
        password = PasswordValidator(password_to_check)
        if password.is_valid():
            raise ValidationError((password.is_valid()))
        

    name = StringField('Enter you name: ', validators=[DataRequired(), my_username_validator])
    password = PasswordField('Enter password: ', validators=[DataRequired(), my_password_validator])
    re_password = PasswordField('Confirm password: ', validators=[DataRequired()])
    email = EmailField('Enter email: ', validators=[DataRequired(), Email()])
    
