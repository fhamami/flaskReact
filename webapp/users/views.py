from flask import render_template, Blueprint, request, flash, redirect, url_for, jsonify, abort, json, Flask, Response
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
    if request.is_xhr:
        if request.method == 'POST':
            if form.validate_on_submit():
                email = request.get_json('email')
                password = request.get_json('password')
                # email = request.json['email']
                # password = request.json['password']
                user = User.query.filter_by(email).first()
                if user is not None and user.is_correct_password(password):
                # if email is not None and password is not None:
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    # value = [{ 'username': user.email, 'password': user.password_plaintext }]
                    # value = request.json[{ 'username': user.email, 'password': user.password_plaintext }]
                    # js = [ { "name" : filename, "size" : st.st_size , "url" : url_for('show', filename=filename)} ]
                    flash('Thanks for logging in, {}'.format(current_user.email))
                    return redirect(url_for('post.index'))
                    # return jsonify({ 'username': user.email, 'password': user.password_plaintext }), 201
                    # return jsonify(value)
                    # return Response(json.dumps(value),  mimetype='application/json')
                # mail = request.get_json('email')
                # pswd = request.get_json('password')
                # login = User(mail=request.form['email'], pswd=request.form['password'])
                # login = User(email=request.get_json('email'), password=request.get_json('password'))
                # user.authenticated = True
                # db.session.add(login)
                # db.session.commit()
                # flash('Thanks for logging in, {}'.format(current_user.email))
                # return redirect(url_for('post.index'))
                else:
                    flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('login.html', form=form)

        # form = LoginForm(request.form)
        # if request.is_xhr:
        #     if form.validate_on_submit():
        #         email = request.get_json('email')
        #         password = request.get_json('password')
        #         user = User.query.filter_by(email=email).first()
        #         if user is not None and user.is_correct_password(password):
        #             user.authenticated = True
        #             user = User.query.all()
        #             ujson = json.dumps(user)
        #             form = EventForm.from_json(ujson)
        #             # return jsonify({
        #             #     'count': len(user)
        #             # })
        #             return jsonify({'email' : email, 'password' : password})
        # # return jsonify({'email' : email, 'password' : password})
        # # return redirect(url_for('post.index'))
        # return Response(json.dumps(user),  mimetype='application/json')

@users_blueprint.route('/background_process', methods = ['GET', 'POST'])
def background_process():
    # email = request.form['email']
    # password = request.form['password']
    #
    # # if email and password:
    # # # if email is None or password is None:
    # #     return jsonify({'error' : 'Missing data!'})
    # # return jsonify({'email' : email, 'password' : password})
    # return jsonify({ 'email': email, 'password': password }), 201

    # data = get_data(email, password)  # Get your data
    # return json.dumps(data)
    # pass

    # email = request.get_json('email')
    # password = request.get_json('password')
    # if email is None or password is None:
    #     abort(400) # missing arguments
    # if User.query.filter_by(email = email).first() is not None:
    #     abort(400) # existing user
    # user = User(email = email, password = password)
    # db.session.add(user)
    # db.session.commit()
    # return json.dumps({ 'email': user.email, 'password': user.password }), 201

    email = request.form['email']
    password = request.form['password']
    if email and password:
        mail = jsonify({'email' : email})
        pswd = jsonify({'password' : password})
        user = User(mail = mail, pswd = pswd)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Thanks for logging in, {}'.format(current_user.email))
        return redirect(url_for('post.index'))
    else:
        flash('ERROR! Incorrect login credentials.', 'error')

# @users_blueprint.route('/api/users', methods = ['GET', 'POST'])
# def new_user():
#     email = request.get_json('email')
#     password = request.get_json('password')
#     if email is None or password is None:
#         abort(400) # missing arguments
#     if User.query.filter_by(email = email).first() is not None:
#         abort(400) # existing user
#     user = User(email = email, password = password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({ 'email': user.email, 'password': user.password }), 201

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
