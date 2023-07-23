from flask import request, render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.services import create_subscription, get_plan_by_name
from app.data import PLANS

user_bp = Blueprint('aiflix_user', __name__, url_prefix='/aiflix_user')

@user_bp.route('/subscription', methods=['POST'])
@login_required
def handle_subscription():
    user = current_user
    current_subscription = user.subscription
    selected_plan_name = request.form.get('plan_name')
    selected_plan = get_plan_by_name(selected_plan_name)

    print(f"Selected plan: {selected_plan.name}, current plan: {current_subscription.name}")

    if selected_plan['price'] > current_subscription['price']:
        subscription_action = url_for('upgrade_subscription', new_subscription_name=selected_plan.name)
    elif selected_plan['price'] < current_subscription['price']:
        subscription_action = url_for('downgrade_subscription', new_subscription_name=selected_plan.name)
    else:
        flash('You are already subscribed to this plan.', 'info')
        return redirect(url_for('auth.signin'))

    return render_template('pricing.html', subscription_action=subscription_action)

def upgrade_subscription(new_subscription_name):
    user = current_user
    create_subscription(new_subscription_name, PLANS[new_subscription_name])
    user.upgrade_subscription(new_subscription_name)
    return redirect(url_for('auth.login'))

def downgrade_subscription(new_subscription_name):
    user = current_user
    create_subscription(new_subscription_name, PLANS[new_subscription_name])
    user.downgrade_subscription(new_subscription_name)
    return redirect(url_for('auth.login'))