from flask import Blueprint, render_template,  session
from flask_login import login_required
from cantor_application.login.views import load_user
from cantor_application.models.history import History

history_blueprint = Blueprint('history',__name__, template_folder='templates')


@history_blueprint.route('/history', methods = ['GET'])
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
