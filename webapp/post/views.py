from flask import render_template, Blueprint, request, flash, redirect, url_for
from webapp.models import Post
from .forms import AddPostForm

from webapp import db

post_blueprint = Blueprint('post', __name__, template_folder='templates')


@post_blueprint.route('/')
def index():
    all_post = Post.query.all()
    return render_template('posts.html', posts=all_post)

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
