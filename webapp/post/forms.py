from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddPostForm(Form):
    post_title = StringField('Post Title', validators=[DataRequired()])
    post_description = StringField('Post Description', validators=[DataRequired()])

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])
