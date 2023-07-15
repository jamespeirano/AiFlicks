from flask import Flask, render_template
from flask_session import Session
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from .config import Config
from .utils import scheduler
from .models import User

db = MongoEngine()
login_manager = LoginManager()

app = Flask(__name__, template_folder='frontend', static_folder='frontend/assets')
app.config.from_object(Config)

Session(app)
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.objects(pk=user_id).first()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

admin = Admin(app, name='Dashboard', template_mode='bootstrap3')
admin.add_view(ModelView(User))

from app import routes