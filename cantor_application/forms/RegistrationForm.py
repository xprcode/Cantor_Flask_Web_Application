from wtforms import StringField, PasswordField, EmailField
from flask_wtf import FlaskForm 
from wtforms.validators import DataRequired, ValidationError, Email
from .password_validators.password_validators import PasswordValidator

class RegistrationForm(FlaskForm):

    def my_username_validator(form, field):
        username = field.data
        if len(username) < 6:
            raise ValidationError(('Username must be at least 6 characters long'))
        if not username.isalnum():
            raise ValidationError(('Username may only contain letters and numbers'))
        
    def my_password_validator(form, field):
        
        password_to_check = field.data
        password = PasswordValidator(password_to_check)
        message = password.is_valid()
        
        if message and isinstance(message, str):
            raise ValidationError(message)
        
    name = StringField('Enter you name: ', validators=[DataRequired(), my_username_validator])
    password = PasswordField('Enter password: ', validators=[DataRequired(), my_password_validator])
    re_password = PasswordField('Confirm password: ', validators=[DataRequired()])
    email = EmailField('Enter email: ', validators=[DataRequired(), Email()])

