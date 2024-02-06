from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from cantor_application.helpers import lookup

class BuyForm(FlaskForm):
    
    def symbol_validator(form, field):
        symbol = field.data
        validator1, _ = lookup(symbol)
        if validator1 is None:
            raise ValidationError('Wrong currency index - transaction canceled. Please check Standard ISO 4217 currency list')

    currency = StringField('Currency: ', validators=[DataRequired(), symbol_validator])
    amount = IntegerField('Amount: ', validators=[DataRequired(), NumberRange(min=0, max=None)])
