import io
import os

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


@app.route('/model', methods=['POST'])
def model():
    try:
        prompt = request.form['prompt']
    except KeyError:
        return "Invalid form data supplied", 400

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

    return render_template("result.html", image=base64_image)
