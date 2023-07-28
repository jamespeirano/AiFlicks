import os
import requests
import json
import gradio as gr
import base64
import io
import threading
from PIL import Image
from flask import Blueprint, render_template, g

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

def generate(prompt, negative_prompt, steps, guidance, width, height):
    params = {
        "negative_prompt": negative_prompt,
        "num_inference_steps": steps,
        "guidance_scale": guidance,
        "width": width,
        "height": height
    }
    output = get_completion(prompt, params)
    pil_image = Image.open(io.BytesIO(output))  # directly read image from raw data
    return pil_image

# Define Gradio interface
def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Image Generation with Stable Diffusion")
        with gr.Row():
            with gr.Column(scale=4):
                prompt = gr.Textbox(label="Your prompt")
            with gr.Column(scale=1, min_width=50):
                btn = gr.Button("Submit")
        with gr.Accordion("Advanced options", open=False):
            negative_prompt = gr.Textbox(label="Negative prompt")
            with gr.Row():
                with gr.Column():
                    steps = gr.Slider(label="Inference Steps", minimum=1, maximum=100, value=25)
                    guidance = gr.Slider(label="Guidance Scale", minimum=1, maximum=20, value=7)
                with gr.Column():
                    width = gr.Slider(label="Width", minimum=64, maximum=512, step=64, value=512)
                    height = gr.Slider(label="Height", minimum=64, maximum=512, step=64, value=512)
        output = gr.Image(label="Result", type="pil")  # Indicate the output is a PIL Image
        btn.click(fn=generate, inputs=[prompt, negative_prompt, steps, guidance, width, height], outputs=[output])
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
    return render_template('gradio.html')