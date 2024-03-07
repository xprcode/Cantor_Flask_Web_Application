from flask import render_template,  session



from cantor_application.helpers import lookup


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






if __name__ == '__main__':
    app.run()
