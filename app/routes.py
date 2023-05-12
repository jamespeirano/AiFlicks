import io
import os
import time

import requests
from PIL import Image
from flask import render_template, request, Flask, jsonify
from dotenv import load_dotenv
import base64
import httpx
import stripe
import asyncio
from flask import Flask, request, jsonify
import stripe
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

        options = {k: v for k, v in attributes.items() if k is not False}

        if len(options) == 0:
            options = {"photorealistic": True}

        prompt = f"{pre_prompt} {prompt}. {post_prompt} {', '.join(options.values())}."

    except KeyError:
        return "Invalid form data supplied", 400

    response = asyncio.run(fetch_response(API_URL, headers=headers, json={"inputs": prompt}))
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

    return render_template("result.html", image=base64_image, prompt=prompt)

async def fetch_response(url, headers, json):
    async with httpx.AsyncClient(timeout = 10.0) as client:
        response = await client.post(url, headers=headers, json=json)
    return response


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
        # Create a payment intent with the payment method and amount
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
