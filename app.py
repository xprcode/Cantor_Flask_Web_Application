from flask import render_template,  flash, session

from flask_login import (
    login_required,
)

from cantor_application.helpers import lookup
from cantor_application.login.views import load_user
from cantor_application.forms.sellform import SellForm
from cantor_application import app, db
from cantor_application.models.history import History
from cantor_application.models.user import User
from cantor_application.models.portfolio import Portfolio






@app.route('/')
def index():
    """
    This route renders the index.html template.

    Returns:
    str: Rendered HTML content of the index page.
    """
    return render_template('index.html')


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
