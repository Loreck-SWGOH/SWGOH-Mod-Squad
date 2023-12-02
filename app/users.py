from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, \
                           SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.profile import Profile


from flask import Blueprint
bp = Blueprint('users', __name__)

""" Login and registration forms for users """


class LoginForm(FlaskForm):
    """ Login form """
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
    this page. If the user is found then reload home page. Invalid form
    credentials force the form to be reloaded.
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
    """ Registration form. Duplicate e-mail addresses not allowed. """

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField("Administrator")
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('E-mail address already exists.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page. Reached from registration link on home page (index)
    or from login page.

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
                         reg_form.last_name.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=reg_form)


class AllyCodeField(StringField):
    def process_formdata(self, valuelist):
        self.data = [v.replace('-', '') for v in valuelist]
        super().process_formdata(self.data)


class AllyCodeForm(FlaskForm):
    """ SWGOH profile form. """

    ally_code = AllyCodeField('Ally Code', validators=[DataRequired()])
    submit_ac = SubmitField('Update Profile')

    def validate_ally_code(self, ally_code):
        try:
            int(ally_code.data)
        except ValueError:
            raise ValidationError('Only numbers and dashes allowed.')


class PasswordForm(FlaskForm):
    """ Change password form. """

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
    Uses GET to allow form to be filled in. Uses POST to update profile.
    Valid form credentials attempt to update profile of user in database.
    Successful updating redirects to the login page. Unsucessful updates
    or invalid form credentials reload the profile form.
    """

# Is this section redundant?
    if not current_user.is_authenticated:
        flash("Must be logged in to update profile")
        return redirect(url_for('index.index'))

    ally_code_form = AllyCodeForm()
    password_form = PasswordForm()
    if "submit_ac" in request.form.keys():
        print("ally code submitted")
        if ally_code_form.validate():
            if Profile.update(uid, int(ally_code_form.ally_code.data)):
                flash('Profile updated')
                return redirect(url_for('users.login'))
    if "submit_pwd" in request.form.keys():
        print("password submitted")
        if password_form.validate():
            if User.update_password(uid, password_form.cur_password.data,
                                    password_form.new_password.data):
                flash("Password updated")
                return redirect(url_for("users.login"))
            flash("Incorrect password")
            return redirect(url_for("users.profile", uid=uid))
    print("GET or password not posted")

    return render_template('profile.html', title='Update Profile',
                           ally_code_form=ally_code_form,
                           password_form=password_form, id=uid)


@bp.route('/logout')
def logout():
    """
    Log out user using flask_login package. Return to home page (index)
    """
    logout_user()
    return redirect(url_for('index.index'))
