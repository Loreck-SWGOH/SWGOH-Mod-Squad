from flask import render_template, redirect, url_for, flash
# from werkzeug.urls import url_parse
# from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required
# from flask_login import logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, SubmitField
# from wtforms.validators import ValidationError, DataRequired, EqualTo

from app.controllers.users import RegistrationForm

from ..models.stats.user import UserStats
from ..models.user import User
# from ..models.profile import Profile


from flask import Blueprint
bp = Blueprint('admins', __name__)

"""
Forms and routes for administrating the web app
"""


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def home():
    """
    Admin page. Reached from admin link on home page (index).

    Displays site/app statistics. Allow admins to manage app
    information; users, events, teams, etc.
    """

    if not current_user.is_admin:
        return redirect(url_for('index.index'))

    user_stats = UserStats.get()
    # if login_form.validate_on_submit():
    #     try:
    #         user = User.get_from_login(login_form.email.data,
    #                                    login_form.password.data)
    #     except Exception as e:
    #         flash(str(e))
    #         return redirect(url_for("users.login"))

    #     if user is None:
    #         flash('Invalid email or password')
    #         return redirect(url_for('users.login'))

    #     login_user(user)
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('index.index')

    #     return redirect(next_page)

    return render_template('admin.html', user_stats=user_stats)


@bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
def list_users():
    users = User.get_all()
    return render_template('users.html', users=users)


class EditUserForm(FlaskForm):
    """
    Form to edit users
    """
    update_user = SubmitField("Update User")


@bp.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Admin page. Reached from admin link on home page (index).

    Displays site/app statistics. Allow admins to manage app
    information; users, events, teams, etc.
    """

    print("Edit user page")
    if not current_user.is_admin:
        return redirect(url_for('index.index'))

    # get all users
    user = User.get(id)
    print(user)
    # if login_form.validate_on_submit():
    #     try:
    #         user = User.get_from_login(login_form.email.data,
    #                                    login_form.password.data)
    #     except Exception as e:
    #         flash(str(e))
    #         return redirect(url_for("users.login"))

    #     if user is None:
    #         flash('Invalid email or password')
    #         return redirect(url_for('users.login'))

    #     login_user(user)
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('index.index')

    #     return redirect(next_page)

    return render_template('admin.html')


@bp.route('/admin/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    """
    Admin page. Reached from admin link on home page (index).

    Displays site/app statistics. Allow admins to manage app
    information; users, events, teams, etc.
    """

    print("Edit users page")
    if not current_user.is_admin:
        return redirect(url_for('index.index'))

    # get all users
    users = User.get_all()
    print(users)
    # if login_form.validate_on_submit():
    #     try:
    #         user = User.get_from_login(login_form.email.data,
    #                                    login_form.password.data)
    #     except Exception as e:
    #         flash(str(e))
    #         return redirect(url_for("users.login"))

    #     if user is None:
    #         flash('Invalid email or password')
    #         return redirect(url_for('users.login'))

    #     login_user(user)
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('index.index')

    #     return redirect(next_page)

    return render_template('admin.html')


@bp.route('/admin/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    """
    Admin page. Reached from admin link on home page (index).

    Displays site/app statistics. Allow admins to manage app
    information; users, events, teams, etc.
    """

    print("Edit users page")
    if not current_user.is_admin:
        return redirect(url_for('index.index'))

    # get all users
    users = User.get_all()
    print(users)

    return render_template('admin.html')


class AdminRegistrationForm(RegistrationForm):
    """
    Registration form for admin. Allow creation of admin accounts.

    Expand the user's registration form and add ability to create an admin
    account.
    Existing e-mail addresses not allowed. Repeat password must match.
    """

    is_admin = BooleanField("Administrator")


@bp.route('/admin/register', methods=['GET', 'POST'])
def register():
    """
    Registration page. Reached from registration link on home page (index)
    or from login page.

    Uses GET to allow form to be filled in. Uses POST to attempt registration.
    Valid form credentials attempt to add user to database. Successful
    registration redirects to the login page. Unsucessful registration reloads
    the registration page.
    """

    if not current_user.is_admin:
        return redirect(url_for('index.index'))

    reg_form = AdminRegistrationForm()
    if reg_form.validate_on_submit():
        if User.register(reg_form.email.data,
                         reg_form.password.data,
                         reg_form.first_name.data,
                         reg_form.last_name.data,
                         reg_form.is_admin.data):
            flash('User added.')
            return redirect(url_for('admins.register'))

    return render_template('register.html', title='Register', form=reg_form)
