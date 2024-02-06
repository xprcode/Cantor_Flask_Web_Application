from flask_wtf import FlaskForm 
from wtforms import StringField,  BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name = StringField('Enter you name: ', validators=[DataRequired()])
    password = PasswordField('Enter password: ', validators=[DataRequired()])
    remember = BooleanField('Rememeber me')