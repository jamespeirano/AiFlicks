import io
import os
from PIL import Image
from flask import render_template, request, jsonify, flash, redirect, url_for, session
from dotenv import load_dotenv
import base64
import httpx
from httpx import Timeout, RequestError
import stripe
import requests

import uuid

# import send_email below that's in the same directory
from app.send_email import send_email

from app import app

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

load_dotenv()

HUGGING_FACE_API_URLS = {
    'model-1': os.getenv('HUGGING_FACE_API_URL1'),
    'model-2': os.getenv('HUGGING_FACE_API_URL2'),
    'model-3': os.getenv('HUGGING_FACE_API_URL3'),
    'model-4': os.getenv('HUGGING_FACE_API_URL4'),
}

headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_TOKEN')}"}

cart_items = []
user_cart_items = []


@app.route('/')
def index():
    """
    Renders the index page which contains the form for the user to enter 
    a prompt and select the quality attributes they want to achieve in the image.
    """
    return render_template("index.html")


@app.route('/gallery')
def gallery():
    """
    Renders the gallery page which contains the images generated by the AI
    for the user to view and possibly purchase.
    """
    return render_template("gallery.html")


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """
    Adds the item to the cart.
    """
    data = request.get_json()
    name = data['name']
    price = data['price']
    size = data['size']
    image = data['image']
    cart_items.append({'image': image, 'name': name, 'price': price, 'size': size})
    # print(( 'image: ', image))
    # item = {'image': image, 'name': name, 'price': price, 'size': size}
    # cart_items.update({len(cart_items) + 1: item})
    return jsonify({'message': 'Item added to the cart'})


@app.route('/cart')
def cart():
    """
    Renders the cart page which contains the items added to the cart as well as the total price
    and a button to proceed to checkout.
    """
    # print(cart_items['name'], cart_items['price'], cart_items['size'])
    # print(cart_items)
    
    # for the user, display cart except the overlayImage (don't delete anything)
    

    for item in cart_items:
        user_cart_items.append({'name': item['name'], 'price': item['price'], 'size': item['size']})

    # for item in cart_items.values():
    #     user_cart_items.append({'name': item['name'], 'price': item['price'], 'size': item['size']})
    print(user_cart_items)
    return render_template("cart.html", cart_items=user_cart_items)


@app.route("/payment", methods=["POST"])
def payment():
    data = request.get_json()
    payment_method_id = data.get("paymentMethodId")
    amount = data.get("amount")

    try:
        # create a payment intent with the payment method and amount
        payment_intent = stripe.PaymentIntent.create(
            payment_method=payment_method_id,
            amount=amount,
            currency="usd",
            confirmation_method="manual",
            confirm=True,
        )
        if payment_intent.status == "succeeded":
            return jsonify({"success": True})

    except stripe.error.CardError as e:
        return jsonify({"success": False, "message": e.user_message})

    return jsonify({"success": False, "message": "Payment failed"})


@app.route('/model', methods=['GET', 'POST'])
async def model():
    pre_prompt = "Create a highly detailed and visually stunning 8K image featuring:"
    post_prompt = "Ensure that the image achieves the following quality attributes:"

    try:

        selected_model = request.form.get('selected-model')
        HUGGING_API = HUGGING_FACE_API_URLS.get(selected_model)

        prompt = request.form['prompt']
        photorealistic = request.form.get('photorealistic', False)
        semantic = request.form.get('semantic', False)
        coherence = request.form.get('coherence', False)
        novelty = request.form.get('novelty', False)

        attributes = {
            photorealistic: "Emphasize a high level of realism in the image, capturing intricate details, accurate lighting, and lifelike textures",
            semantic: "Ensure that the image accurately represents the intended meaning and context of the subject and the chosen environment",
            coherence: "Maintain a logical and coherent composition, ensuring that the elements within the image seamlessly blend together to create a visually harmonious scene",
            novelty: "Aim for a unique and original depiction, showcasing a fresh and distinctive perspective"
        }

        options = {k: v for k, v in attributes.items() if k is not False}

        if len(options) == 0:
            options = {"photorealistic": True}

        # prompt = f"{pre_prompt} {prompt}. {post_prompt} {', '.join(options.values())}."

    except KeyError:
        return "Invalid form data supplied", 400


    print(HUGGING_API)

    response = await fetch_response(HUGGING_API, headers=headers, json={
    "inputs": prompt,
    "options": {
        "seed": -1,
        "use_cache": False,
        "wait_for_model": True,
        "negative_prompt": [
            "(deformed iris)",
            "(deformed pupils)",
            "semi-realistic",
            "cgi",
            "3d",
            "render",
            "sketch",
            "cartoon",
            "drawing",
            "anime:1.4",
            "mutated hands and fingers:1.4",
            "deformed",
            "distorted",
            "disfigured:1.3",
            "poorly drawn",
            "bad anatomy",
            "wrong anatomy",
            "extra limb",
            "missing limb",
            "floating limbs",
            "disconnected limbs",
            "mutation",
            "mutated",
            "ugly",
            "disgusting",
            "amputation"
            ]
        }
    })

    if response is None:
        return render_template("error.html")
    if response.status_code != 200:
        return "Failed to fetch response from the API", 500

    try:
        image = Image.open(io.BytesIO(response.content))
    except Exception:
        return "Failed to process image response from the API", 500

    image_byte_data = io.BytesIO()
    try:
        image.save(image_byte_data, format='PNG')
    except Exception:
        return "Failed to save image data", 500

    base64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')
    image_id = str(uuid.uuid4())

    return render_template("result.html", image=base64_image, image_id=image_id, prompt=prompt)


async def fetch_response(url, headers, json):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=json, timeout=Timeout(20))
        except RequestError:
            response = None
    return response

@app.route('/random-prompt')
def random_prompt():
    text = "Describe a surreal and abstract image that could be generated by an advanced AI; limit your prompt to max 75 words."
    random_prompt = chat_gpt(text)
    return jsonify({'prompt': random_prompt})

def chat_gpt(prompt, model="gpt-3.5-turbo"):
    url = os.getenv("RAPID_OPENAI_API_URL")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPID_OPENAI_API_HOST")
    }
    response = requests.post(url, json=payload, headers=headers)

    try:
        choices = response.json()['choices']
        if choices:
            message_content = choices[0]['message']['content']
            return message_content
        else:
            raise KeyError("'choices' key is missing or empty in the response")
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        return ""

@app.route('/email_user', methods=['POST'])
def email_user():
    name = request.form.get('card_holder_name', False)
    receiver_email = request.form.get('card_holder_email', False)
    address = request.form.get('card_holder_address', False)
    phone = request.form.get('card_holder_phone', False)


    send_email(
        subject="New order placed",
        name=name,
        receiver_email="jnestleme@gmail.com",
        address=address,
        phone=phone,
        invoice_no="INV-21-12-009",
        amount="5",
        toCustomer=False,
        cartItems=cart_items
    )

    send_email(
        subject="New order placed",
        name=name,
        receiver_email=receiver_email,
        address=address,
        phone=phone,
        invoice_no="INV-21-12-009",
        amount="5",
        toCustomer=True,
        cartItems=user_cart_items
    )

    flash('Email sent successfully', 'success')
    # return back to index.html
    return redirect(url_for('index'))