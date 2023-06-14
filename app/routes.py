import os
import base64
from flask import render_template, request, jsonify
from dotenv import load_dotenv
from utils import generate_random_prompt
from model import Model
from app import app

load_dotenv()

HUGGING_FACE_API_URLS = {
    'stable-diffusion': os.getenv('HUGGING_FACE_API_URL1'),
    'realistic-vision': os.getenv('HUGGING_FACE_API_URL2'),
    'nitro-diffusion': os.getenv('HUGGING_FACE_API_URL3'),
    'dreamlike-anime': os.getenv('HUGGING_FACE_API_URL4'),
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/models')
def models():
    return render_template('models.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/model', methods=['GET', 'POST'])
async def model():
    try:
        selected_model = request.form.get('model_input')
        if selected_model is None:
            raise ValueError("Model not selected")
        HUGGING_API = HUGGING_FACE_API_URLS.get(selected_model)
        prompt = request.form['prompt']
    except KeyError:
        return "Invalid form data supplied", 400

    print(HUGGING_API)
    model = Model(HUGGING_API, prompt=prompt)
    response = model.generate_image()
    if response is None:
        return render_template("error.html")
    return render_template("result.html", image=response, prompt=prompt)

@app.route('/gallery-image/<img_name>', methods=['GET'])
def gallery_image(img_name):
    try:
        with open(f"app/frontend/assets/img/{img_name}.png", "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        return render_template("result.html", image=img_data, prompt="From Gallery")
    except Exception as e:
        print(e)
        return render_template("error.html")

@app.route('/random-prompt', methods=['GET'])
def random_prompt():
    selected_model = request.args.get('model')
    prompt = generate_random_prompt(selected_model)
    return jsonify({'prompt': prompt})

@app.route('/addToCart', methods=['POST'])
def addToCart():
    image_base64 = request.form['imageBase64']
    selectedSize = request.form['selectedSize']
    selectedColor = request.form['selectedColor']

    print(selectedSize, selectedColor)

    return render_template('cart.html', image=image_base64, size=selectedSize, color=selectedColor)