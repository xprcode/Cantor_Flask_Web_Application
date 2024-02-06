from cantor_application  import db
from flask_login import UserMixin

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