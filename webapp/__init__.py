from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_wtf.csrf import CsrfProtect
CsrfProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from webapp.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

from webapp.users.views import users_blueprint
from webapp.post.views import post_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(post_blueprint)
