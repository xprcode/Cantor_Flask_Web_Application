from flask import Blueprint, redirect, url_for
from flask_login import logout_user

logout_blueprint = Blueprint('logout',__name__, template_folder='templates')


@logout_blueprint.route('/logout')
def logout():
    """
    This route logs out the current user by using the `logout_user()` function
    provided by Flask-Login. 

    Returns:
    redirect: Redirects the user to the login page ('login' endpoint).
    """
    logout_user()
    return redirect(url_for('login.login'))