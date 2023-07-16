import os
import base64
import time
import math
from flask import render_template, request, jsonify, session, abort, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from utils import generate_random_prompt, generate_negative_prompt
from model import Model
from app import app, login_manager
from .models import User

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
    return render_template("index.html")


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    username = current_user.email.split('@')[0]
    return render_template('admin_profile.html', username=username)


@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    
    username = current_user.email.split('@')[0]
    
    page = request.args.get('page', default=1, type=int)
    rows_per_page = request.args.get('rows', default=10, type=int)
    
    users = User.objects()
    users = [user for user in users if user != current_user]
    total_users = len(users)
    total_pages = math.ceil(total_users / rows_per_page)
    
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    paginated_users = users[start_index:end_index]
    
    return render_template('admin_users.html', username=username, users=paginated_users, 
                           total_pages=total_pages, current_page=page, rows=rows_per_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.objects(email=request.form.get('email')).first()
        if user and user.check_password(request.form.get('password')):
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
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if account already exists
        existing_user = User.objects(email=email).first()
        if existing_user:
            flash('An account with that email already exists. Please login.')
            return redirect(url_for('login'))
        
        # Create a new user account
        user = User(email=email)
        user.set_password(password)
        user.save()
        
        flash('Your account has been created! You can now login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/models')
def models():
    return render_template('models.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/gallery')
def gallery():
    exclude_images = ['forest.png', 'hoodie-b.png', 'hoodie-w.png', 'tshirt-b.png', 'tshirt-w.png', 'logo.png']
    images = [f for f in os.listdir('app/frontend/assets/img') if f.endswith('.png') and f not in exclude_images]
    return render_template('gallery.html', images=images)


@app.route('/model', methods=['POST'])
async def model():
    data = request.form
    selected_model = data.get('model_input')
    prompt = data.get('prompt')
    negative_prompt = data.get('negative_prompt')

    if not selected_model or not prompt:
        return abort(400, "Invalid form data supplied")

    HUGGING_API = HUGGING_FACE_API_URLS.get(selected_model)
    if not HUGGING_API:
        return abort(400, "Invalid model selected")

    if not negative_prompt or negative_prompt.isspace():
        negative_prompt = generate_negative_prompt(selected_model)

    return await generate_image_and_render(HUGGING_API, selected_model, prompt, negative_prompt)


async def generate_image_and_render(HUGGING_API, selected_model, prompt, negative_prompt, retry_count=0):
    model = Model(HUGGING_API, prompt=prompt, negative_prompt=negative_prompt)

    print("Prompt: ", prompt)
    print("Negative Prompt: ", negative_prompt)
    print("Model: ", selected_model)
    print("Hugging Face API: ", HUGGING_API)

    try:
        start = time.time()
        response = await model.generate_image()
        print(f"Time taken: {time.time() - start} seconds")
        if response == "timeout" and retry_count < 5:  # Limit retries to avoid infinite recursion
            print('retrying...')
            return await generate_image_and_render(HUGGING_API, selected_model, prompt, negative_prompt, retry_count + 1)
    except Exception as e:
        return render_template("error.html", error=str(e))

    if not response or response == "timeout":
        return render_template("error.html", error="No image generated or timeout after retries")
    
    image_data = f"data:image/png;base64,{response}"
    return render_template("result.html", image=image_data, prompt=prompt)


@app.route('/gallery-image/<img_name>', methods=['GET'])
def gallery_image(img_name):
    try:
        file_path = f"app/frontend/assets/img/{img_name}"
        print(f"Fetching image from: {file_path}")
        with open(file_path, "rb") as img_file:
            image = base64.b64encode(img_file.read()).decode('utf-8')
        image_data = f"data:image/png;base64,{image}"
        return render_template("result.html", image=image_data, prompt="Gallery Image")
    except Exception as e:
        print(f"Error serving image: {e}")
        return render_template("error.html")


@app.route('/random-prompt', methods=['GET'])
def random_prompt():
    selected_model = request.args.get('model')
    prompt = generate_random_prompt(selected_model)
    return jsonify({'prompt': prompt})