import io
import os
import time

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

    time.sleep(2)
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code != 200:
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
