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
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart_items=cart, subtotal=subtotal)

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
    selectedProduct = request.form['selectedProduct']
    quantity = int(request.form.get('quantity', 1))  # Get the quantity from the request, convert it to int, or use 1 as a default

    if selectedProduct == 'tshirt':
        selectedSize = request.form['tshirtSelectedSize']
        selectedColor = request.form['tshirtSelectedColor']
        product = Tshirt("Your tshirt design", selectedSize, selectedColor, image_base64, 20.00, quantity)
    elif selectedProduct == 'hoodie':
        selectedSize = request.form['hoodieSelectedSize']
        selectedColor = request.form['hoodieSelectedColor']
        product = Hoodie("Your hoodie design", selectedSize, selectedColor, image_base64, 40.00, quantity)    

    # Get the current cart from the session (or an empty list if there's no 'cart' key)
    cart = session.get('cart', [])
    # Append the dictionary representation of the new item to the cart
    cart.append(product.to_dict())
    # Store the updated cart back in the session
    session['cart'] = cart

    return redirect(url_for('cart'))


import stripe
from flask import jsonify

stripe.api_key = "sk_test_51Mpg4OHhtpW6f5otjU9sxetInnUYfgcZaXhOuXj9paTTt1fx9MkhVjbzYu8gziqWYt2cDCkBrGE1QfgOgaqpOcTe002PWJ0OIH"

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # Get the cart from the session
    cart = session.get('cart', [])

    # Prepare line items for Stripe
    line_items = []
    for product in cart:
        line_item = {
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(float(product['price']) * 100),  # convert to cents
                'product_data': {
                    'name': product['name'],
                },
            },
            'quantity': product['quantity'],
        }
        line_items.append(line_item)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cancel', _external=True),
        )
        return jsonify(id=checkout_session.id)
    except Exception as e:
        return jsonify(error=str(e)), 403



@app.route('/update-cart-quantity', methods=['POST'])
def update_cart_quantity():
    data = request.get_json()
    product_id = data.get('productId', None)
    new_quantity = int(data.get('newQuantity', 1))
    cart = session.get('cart', [])

    new_total = 0.0
    subtotal = 0.0
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = new_quantity
            new_total = item['price'] * new_quantity  # New total for this item
        subtotal += item['price'] * item['quantity']  # Subtotal for all items

    session['cart'] = cart

    return jsonify({"success": True, "newTotal": new_total, "subtotal": subtotal}), 200  # Return new total for this item and subtotal