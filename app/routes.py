import os
import base64
from flask import render_template, request, jsonify, url_for, redirect, session
from dotenv import load_dotenv
from utils import generate_random_prompt, Tshirt, Hoodie
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
    session.permanent = False
    return render_template("index.html")

@app.route('/models')
def models():
    return render_template('models.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

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
    selectedProduct = request.form['selectedProduct']

    if selectedProduct == 'tshirt':
        product = Tshirt("Your tshirt design", selectedSize, selectedColor, image_base64, 20.00)
    elif selectedProduct == 'hoodie':
        product = Hoodie("Your hoodie design", selectedSize, selectedColor, image_base64, 40.00)

    # Get the current cart from the session (or an empty list if there's no 'cart' key)
    cart = session.get('cart', [])
    # Append the dictionary representation of the new item to the cart
    cart.append(product.to_dict())
    # Store the updated cart back in the session
    session['cart'] = cart

    return redirect(url_for('cart'))