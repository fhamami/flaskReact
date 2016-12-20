from flask import render_template, Blueprint, request, flash, redirect, url_for, Flask, jsonify, session
from webapp.models import Post
from .forms import AddPostForm, LoginForm

from webapp import db
import json

post_blueprint = Blueprint('post', __name__, template_folder='templates')


@post_blueprint.route('/', methods=['GET', 'POST'])
@post_blueprint.route('/home', methods=['GET', 'POST'])
def index():
    # form = LoginForm(request.form)
    all_post = Post.query.all()
    form = LoginForm(request.form)
    # return render_template('login.html', form=form)
    return render_template('posts.html', posts=all_post, form=form)

@post_blueprint.route('/login.json', methods=["POST"])
def login():
    # log the user in.
    email = request.form.get('email')
    password = request.form.get('password')

    session['email'] = email

    # jsonify = return a response object from flask that contains JSON instead of HTML
    # return jsonify({'cher': 'is awesome'})
    return jsonify({ 'username': email, 'password': password})

@post_blueprint.route('/aboutme.json', methods=["POST"])
def update_about_me():
    # save the new about me text in DB
    aboutme_text = request.form.get('about_me')
    print '\n\n\n\n', aboutme_text, '\n\n\n\n'
    return jsonify({'save': 'successful'})

@post_blueprint.route('/logout.json', methods=["POST"])
def logout():
    print "\n\n\n\nSession before we cleared it.\n", session
    session.clear()
    print "\n\n\n\nSession after we cleared it.\n", session
    return jsonify({'logout': 'successful'})

@post_blueprint.route('/add', methods=['GET', 'POST'])
def add_post():
    form = AddPostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_post = Post(form.post_title.data, form.post_description.data)
            db.session.add(new_post)
            db.session.commit()
            flash('New post, {}, added!'.format(new_post.post_title), 'success')
            return redirect(url_for('post.index'))
        else:
            #flash_errors(form)
            flash('ERROR! Post was not added.', 'error')

    return render_template('add_post.html',
                           form=form)

# @post_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if request.is_xhr:
#         if request.method == 'POST':
#             if form.validate_on_submit():
#                 email = request.get_json('email')
#                 password = request.get_json('password')
#                 user = User.query.filter_by(email).first()
#                 if user is not None and user.is_correct_password(password):
#                     user.authenticated = True
#                     db.session.add(user)
#                     db.session.commit()
#                     login_user(user)
#                     flash('Thanks for logging in, {}'.format(current_user.email))
#                     return redirect(url_for('post.index'))
#                 else:
#                     flash('ERROR! Incorrect login credentials.', 'error')
#     return render_template('login.html', form=form)
#
# @post_blueprint.route('/background_process', methods = ['GET', 'POST'])
# def background_process():
#     email = request.form['email']
#     password = request.form['password']
#     if email and password:
#         mail = jsonify({'email' : email})
#         pswd = jsonify({'password' : password})
#         user = User(mail = mail, pswd = pswd)
#         db.session.add(user)
#         db.session.commit()
#         login_user(user)
#         flash('Thanks for logging in, {}'.format(current_user.email))
#         return redirect(url_for('post.index'))
#     else:
#         flash('ERROR! Incorrect login credentials.', 'error')
