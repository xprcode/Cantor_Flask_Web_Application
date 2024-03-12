from flask import Blueprint, render_template,  flash, session
from flask_login import login_required
from cantor_application.forms.buyform import BuyForm
from cantor_application.helpers import lookup
from cantor_application.login.views import load_user

buy_blueprint = Blueprint('buy',__name__, template_folder='templates')


@buy_blueprint.route('/buy', methods = ['GET', 'POST'])
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
