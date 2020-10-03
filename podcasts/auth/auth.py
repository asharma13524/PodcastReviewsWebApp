from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, logout_user
from ..models import db, User
from .. import login_manager
from ..forms import LoginForm, SignupForm
from datetime import datetime as dt
from werkzeug.security import check_password_hash


auth_bp = Blueprint('auth_bp', __name__,
 template_folder='templates', static_folder='static')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User-sign up page and logic

    GET requests serve sign-up page
    POST requests validate the sign-up form and create a user.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            created_on = dt.now()
            user = User(created_on=created_on, email=form.email.data, username=form.username.data)
            user.set_password(password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user) # officially login new user
            return redirect(url_for('home_bp.home'))
        flash('A user already exists with that email address.')
    return render_template('signup.html',
        form=form,
        title='Create an Account',
        template='signup-page')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in.
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home_bp.home'))
        flash('Invalid username/password combination.')
    return render_template('login.html',
        form=form,
        title = 'Log In.',
        template='login-page')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect(url_for('home_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged in upon the page loading."""
    if user_id is not None:
        return User.query.get(user_id)
    return render_template('home_bp.home')


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to the Login Page."""
    flash('You must be logged in to do that!')
    return redirect(url_for('auth_bp.login'))
