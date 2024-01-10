from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, url_for, redirect, request, flash
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

from modules import LoginForm, RegistrationForm

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

    def __repr__(self) -> str:
        return f'User: {self.name}'

    def get_user_info(self):
        """Retrieves user information from the database and updates the instance."""

        user = User.query.filter_by(name=self.name).first()

        if user:
            self.name = user.name
        else:
            self.name = ""


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

@app.route('/buy')
@login_required
def buy():
    return render_template('buy.html')

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
