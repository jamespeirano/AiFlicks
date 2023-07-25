from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.services import get_all_users

admin_bp = Blueprint('aiflix', __name__, url_prefix='/aiflix')

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/admin_profile.html', user=current_user)

@admin_bp.route('/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    users = get_all_users()
    return render_template('admin/admin_users.html', user=current_user, users=users)