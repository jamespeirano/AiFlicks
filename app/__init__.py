from flask import Flask, render_template, redirect, url_for, flash
from flask_session import Session
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from .config import Config

db = MongoEngine()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='frontend', static_folder='frontend/assets')
    app.config.from_object(config_class)

    Session(app)
    db.init_app(app)
    login_manager.init_app(app)

    from . import models
    admin = Admin(app, name='Dashboard', template_mode='bootstrap3')
    admin.add_view(ModelView(models.User))

    from .routes import main_bp, admin_bp, auth_bp, user_bp, gallery_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(gallery_bp)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.objects(pk=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('You must be logged in to view this page.')
        return redirect(url_for('auth.login'))

    return app