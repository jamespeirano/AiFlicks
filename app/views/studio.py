import os
import requests
import json
import gradio as gr
import io
import threading
import numpy as np
import cv2
from PIL import Image
from flask import Blueprint, render_template, g
from app.data import MODELS

studio_bp = Blueprint('studio', __name__, url_prefix='/studio')

hf_api_key = os.getenv('HUGGING_FACE_API_TOKEN')
ENDPOINT_URL = os.environ['STABLE_DIFFUSION_V15']

def get_completion(inputs, parameters=None):
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"
    }
    data = {"inputs": inputs}
    if parameters is not None:
        data.update({"parameters": parameters})
    response = requests.request("POST", ENDPOINT_URL, headers=headers, data=json.dumps(data))
    return response.content

def generate(prompt, negative_prompt, steps, guidance, width, height, enhance, upscale):
    params = {
        "negative_prompt": negative_prompt,
        "num_inference_steps": steps,
        "guidance_scale": guidance,
        "width": width,
        "height": height
    }
    output = get_completion(prompt, params)
    output = io.BytesIO(output)
    if enhance:
        output = enhance_image(output, strength=10)
    if upscale:
        output = upscale_image(output)
    pil_image = Image.open(output)
    return pil_image

def enhance_image(image, strength):
    cv_img = cv2.imdecode(np.frombuffer(image.getvalue(), np.uint8), -1)
    cv_img = cv2.detailEnhance(cv_img, sigma_s=strength, sigma_r=0.15)
    cv_img = cv2.edgePreservingFilter(cv_img, flags=1, sigma_s=64, sigma_r=0.2)  
    image = cv2.imencode('.png', cv_img)[1].tostring()
    result = io.BytesIO(image)
    return result

def upscale_image(image, scale_percent=150):
    image = cv2.imdecode(np.frombuffer(image.getvalue(), np.uint8), -1)
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_LINEAR)
    image = cv2.imencode('.png', image)[1].tostring()
    result = io.BytesIO(image)
    return result

# Define Gradio interface
def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Image Generation with Stable Diffusion")
        with gr.Row():
            prompt = gr.Textbox(label="Your prompt")
        with gr.Accordion("Advanced options", open=False):
            negative_prompt = gr.Textbox(label="Negative prompt")
            with gr.Row():
                with gr.Column():
                    steps = gr.Slider(label="Inference Steps", minimum=1, maximum=100, value=25)
                    guidance = gr.Slider(label="Guidance Scale", minimum=1, maximum=20, value=7)
                with gr.Column():
                    width = gr.Slider(label="Width", minimum=64, maximum=512, step=64, value=512)
                    height = gr.Slider(label="Height", minimum=64, maximum=512, step=64, value=512)
            
            enhance = gr.Checkbox(label="Enhance image")
            upscale = gr.Checkbox(label="Upscale image")
            
        with gr.Row():
            btn = gr.Button("Generate Image")
        output = gr.Image(label="Result", type="pil")
        btn.click(fn=generate, inputs=[prompt, negative_prompt, steps, guidance, width, height, enhance, upscale], outputs=[output])
    gr.close_all()
    return demo

@studio_bp.before_app_first_request
def initialize_gradio_interface():
    g.gradio_interface = {}

@studio_bp.route('/start_gradio', methods=['GET'])
def start_gradio():
    if not hasattr(g, 'gradio_interface'):
        g.gradio_interface = create_gradio_interface()
    demo_thread = threading.Thread(target=g.gradio_interface.launch, args=(True, os.getenv('PORT4')))
    demo_thread.start()
    return {"message": "Gradio app started"}

@studio_bp.route('/stop_gradio', methods=['GET'])
def stop_gradio():
    # Get the gradio interface and stop it
    gradio_interface = g.gradio_interface
    gradio_interface.close()
    return {"message": "Gradio app stopped"}

@studio_bp.route('/gradio', methods=['GET'])
def gradio():
    # Check if the Gradio interface is already running
    if not hasattr(g, 'gradio_interface') or not g.gradio_interface.is_alive():
        # If not, start it
        start_gradio()
    return render_template('gradio.html', models=MODELS)