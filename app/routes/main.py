from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.plan_data import plans

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
@login_required  
def index():
    return render_template("index.html", user=current_user)

@main_bp.route('/pricing')
def pricing():
    return render_template('pricing.html', plans=plans)

@main_bp.route('/models')
def models():
    return render_template('models.html', user=current_user)

@main_bp.route('/guide')
def guide():
    return render_template('guide.html', user=current_user)