from cantor_application  import db

class History(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    currency_symbol = db.Column(db.String(3))
    currency_name = db.Column(db.String(30))
    currency_amount = db.Column(db.Integer)
    currency_price = db.Column(db.Integer)
    date_of_action = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))