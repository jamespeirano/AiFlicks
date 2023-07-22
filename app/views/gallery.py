import os
import base64
import asyncio
import dotenv
from flask import request, render_template, abort, jsonify, Blueprint
from flask_login import current_user
from concurrent.futures import TimeoutError
from app.api import Model, ModelError
from utils import generate_negative_prompt, generate_random_prompt

dotenv.load_dotenv()

gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

HUGGING_FACE_API_URLS = {
    'stable-diffusion': os.environ.get('HUGGING_FACE_API_URL1'),
    'realistic-vision': os.environ.get('HUGGING_FACE_API_URL2'),
    'nitro-diffusion': os.environ.get('HUGGING_FACE_API_URL3'),
    'dreamlike-anime': os.environ.get('HUGGING_FACE_API_URL4'),
}

@gallery_bp.route('/')
def gallery():
    exclude_images = ['forest.png', 'hoodie-b.png', 'hoodie-w.png', 'tshirt-b.png', 'tshirt-w.png', 'logo.png']
    images = [f for f in os.listdir('app/static/img') if f.endswith('.png') and f not in exclude_images]
    return render_template('gallery.html', images=images, user=current_user)

@gallery_bp.route('/model', methods=['POST'])
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

@gallery_bp.route('/gallery_image/<path:img_name>', methods=['GET'])
def gallery_image(img_name):
    try:
        file_path = f"app/static/img/{img_name}"
        with open(file_path, "rb") as img_file:
            image = base64.b64encode(img_file.read()).decode('utf-8')
        image_data = f"data:image/png;base64,{image}"
        return render_template("result.html", image=image_data, prompt="Gallery Image", user=current_user)
    except Exception as e:
        print(f"Error serving image: {e}")
        return render_template("error.html")

@gallery_bp.route('/random-prompt', methods=['GET'])
def random_prompt():
    selected_model = request.args.get('model')
    prompt = generate_random_prompt(selected_model)
    return jsonify({'prompt': prompt})