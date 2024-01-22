from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from modules import LoginForm, RegistrationForm, BuyForm
from helpers import lookup
from datetime import date


app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'




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

    def get_user_info(self):
        """Retrieves user information from the database and updates the instance."""

        user = User.query.filter_by(name=self.name).first()

        if user:
            self.name = user.name
        else:
            self.name = ""

class Portfolio(db.Model): 
   id = db.Column(db.Integer, primary_key=True) 
   currency_symbol = db.Column(db.String(3))
   currency_name = db.Column(db.String(30))
   currency_amount = db.Column(db.Integer)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class History(db.Model): 
   id = db.Column(db.Integer, primary_key=True) 
   currency_symbol = db.Column(db.String(3))
   currency_name = db.Column(db.String(30))
   currency_amount = db.Column(db.Integer)
   currency_price = db.Column(db.Integer)
   date_of_action = db.Column(db.DateTime)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route('/init')
def init():
    """initialazing data base.

    Returns:
    str, database: this function is initialaizing
    cantor.db database
    """
    app.app_context().push()
    db.create_all()

    return '<h1>Initial configuration done!</h1>'


@login_manager.user_loader
def load_user(id):
    """Load a user by their user ID.

    Args:
    id (int): The user ID.

    Returns:
    User or None: The User object if found, otherwise None.
    """
    return User.query.filter(User.id == id).first()


def is_safe_url(target):
    """Check if the target URL is safe to redirect to.

    Args:
    target (str): The target URL.

    Returns:
    bool: True if the URL is safe, False otherwise.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/login', methods = ['Get', 'POST'])
def login():
    """Handle user login.

    Returns:
    str or render_template: If the form is submitted and the user is successfully logged in,
    it redirects to 'index.html'. Otherwise, it renders 'login.html' with the login form.
    """
    # add invalid user name or password
    form = LoginForm()
    if form.validate_on_submit():
        # Query database for username
        user = User.query.filter(User.name == form.name.data).first()
        # Ensure username exists and password is correct
        if user is not None and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            login_user(user)
            flash(f'Hi {user.name}, nice to see you!')
            return render_template('index.html')
    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registering user and adding to database.

    Returns:
    str or render_template: If the form is submitted and the user is successfully registered,
    it redirects to 'login.html'. Otherwise, it renders 'register.html' with the register form.

    """

    form = RegistrationForm()

    if form.validate_on_submit():
        if (
            db.session.query(User.name)
            .filter(func.lower(User.name) == func.lower(form.name.data))
            .first()
            is not None
        ):
            flash(f"User name '{form.name.data}' already exists.")
            return render_template("register.html", form=form)

        if (
            db.session.query(User.email)
            .filter(func.lower(User.email) == func.lower(form.email.data))
            .first()
            is not None
        ):
            flash(f"Email '{form.email.data}' already exists.")
            return render_template("register.html", form=form)

        if not form.password.data == form.re_password.data:
            flash("Ensure you provide correct pasword twice")
            return render_template("register.html", form=form)

        new_user = User(
            name=form.name.data,
            password=generate_password_hash(form.password.data),
            email=form.email.data,
            # give the user 10000 pln. 
            amount_of_pln = 10000
            
        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            f"Hello '{form.name.data}'! You have been registered sucesfully! Please log in."
        )

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy', methods = ['GET', 'POST'])
@login_required
def buy():
    
    form = BuyForm()
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        #NBP API
        currency_value, currency_name = lookup(form.currency.data)
        
        if currency_value: 
            purchase_value = form.amount.data * currency_value
            if purchase_value > user.amount_of_pln:
                flash("Insufficient funds in the account - transaction canceled")
                return render_template('buy.html', form=form)
            else:

                user.amount_of_pln = user.amount_of_pln - purchase_value
                new_portfolio_record = Portfolio(
                    currency_symbol = form.currency.data,
                    currency_name = currency_name,
                    currency_amount = form.amount.data,
                    user_id = user.id)
                
                db.session.add(new_portfolio_record)

                db.session.commit()
                return 'purchase ok, new record in DB'
        else:
            flash("Wrong currency index - transaction canceled. Please check Standard ISO 4217 currency list")
            return render_template('buy.html', form=form)
    return render_template('buy.html', form=form)

@app.route('/history')
def history():
    return redirect(url_for('not_implemented', message="Function history is not ready yet")) 

@app.route('/quote')
def quote():
    return redirect(url_for('not_implemented', message="Function quote is not ready yet")) 

@app.route('/sell')
@login_required
def sell():
    return redirect(url_for('not_implemented', message="Function sell is not ready yet")) 

@app.route('/not_implemented/<message>') 
def not_implemented(message): 
 return '<h1 style="color:red">{}</h1>'.format(message) 

if __name__ == '__main__':
    app.run()
