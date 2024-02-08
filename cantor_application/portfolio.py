from cantor_application import db

class Portfolio(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    currency_symbol = db.Column(db.String(3))
    currency_name = db.Column(db.String(30))
    currency_amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Symbol: {self.currency_symbol}, Amount: {self.currency_amount}'
