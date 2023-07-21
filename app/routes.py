import asyncio
import os
import base64
import dotenv
from flask import request, render_template, abort, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user, login_user, logout_user
from concurrent.futures import TimeoutError
from google_auth_oauthlib.flow import Flow

from app import app, login_manager
from .db_ops import *
from .plan_data import plans

from model import Model, ModelError
from utils import generate_negative_prompt, generate_random_prompt, resize_avatar, generate_random_password, get_google_profile_pic

dotenv.load_dotenv()

HUGGING_FACE_API_URLS = {
    'stable-diffusion': os.environ.get('HUGGING_FACE_API_URL1'),
    'realistic-vision': os.environ.get('HUGGING_FACE_API_URL2'),
    'nitro-diffusion': os.environ.get('HUGGING_FACE_API_URL3'),
    'dreamlike-anime': os.environ.get('HUGGING_FACE_API_URL4'),
}


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view this page.')
    return redirect(url_for('login'))


@app.route('/')
@login_required  
def index():
    session.permanent = False
    if 'oauth_token' in session:
        info = google_auth.authorized_response()
        email = info['email']
        user = get_user_by_email(email)
        if user:
            login_user(user)
    return render_template("index.html", user=current_user)


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin_profile.html', user=current_user)


@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    users = get_all_users()
    return render_template('admin_users.html', user=current_user, users=users)


@app.route('/login/google')
def google_login():
    google_auth = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.environ.get('GOOGLE_CLIENT_KEY'),
                "client_secret": os.environ.get('GOOGLE_CLIENT_SECRET'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [url_for('google_auth', _external=True, _scheme='https')]
            }
        },
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email']
    )

    redirect_uri = url_for('google_auth', _external=True)
    google_auth.redirect_uri = redirect_uri
    authorization_url, state = google_auth.authorization_url()

    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/login/google/auth')
def google_auth():
    state = session.get('oauth_state')
    if state is None:
        return redirect(url_for('login'))

    google_auth = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.environ.get('GOOGLE_CLIENT_KEY'),
                "client_secret": os.environ.get('GOOGLE_CLIENT_SECRET'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [url_for('google_auth', _external=True, _scheme='https')]
            }
        },
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'],
        state=state
    )

    google_auth.redirect_uri = url_for('google_auth', _external=True)
    
    # Ensure that we got back the same state to avoid CSRF attacks
    if state != request.args.get('state', ''):
        return redirect(url_for('login'))
    
    google_auth.fetch_token(
        authorization_response_url=request.url,
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        code=request.args.get('code')
    )

    userinfo = google_auth.authorized_session().get('https://www.googleapis.com/oauth2/v1/userinfo').json()

    email = userinfo['email'] 
    avatar = userinfo['picture']
    avatar = get_google_profile_pic(avatar)
    resized_avatar = resize_avatar(avatar)

    existing_user = get_user_by_email(email)
    if existing_user:
        login_user(existing_user)
        return redirect(url_for('index'))

    new_user = create_user(
        email=email,
        password=generate_random_password(),
        avatar=resized_avatar
    )

    login_user(new_user)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = get_user_by_email(request.form.get('email').strip())
        if user and user.check_password(request.form.get('password').strip()):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out. See you again soon!')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        avatar = request.files['avatar']

        # Validate input
        if not all([email, password]):
            flash('Please enter all the fields')
            return redirect(url_for('signup'))

        existing_user = get_user_by_email(email)
        if existing_user:
            flash('An account with that email already exists. Please login.')
            return redirect(url_for('login'))

        existing_username = get_user_by_email(email)
        if existing_username:
            flash('That username is already taken. Please choose a different username.')
            return redirect(url_for('signup'))
        
        # Resize and save the avatar
        if avatar and allowed_file(avatar.filename):
            try:
                resized_avatar = resize_avatar(avatar.read())
            except Exception as e:
                print("Error resizing avatar: ", e)
                resized_avatar = None
        
        if not avatar or resized_avatar is None:
            with open('app/frontend/assets/img/default.png', 'rb') as img:
                resized_avatar = img.read()

        new_user = create_user(email, password, resized_avatar)
        flash('Your account has been created!')
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/subscription', methods=['POST'])
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
        return redirect(url_for('signin'))

    return render_template('pricing.html', subscription_action=subscription_action)


def upgrade_subscription(new_subscription_name):
    user = current_user
    create_subscription(new_subscription_name, plans[new_subscription_name])
    user.upgrade_subscription(new_subscription_name)
    return redirect(url_for('login'))


def downgrade_subscription(new_subscription_name):
    user = current_user
    create_subscription(new_subscription_name, plans[new_subscription_name])
    user.downgrade_subscription(new_subscription_name)
    return redirect(url_for('login'))


@app.route('/pricing')
def pricing():
    return render_template('pricing.html', plans=plans)


@app.route('/models')
def models():
    return render_template('models.html', user=current_user)


@app.route('/guide')
def guide():
    return render_template('guide.html', user=current_user)


@app.route('/gallery')
def gallery():
    exclude_images = ['forest.png', 'hoodie-b.png', 'hoodie-w.png', 'tshirt-b.png', 'tshirt-w.png', 'logo.png']
    images = [f for f in os.listdir('app/frontend/assets/img') if f.endswith('.png') and f not in exclude_images]
    return render_template('gallery.html', images=images, user=current_user)


@app.route('/model', methods=['POST'])
async def model():
    try:
        data = request.form
        model_input = data.get('model_input')
        selected_model = HUGGING_FACE_API_URLS.get(model_input)
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt')

        if not selected_model or not prompt:
            return abort(400, "Invalid form data supplied")
        
        if not negative_prompt or negative_prompt.isspace():
            negative_prompt = generate_negative_prompt(model_input)
        return await generate_image(selected_model, prompt, negative_prompt)

    except TimeoutError:
        return render_template('error.html', error='Timeout')

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return render_template('error.html', error=str(e))
    

async def generate_image(selected_model, prompt, negative_prompt):
    for attempt in range(3):
        try:
            image = await query_model(selected_model, prompt, negative_prompt)
        except ModelError as e:
            if attempt < 2: # Only allow retries if less than 2 attempts have been made
                print(f"Attempt {attempt + 1} failed: {e}")
                continue
            else:
                return render_template('error.html', error=str(e))
        image_data = f"data:image/png;base64,{image}"
        return render_template('result.html', image=image_data, prompt=prompt, user=current_user)
    return render_template('error.html', error='No image generated after retries')


async def query_model(selected_model, prompt, negative_prompt):
    model = Model(selected_model, prompt, negative_prompt)
    try:
        image = await asyncio.wait_for(model.generate(), timeout=120)
    except TimeoutError:
        raise ModelError('Timeout while generating image')

    if not image:
        raise ModelError('No image generated')
    return image


@app.route('/gallery-image/<path:img_name>', methods=['GET'])
def gallery_image(img_name):
    try:
        file_path = f"app/frontend/assets/img/{img_name}"
        with open(file_path, "rb") as img_file:
            image = base64.b64encode(img_file.read()).decode('utf-8')
        image_data = f"data:image/png;base64,{image}"
        return render_template("result.html", image=image_data, prompt="Gallery Image", user=current_user)
    except Exception as e:
        print(f"Error serving image: {e}")
        return render_template("error.html")


@app.route('/random-prompt', methods=['GET'])
def random_prompt():
    selected_model = request.args.get('model')
    prompt = generate_random_prompt(selected_model)
    return jsonify({'prompt': prompt})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 