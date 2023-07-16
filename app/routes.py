import os
import base64
import math
from flask import render_template, request, jsonify, session, abort, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from utils import generate_random_prompt, generate_negative_prompt, resize_avatar
from model import Model, ModelError
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from app import app, login_manager
from .models import User

executor = ThreadPoolExecutor(max_workers=5)

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
    
    page = request.args.get('page', default=1, type=int)
    rows_per_page = request.args.get('rows', default=10, type=int)
    
    users = User.objects()
    total_users = len(users)
    total_pages = math.ceil(total_users / rows_per_page)
    
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    paginated_users = users[start_index:end_index]
    
    return render_template('admin_users.html', user=current_user, users=paginated_users, 
                           total_pages=total_pages, current_page=page, rows=rows_per_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.objects(username=request.form.get('username').strip()).first()
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
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        avatar = request.files['avatar']

        # Validate input
        if not all([first_name, last_name, username, email, password]):
            flash('Please enter all the fields')
            return redirect(url_for('signup'))

        # Check if account already exists
        existing_user = User.objects(email=email).first()
        if existing_user:
            flash('An account with that email already exists. Please login.')
            return redirect(url_for('login'))

        # Check if username is taken
        existing_username = User.objects(username=username).first()
        if existing_username:
            flash('That username is already taken. Please choose a different username.')
            return redirect(url_for('signup'))
        
        # Create a new user account
        user = User(first_name=first_name, last_name=last_name, email=email, username=username)
        user.set_password(password)

        # Resize and save the avatar
        if avatar and allowed_file(avatar.filename):
            try:
                resized_avatar = resize_avatar(avatar.read())
            except Exception as e:
                print("Error resizing avatar: ", e)
                resized_avatar = None

            if resized_avatar: 
                user.save_avatar(resized_avatar)
            else:
                with open('app/frontend/assets/img/default.png', 'rb') as img:
                    default_avatar = img.read()
                    user.save_avatar(default_avatar)
        user.save()
        flash('Your account has been created! You can now login.')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


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
def model():
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

        response = executor.submit(generate_image, selected_model, prompt, negative_prompt).result(timeout=120)
        return response

    except TimeoutError:
        return render_template('error.html', error='Timeout')

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return render_template('error.html', error=str(e))
    

def generate_image(selected_model, prompt, negative_prompt):
    for attempt in range(3):
        try:
            image = query_model(selected_model, prompt, negative_prompt)
        except ModelError as e:
            if attempt < 2: # Only allow retries if less than 2 attempts have been made
                print(f"Attempt {attempt + 1} failed: {e}")
                continue
            else:
                return render_template('error.html', error=str(e))
        image_data = f"data:image/png;base64,{image}"
        return render_template('result.html', image=image_data, prompt=prompt, user=current_user)
    return render_template('error.html', error='No image generated after retries')


def query_model(model, prompt, negative_prompt):
    model = Model(model, prompt, negative_prompt)
    try:
        image = model.generate()
    except TimeoutError:
        raise ModelError('Timeout')
    
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