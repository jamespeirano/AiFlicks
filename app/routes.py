import os
import base64
import time
from flask import render_template, request, jsonify, url_for, redirect, session, abort, current_app
from utils import generate_random_prompt, generate_negative_prompt, send_email, Tshirt, Hoodie
from model import Model
from app import app
import stripe


HUGGING_FACE_API_URLS = {
    'stable-diffusion': os.environ.get('HUGGING_FACE_API_URL1'),
    'realistic-vision': os.environ.get('HUGGING_FACE_API_URL2'),
    'nitro-diffusion': os.environ.get('HUGGING_FACE_API_URL3'),
    'dreamlike-anime': os.environ.get('HUGGING_FACE_API_URL4'),
}

@app.route('/')
def index():
    session.permanent = False
    return render_template("index.html")


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


@app.route('/cart')
def cart():
    cart = session.get('cart', [])

    if not cart:
        return render_template('cart.html', cart_items=cart, subtotal=0)
    
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart_items=cart, subtotal=subtotal)


@app.route('/model', methods=['POST'])
def model():
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

    return generate_image_and_render(HUGGING_API, selected_model, prompt, negative_prompt)


def generate_image_and_render(HUGGING_API, selected_model, prompt, negative_prompt, retry_count=0):
    model = Model(HUGGING_API, prompt=prompt, negative_prompt=negative_prompt)

    print("Prompt: ", prompt)
    print("Negative Prompt: ", negative_prompt)
    print("Model: ", selected_model)
    print("Hugging Face API: ", HUGGING_API)

    try:
        start = time.time()
        response = model.generate_image()
        print(f"Time taken: {time.time() - start} seconds")
        if response == "timeout" and retry_count < 5:  # Limit retries to avoid infinite recursion
            print('retrying...')
            return generate_image_and_render(HUGGING_API, selected_model, prompt, negative_prompt, retry_count + 1)
    except Exception as e:
        return render_template("error.html", error=str(e))

    if not response or response == "timeout":
        return render_template("error.html", error="No image generated or timeout after retries")
    return render_template("result.html", image=response, prompt=prompt)


@app.route('/gallery-image/<img_name>', methods=['GET'])
def gallery_image(img_name):
    try:
        file_path = f"app/frontend/assets/img/{img_name}"
        with open(file_path, "rb") as img_file:
            image = base64.b64encode(img_file.read()).decode('utf-8')
        return render_template("result.html", image=image, prompt="Gallery Image")
    except Exception as e:
        print(f"Error serving image: {e}")
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
    teeMillApiKey = "8F7VouCxpe4xUx1icErBNIrJiXvqpnRS7tUWFvi7"
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

    # Set the options
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(teeMillApiKey)
    }

    data = {
        'image_url': "https://www.seiu1000.org/sites/main/files/main-images/camera_lense_0.jpeg",
        'item_code': 'RNA1',
        'name': 'Hello World',
        'colours': 'White,Black',
        'description': 'Check out this awemand.',
        'price': 20.00
    }

    # Send the API request
    response = requests.post('https://teemill.com/omnis/v3/product/create', headers=headers, data=json.dumps(data))

    from flask import redirect

    # ...

    # Check the response
    if response.status_code == 200:
        response_data = response.json()
        # Redirect to the new URL
        return redirect(response_data['url'])
    else:
        print('Error:', response.status_code)
        print('Message:', response.text)  # Add this line
        return abort(500, "Error contacting API")

    # cart = session.get('cart', [])
    # cart.append(product.to_dict())
    # session['cart'] = cart
    # return redirect(url_for('cart'))



