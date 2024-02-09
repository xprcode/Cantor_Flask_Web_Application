"""Module representing the BuyForm class for the Flask application.

This module defines the BuyForm class, which is a FlaskForm used 
for handling the purchase form on the online cantor website. 
It includes fields for the currency symbol and the amount of currency 
to purchase. Additionally, it provides a custom validator to check the 
validity of the currency symbol using the `lookup` function from the `helpers` module.

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from cantor_application.helpers import lookup

class BuyForm(FlaskForm):
    """Class representing the purchase form on the online cantor website.

    Attributes:
        currency (StringField): Field for entering the currency symbol.
        amount (IntegerField): Field for entering the amount of currency to purchase.

    Methods:
        symbol_validator: Custom validator to check the validity of the currency symbol.
    """

    def symbol_validator(form, field):
        """Custom validator to check the validity of the currency symbol.

        Args:
            form: The form being validated.
            field: The field containing the currency symbol.

        Raises:
            ValidationError: If the currency symbol is invalid.
        """
        symbol = field.data
        validator1, _ = lookup(symbol)
        if validator1 is None:
            raise ValidationError(
                'Wrong currency index - transaction canceled.\
                Please check Standard ISO 4217 currency list')

    currency = StringField('Currency: ', validators=[DataRequired(), symbol_validator])
    amount = IntegerField('Amount: ', validators=[DataRequired(), NumberRange(min=0, max=None)])
