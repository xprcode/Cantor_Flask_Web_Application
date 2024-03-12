from flask import render_template

from cantor_application import app


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
