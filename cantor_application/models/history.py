"""Module representing the History class and related functionalities.

This module defines the History class, which represents the transaction
history of currency actions for a user in the online cantor application. 
It utilizes SQLAlchemy for database operations. The History class includes 
attributes for the currency symbol, currency name, amount, price, date 
of action, and the user ID associated with the transaction.

"""
from cantor_application  import db

class History(db.Model):
    """Class representing the transaction history of currency actions for a user.

    Attributes:
        id (int): The unique identifier for the history entry.
        currency_symbol (str): The symbol of the currency involved in the transaction.
        currency_name (str): The name of the currency involved in the transaction.
        currency_amount (int): The amount of currency involved in the transaction.
        currency_price (int): The price of the currency at the time of the transaction.
        date_of_action (DateTime): The date and time of the transaction.
        user_id (int): The ID of the user associated with the transaction.

    """
    id = db.Column(db.Integer, primary_key=True)
    currency_symbol = db.Column(db.String(3))
    currency_name = db.Column(db.String(30))
    currency_amount = db.Column(db.Integer)
    currency_price = db.Column(db.Integer)
    date_of_action = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

   