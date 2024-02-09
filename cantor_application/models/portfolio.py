"""Module representing the Portfolio class and related functionalities.
This module defines the Portfolio class, which represents a portfolio 
of currencies for a user in the online cantor application. It utilizes 
SQLAlchemy for database operations. The Portfolio class includes attributes 
for the currency symbol, the amount of the currency held, and the user 
ID to which the portfolio belongs.

"""
from cantor_application import db

class Portfolio(db.Model):
    """Class representing a portfolio of currencies for a user.

    Attributes:
        id (int): The unique identifier for the portfolio.
        currency_symbol (str): The symbol of the currency in the portfolio.
        currency_amount (int): The amount of the currency held in the portfolio.
        user_id (int): The ID of the user to whom the portfolio belongs.
    """
    id = db.Column(db.Integer, primary_key=True)
    currency_symbol = db.Column(db.String(3))
    currency_amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        """Returns a string representation of the Portfolio object."""
        return f'Symbol: {self.currency_symbol}, Amount: {self.currency_amount}'
