"""Module representing the SellForm class for the Flask application.

This module defines the SellForm class, which is a FlaskForm used for handling
 the sell form on the online cantor website. It includes fields for entering 
 the currency and the amount of currency to sell.

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class SellForm(FlaskForm):
    """Class representing the sell form on the online cantor website.

    Attributes:
        currency (StringField): Field for entering the currency symbol.
        amount (IntegerField): Field for entering the amount of currency to sell.

    """
    currency = StringField('Currency: ', validators=[DataRequired()])
    amount = IntegerField('Amount: ', validators=[DataRequired(), NumberRange(min=0, max=None)])
