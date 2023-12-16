from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
                           SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from ..models.user import User
from ..models.profile import Profile


from flask import Blueprint
bp = Blueprint('users', __name__)

"""
Forms for user information, i.e. login, registration, etc.
"""


class LoginForm(FlaskForm):
    """
    Login form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page. Reached from login link on home page (index).

    Uses GET to allow form to be filled in. Uses POST to attempt login.
    Valid form credentials check for user in database. If user not found
    or a database error occurs, flash an error and return (redirect) to
    this page. If the user is found then login user (via flask_login) and
    reload home page. Invalid form credentials force the form to be reloaded.
    """

    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            user = User.get_from_login(login_form.email.data,
                                       login_form.password.data)
        except Exception as e:
            flash(str(e))
            return redirect(url_for("users.login"))

        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)

    return render_template('login.html', title='Log In', form=login_form)


class RegistrationForm(FlaskForm):
    """
    Registration form.

    Existing e-mail addresses not allowed. Repeat password must match.
    """

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('E-mail address already exists.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Allow user to register themselve. Reached from registration link on home
    page (index) or from login page. Users cannot register as administrators

    Uses GET to allow form to be filled in. Uses POST to attempt registration.
    Valid form credentials attempt to add user to database. Successful
    registration redirects to the login page. Unsucessful registration reloads
    the registration page.
    """

    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        if User.register(reg_form.email.data,
                         reg_form.password.data,
                         reg_form.first_name.data,
                         reg_form.last_name.data, False):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=reg_form)


""" Profile forms """


class AllyCodeField(StringField):
    def process_formdata(self, valuelist):
        self.data = [v.replace('-', '') for v in valuelist]
        super().process_formdata(self.data)


class AllyCodeForm(FlaskForm):
    """
    SWGOH profile form.
    """

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
