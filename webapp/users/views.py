from flask import render_template, Blueprint, request, flash, redirect, url_for
from .forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user

from webapp import db
from webapp.models import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering!', 'success')
                return redirect(url_for('post.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.email))
                return redirect(url_for('post.index'))
            else:
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('users.login'))
