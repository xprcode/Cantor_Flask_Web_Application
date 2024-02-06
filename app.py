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
from cantor_application.forms.RegistrationForm import RegistrationForm
from cantor_application.forms.BuyForm import BuyForm
from cantor_application.forms.LoginForm import LoginForm
from cantor_application import app, db
from cantor_application.history import History
from cantor_application.user import User
from cantor_application.portfolio import Portfolio


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
            user.purchase(purchase_value, user, form.currency.data, currency_name, form.amount.data)
            flash(f"You have successfully bought amount: {form.amount.data} of: {currency_name}")
            return render_template('index.html', form=form)

        flash("Insufficient funds in the account - transaction canceled")

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
