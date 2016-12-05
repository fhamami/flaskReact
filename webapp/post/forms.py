from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class AddPostForm(Form):
    post_title = StringField('Post Title', validators=[DataRequired()])
    post_description = StringField('Post Description', validators=[DataRequired()])
