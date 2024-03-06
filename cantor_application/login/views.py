from flask import Blueprint, render_template, flash, session
from flask_login import login_user
from werkzeug.security import check_password_hash

from cantor_application import db
from cantor_application.models.user import User
from cantor_application.forms.loginform import LoginForm

login_blueprint = Blueprint('login',__name__, template_folder='templates')


@login_blueprint.route('/login', methods = ['GET', 'POST'])
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
