from flask import render_template, redirect, url_for, flash, request
# from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
# from flask_login import login_user, logout_user, current_user, login_required
from flask_login import logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, \
                           SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo

from app.controllers.users import RegistrationForm

from ..models.user import User
from ..models.profile import Profile


from flask import Blueprint
bp = Blueprint('admins', __name__)

"""
Forms for user information, i.e. login, registration, etc.
"""


class AdminUsersForm(FlaskForm):
    """
    Manage users form
    """
    add_user = SubmitField('Add User')
    rm_user = SubmitField('Remove User')


@bp.route('/admin', methods=['GET', 'POST'])
def home():
    """
    Admin page. Reached from admin link on home page (index).

    Displays site/app statistics. Allow admins to manage app
    information; users, etc.i.e. users.
    """

    if not current_user.is_admin:
        return redirect(url_for('index.index'))

    admin_user_form = AdminUsersForm()
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

    return render_template('admin.html', form=admin_user_form)


class AdminRegistrationForm(RegistrationForm):
    """
    Registration form for admin. Allow creationg of admin accounts.

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


""" Profile forms"""


class AllyCodeForm(FlaskForm):
    """
    SWGOH profile form.
    """

    class AllyCodeField(StringField):
        def process_formdata(self, valuelist):
            self.data = [v.replace('-', '') for v in valuelist]
            super().process_formdata(self.data)

    ally_code = AllyCodeField('Ally Code', validators=[DataRequired()])
    submit_ac = SubmitField('Update Profile')

    def validate_ally_code(self, ally_code):
        try:
            int(ally_code.data)
        except ValueError:
            raise ValidationError('Only numbers and dashes allowed.')


class PasswordForm(FlaskForm):
    """
    Change password form.

    Repeat password must match.
    """

    cur_password = PasswordField("Current Password")
    new_password = PasswordField('New Password')
    new_password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('new_password')])
    submit_pwd = SubmitField('Update Password')


@bp.route('/profile/<int:uid>', methods=['GET', 'POST'])
@login_required
def profile(uid):
    """
    Profile page. Reached from any page while logged in.

    Displays 2 forms, SWGOH profile and change password.

    Needs unique names for the submit buttons on each form,
    since validate_on_submit() doesn't work with multiple forms.

    Uses GET to allow form to be filled in. Uses POST to update profile.
    Valid form credentials attempt to update profile/change password of user
    in database. Successful updating redirects to the login page.
    Unsucessful updates or invalid form credentials reload the profile form.
    """

# Is this section redundant?
    if not current_user.is_authenticated:
        flash("Must be logged in to update profile")
        return redirect(url_for('index.index'))

    ally_code_form = AllyCodeForm()
    password_form = PasswordForm()
    if "submit_ac" in request.form.keys():
        if ally_code_form.validate():
            if Profile.update(uid, int(ally_code_form.ally_code.data)):
                flash('Profile updated')
                return redirect(url_for('users.login'))
            flash("Couldn't update profile")
            return redirect(url_for("users.profile", uid=uid))

    if "submit_pwd" in request.form.keys():
        if password_form.validate():
            if User.update_password(
              uid, password_form.cur_password.data,
              generate_password_hash(password_form.new_password.data)):
                flash("Password updated")
                return redirect(url_for("users.login"))
            flash("Incorrect password")
            return redirect(url_for("users.profile", uid=uid))

    return render_template('profile.html', title='Update Profile',
                           ally_code_form=ally_code_form,
                           password_form=password_form, id=uid)


@bp.route('/logout')
def logout():
    """
    Log out user.

    Use flask_login package to log out then return to home page (index)
    """
    logout_user()
    return redirect(url_for('index.index'))
