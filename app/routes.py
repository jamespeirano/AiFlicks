import base64
from flask import render_template, request, jsonify, url_for, redirect, session, abort
from dotenv import dotenv_values
from utils import generate_random_prompt, Tshirt, Hoodie
from model import Model
from app import app
import stripe

# Loading environment variables
config = dotenv_values(".env")

HUGGING_FACE_API_URLS = {
    'stable-diffusion': config['HUGGING_FACE_API_URL1'],
    'realistic-vision': config['HUGGING_FACE_API_URL2'],
    'nitro-diffusion': config['HUGGING_FACE_API_URL3'],
    'dreamlike-anime': config['HUGGING_FACE_API_URL4'],
}

stripe.api_key = config['STRIPE_SECRET_KEY']

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
    selected_model = request.form.get('model_input')
    if not selected_model:
        return abort(400, "Model not selected")
        
    HUGGING_API = HUGGING_FACE_API_URLS.get(selected_model)
    prompt = request.form.get('prompt')

    if not HUGGING_API or not prompt:
        return abort(400, "Invalid form data supplied")

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
    image_base64 = request.form.get('imageBase64')
    selectedProduct = request.form.get('selectedProduct')
    quantity = int(request.form.get('quantity', 1)) 

    # Dictionary to determine product type
    products = {
        'tshirt': Tshirt,
        'hoodie': Hoodie
    }

    if selectedProduct in products:
        selectedSize = request.form.get(f'{selectedProduct}SelectedSize')
        selectedColor = request.form.get(f'{selectedProduct}SelectedColor')
        price = 20.00 if selectedProduct == 'tshirt' else 40.00
        product = products[selectedProduct]("Your {} design".format(selectedProduct), selectedSize, selectedColor, image_base64, price, quantity)
    else:
        return abort(400, "Invalid product type")

    cart = session.get('cart', [])
    cart.append(product.to_dict())
    session['cart'] = cart

    return redirect(url_for('cart'))

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    cart = session.get('cart', [])
    if not cart:
        return abort(400, "Cart is empty")

    # Use list comprehension for generating line items
    line_items = [{
        'price_data': {
            'currency': 'usd',
            'unit_amount': int(float(product['price']) * 100),
            'product_data': {
                'name': product['name'],
            },
        },
        'quantity': product['quantity'],
    } for product in cart]

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
            new_total = item['price'] * new_quantity
        subtotal += item['price'] * item['quantity']

    session['cart'] = cart

    return jsonify({"success": True, "newTotal": new_total, "subtotal": subtotal}), 200