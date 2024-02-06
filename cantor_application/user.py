from flask_login import UserMixin

from cantor_application  import db
from cantor_application.portfolio import Portfolio

class User(db.Model, UserMixin):
    """Class representing a user in the application.

    Args:
        db (SQLAlchemy): The SQLAlchemy database object.
        UserMixin (class): A class providing default implementations for User class.

    Returns:
        User: An instance of the User class.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    amount_of_pln = db.Column(db.Float)
    portfolio = db.relationship('Portfolio', backref='user', lazy='dynamic')
    history = db.relationship('History', backref='user', lazy='dynamic')

    def __repr__(self) -> str:
        return f'User: {self.name}'
    
    def checking_if_can_purchase(self, purchase_value, user):
        
        if purchase_value > user.amount_of_pln:
            return False
        else:
            return True
        
    def purchase(self, purchase_value, user, symbol, currency_name, amount):
        user.amount_of_pln = user.amount_of_pln - purchase_value

        existing_portfolio_record = Portfolio.query.filter_by(user_id=user.id, currency_symbol=symbol).first()
        if existing_portfolio_record:
            existing_portfolio_record.currency_amount += amount
        else:    
            new_portfolio_record = Portfolio(
                currency_symbol = symbol,
                currency_name = currency_name,
                currency_amount = amount,
                user_id = user.id)
            db.session.add(new_portfolio_record)
        db.session.commit()