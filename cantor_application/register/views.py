from flask import Blueprint, render_template, flash
from werkzeug.security import generate_password_hash
from sqlalchemy import func
from cantor_application import db
from cantor_application.forms.registrationform import RegistrationForm
from cantor_application.models.user import User


registration_blueprint = Blueprint('register',__name__, template_folder='templates')


@registration_blueprint.route("/register", methods=["GET", "POST"])
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
