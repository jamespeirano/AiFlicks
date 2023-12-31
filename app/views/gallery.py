import os
import random
import base64
import asyncio
import dotenv
import traceback
from flask import request, render_template, abort, jsonify, Blueprint
from flask_login import current_user
from concurrent.futures import TimeoutError
from app.api import Model, ModelError
from app.data import PROMPTS

dotenv.load_dotenv()

gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

HUGGING_FACE_API_URLS = {
    'stable-diffusion-v15': os.environ.get('STABLE_DIFFUSION_V15'),
    'stable-diffusion-v21': os.environ.get('STABLE_DIFFUSION_V21'),
    
    'dreamlike-photo-real': os.environ.get('DREAMLIKE_PHOTO_REAL'),
    'dream-shaper': os.environ.get('DREAM_SHAPER'),
    'realistic-vision-v14': os.environ.get('REALISTIC_VISION_V14'),
    'nitro-diffusion': os.environ.get('NITRO_DIFFUSION'),
    'dreamlike-anime': os.environ.get('DREAMLIKE_ANIME_V10'),
    'anything-v5': os.environ.get('ANYTHING_V5'),
}

# 'stable-diffusion-xl-base-0.9': os.environ.get('STABLE_DIFFUSION_XL_BASE_0.9'),
# 'stable-diffusion-xl-base-1.0': os.environ.get('STABLE_DIFFUSION_XL_BASE_1.0'),

@gallery_bp.route('/')
def gallery():
    exclude_images = ['forest.png', 'hoodie-b.png', 'hoodie-w.png', 'tshirt-b.png', 'tshirt-w.png', 'logo.png']
    images = [f for f in os.listdir('app/static/img') if f.endswith('.png') and f not in exclude_images]
    return render_template('gallery.html', images=images, user=current_user)

@gallery_bp.route('/model', methods=['POST'])
async def model():
    try:
        print('[Function: model] Received request')
        data = request.form
        model_input = data.get('model_input')
        selected_model = HUGGING_FACE_API_URLS.get(model_input)
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt')

        if not selected_model or not prompt:
            return abort(400, "Invalid form data supplied")
        
        if not negative_prompt or negative_prompt.isspace():
            negative_prompt = get_negative_prompt(selected_model, prompt)
        return await generate_image(selected_model, prompt, negative_prompt)

    except TimeoutError:
        print('[Function: model] Timeout error occurred')
        return render_template('error.html', error='Timeout')

    except Exception as e:
        print('[Function: model] Error occurred')
        traceback.print_exc()
        return render_template('error.html', error=str(e))

async def generate_image(selected_model, prompt, negative_prompt):
    for attempt in range(3):
        try:
            print(f'[Function: generate_image] Attempt {attempt + 1}')
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
    model = Model(selected_model, prompt, negative_prompt, 7, 20, 1024, 1024)
    try:
        print('[Function: query_model] Generating image')
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
    try:
        prompt = random.choice(PROMPTS[selected_model])["prompt"]
    except KeyError:
        return abort(400, "Invalid model name supplied")
    return jsonify({'prompt': prompt})

def get_negative_prompt(model, given_prompt):
    prompt_list = PROMPTS.get(model)
    if not prompt_list:
        return None
    for prompt_dict in prompt_list:
        if prompt_dict['prompt'] == given_prompt:
            return prompt_dict['negative_prompt']
    return ""
