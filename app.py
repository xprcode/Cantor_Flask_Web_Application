from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, url_for, redirect, flash, session
from sqlalchemy import func
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
)

from cantor_application.helpers import lookup
from cantor_application.forms.registrationform import RegistrationForm
from cantor_application.forms.buyform import BuyForm
from cantor_application.forms.loginform import LoginForm
from cantor_application.forms.sellform import SellForm
from cantor_application import app, db
from cantor_application.models.history import History
from cantor_application.models.user import User
from cantor_application.models.portfolio import Portfolio

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    """Load a user by their user ID.

    Returns:
    User or None: The User object if found, otherwise None.
    """
    return User.query.filter(User.id == id).first()


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
    """
    This route logs out the current user by using the `logout_user()` function
    provided by Flask-Login. 

    Returns:
    redirect: Redirects the user to the login page ('login' endpoint).
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    """
    This route renders the index.html template.

    Returns:
    str: Rendered HTML content of the index page.
    """
    return render_template('index.html')

@app.route('/buy', methods = ['GET', 'POST'])
@login_required
def buy():
    """
    This route allows authenticated users to buy currency. It validates the form input,
    checks if the user has sufficient funds, and processes the purchase if conditions are met.
    
    Methods:
    GET: Displays the buy form.
    POST: Handles the purchase request.

    Returns:
    GET: Renders the 'buy.html' template with the buy form.
    POST: Redirects to the homepage ('index.html') after processing the purchase.

    Form Parameters (POST):
    - currency: The currency code to buy.
    - amount: The amount of currency to buy.
    """

    form = BuyForm()

    user = load_user(session.get('user_id'))

    if form.validate_on_submit():
        #NBP API
        currency_value, currency_name = lookup(form.currency.data)
        purchase_value = form.amount.data * currency_value

        # Chacking if user can aford for the purcahse.
        if user.checking_if_can_purchase(purchase_value, user):
            user.purchase(
                purchase_value,
                user,
                form.currency.data.lower(),
                form.amount.data
                )
            flash(f"You have successfully bought amount: {form.amount.data} of: {currency_name}")
            return render_template('index.html', form=form)

        flash("Insufficient funds in the account - transaction canceled")

    return render_template('buy.html', form=form)


@app.route('/sell', methods = ['GET', 'POST'])
@login_required
def sell():
    """
    This route allows authenticated users to sell the currencies from their portfolio. 
    It validates the form input, checks if the user has sufficient amount of currency in portfolio,
    and processes the sale if conditions are met.
    
    Methods:
    GET: Displays the sell form.
    POST: Handles the sell request.

    Returns:
    GET: Renders the 'sell.html' template with the sell form.
    POST: Redirects to the homepage ('index.html') after processing the sale.

    Form Parameters (POST):
    - currency: The currency code to sell.
    - amount: The amount of currency to sell.
    """
    form = SellForm()

    user = load_user(session.get('user_id'))

    if form.validate_on_submit():

        if user.checking_if_can_sell(form.currency.data.lower(), form.amount.data, user):

            #NBP API
            currency_value, currency_name = lookup(form.currency.data)
            purchase_value = form.amount.data * currency_value
            user.sell(form.currency.data.lower(), form.amount.data, purchase_value, user)
            flash(f"You have successfully sold amount: {form.amount.data} of: {currency_name}")
            return render_template('index.html', form=form)

        flash("No sufficient amount of currency on your account.")

    return render_template('sell.html', form=form)


@app.route('/history', methods = ['GET'])
@login_required
def history():
    """
    This route retrieves all transaction history records associated with the logged-in user
    and renders the 'history.html' template, passing the retrieved history records to the template.

    Returns:
    str: Rendered HTML content of the 'history.html' template, displaying the transaction history.
    """
    user = load_user(session.get('user_id'))
    total_history = History.query.filter_by(user_id=user.id).all()

    return render_template('history.html', history=total_history)


if __name__ == '__main__':
    app.run()
