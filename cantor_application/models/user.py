"""Module representing the User class and related functionalities.

It defines the User class, which represents a user in the application 
for managing currencies in an online cantor. It utilizes SQLAlchemy for 
database operations. The User class provides methods for checking if 
a user can afford a purchase, if they can sell a certain amount 
of a currency, handling purchases, sales, and adding transaction records 
to the user's transaction history.

"""

from flask_login import UserMixin
import datetime

from cantor_application  import db
from cantor_application.models.portfolio import Portfolio
from cantor_application.models.history import History
from cantor_application.helpers import lookup

class User(db.Model, UserMixin):
    """Class representing a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The username of the user.
        password (str): The password of the user.
        email (str): The email address of the user.
        amount_of_pln (float): The amount of Polish Zloty (PLN) owned by the user.
        portfolio (relationship): Relationship with the Portfolio class indicating 
        the user's portfolio. history (relationship): Relationship with the History 
        class indicating the user's transaction history.

    Methods:
        __repr__: Returns a string representation of the User object.
        checking_if_can_purchase: Checks if the user can afford a purchase.
        checking_if_can_sell: Checks if the user can sell a certain amount of a cryptocurrency.
        sell: Handles the selling of a cryptocurrency by the user.
        purchase: Handles the purchase of a cryptocurrency by the user.
        adding_history_record: Adds a transaction record to the user's transaction history.

    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    amount_of_pln = db.Column(db.Float)
    portfolio = db.relationship('Portfolio', backref='user', lazy='dynamic')
    history = db.relationship('History', backref='user', lazy='dynamic')

    def __repr__(self) -> str:
        """Returns a string representation of the User object."""
        return f'User: {self.name}'

    def checking_if_can_purchase(self, purchase_value: float, user: 'User'):
        """Checks if the user can afford a purchase.

        Args:
            purchase_value (float): The value of the purchase.
            user (User): The user making the purchase.

        Returns:
            bool: True if the user can afford the purchase, False otherwise.
        """
        return purchase_value <= user.amount_of_pln

    def checking_if_can_sell(self, symbol: str, amount: int, user: 'User'):
        """Checks if the user can sell a certain amount of a currency.

        Args:
            symbol (str): The symbol of the currency.
            amount (float): The amount of currency to sell.
            user (User): The user attempting to sell the currency.

        Returns:
            bool: True if the user can sell the specified amount of currency, False otherwise.
        """
        record = Portfolio.query.filter_by(user_id=user.id, currency_symbol=symbol).first()
        return bool(record and record.currency_amount >= amount)

    def sell(self, symbol: str, amount: int, purchase_value: float, user: 'User'):
        """Handles the selling of a currency by the user.

        Args:
            symbol (str): The symbol of the currency to sell.
            amount (int): The amount of currency to sell.
            purchase_value (float): The value of the sale.
            user (User): The user selling the currency.
        """
        user.amount_of_pln = user.amount_of_pln + purchase_value
        record = Portfolio.query.filter_by(user_id=user.id, currency_symbol=symbol).first()

        if record.currency_amount - amount == 0:
            db.session.delete(record)
        else:
            record.currency_amount = record.currency_amount - amount
        is_negative = -1
        user.adding_history_record(symbol, amount, is_negative, user)
        db.session.commit()

    def purchase(self, purchase_value: float, user: 'User', symbol: str, amount: int):
        """Handles the purchase of a currency by the user.

        Args:
            purchase_value (float): The value of the purchase.
            user (User): The user making the purchase.
            symbol (str): The symbol of the currency to purchase.
            amount (int): The amount of currency to purchase.
        """
        user.amount_of_pln = user.amount_of_pln - purchase_value

        existing_portfolio_record = Portfolio.query.filter_by(user_id=user.id,
                                                              currency_symbol=symbol).first()

        if existing_portfolio_record:
            existing_portfolio_record.currency_amount += amount
        else:
            new_portfolio_record = Portfolio(
                currency_symbol = symbol,
                currency_amount = amount,
                user_id = user.id
                )
            db.session.add(new_portfolio_record)
        is_negative = 1
        user.adding_history_record(symbol, amount, is_negative, user)

        db.session.commit()

    def adding_history_record(self, symbol: str, amount: int, is_negative: int, user: 'User'):
        """Adds a transaction record to the user's transaction history.

        Args:
            symbol (str): The symbol of the currency involved in the transaction.
            amount (int): The amount of currency involved in the transaction.
            is_negative (int): Indicator of whether the transaction is negative 
            (sell) or positive (buy).
            user (User): The user involved in the transaction.
        """
        currency_value, currency_name = lookup(symbol)

        date_of_action = datetime.datetime.now().replace(microsecond=0)
        
        new_history_record = History(
                currency_symbol = symbol,
                currency_name = currency_name,
                currency_amount = amount * is_negative,
                currency_price = currency_value,
                date_of_action = date_of_action,
                user_id = user.id)
        
        db.session.add(new_history_record)
        db.session.commit()
