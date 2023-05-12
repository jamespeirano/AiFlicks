import io
import os
import time
import jsonify
import stripe

import requests
from PIL import Image
from flask import render_template, request
from dotenv import load_dotenv
import base64

from app import app

load_dotenv()
API_URL = os.getenv('API_URL')
headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}

@app.route('/')
def index():
    """ Default webpage."""
    return render_template("index.html")


@app.route('/model', methods=['GET', 'POST'])
def model():
    pre_prompt = "Create a highly detailed and visually stunning 8K image featuring:"
    post_prompt = "Ensure that the image achieves the following quality attributes:"

    try:
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

        # filter out the attributes that are not selected
        options = {k: v for k, v in attributes.items() if k is not False}

        # if no attributes are selected, use the default
        if len(options) == 0:
            options = {"photorealistic": True}

        prompt = f"{pre_prompt} {prompt}. {post_prompt} {', '.join(options.values())}."

    except KeyError:
        return "Invalid form data supplied", 400

    # retry API call with exponential backoff
    try:
        response = make_api_call_with_retry(API_URL, headers, {"inputs": prompt})
    except requests.exceptions.RequestException:
        return "Failed to fetch response from the API", 500

    try:
        image = Image.open(io.BytesIO(response.content))
    except Exception:
        return "Failed to process image response from the API", 500

    # encode the image as base64
    image_byte_data = io.BytesIO()
    try:
        image.save(image_byte_data, format='PNG')
    except Exception:
        return "Failed to save image data", 500
    
    # convert the bytes to string
    base64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')

    return render_template("result.html", image=base64_image, prompt=prompt)


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

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


# replace with James' async API call

def make_api_call_with_retry(url, headers, data, retries=3):
    backoff = 1
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(backoff)
                # exponential backoff
                backoff *= 2
            else:
                # no more retries, raise exception
                raise