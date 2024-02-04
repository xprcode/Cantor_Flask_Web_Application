from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class BuyForm(FlaskForm):
    currency = StringField('Currency test ', validators=[DataRequired()])
    amount = IntegerField('Amount: ', validators=[DataRequired(), NumberRange(min=0, max=None)])
