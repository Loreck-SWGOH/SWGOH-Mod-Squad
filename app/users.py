from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)

""" Login and registration forms for users """


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page. Reached from login button on home page (index).
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

    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
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
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        if User.register(reg_form.email.data,
                         reg_form.password.data,
                         reg_form.firstname.data,
                         reg_form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=reg_form)


@bp.route('/logout')
def logout():
    """
    Log out user using flask_login package. Return to home page (index)
    """
    logout_user()
    return redirect(url_for('index.index'))
