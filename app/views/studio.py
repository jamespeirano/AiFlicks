import os
import io
import gradio as gr
import threading
import numpy as np
import cv2
import realesrgan
from PIL import Image
import base64
from flask import Blueprint, render_template, current_app, request
from app.api import Model, ModelError
from app.data import MODELS

studio_bp = Blueprint('studio', __name__, url_prefix='/studio')

ENDPOINT_URL = os.environ['STABLE_DIFFUSION_V15']

image_data_base64 = None
hfc_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hugging_face'))

def base64_to_np_array(base64_image):
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def np_array_to_base64(np_array):
    _, buffer = cv2.imencode('.png', np_array)
    return base64.b64encode(buffer).decode('utf-8')


async def generate(prompt, negative_prompt, steps, guidance, width, height):
    global image_data_base64
    model = Model(ENDPOINT_URL, prompt, negative_prompt, guidance, steps, height, width)
    try:
        base_64_image = await model.generate()
        image_data_base64 = base64_to_np_array(base_64_image)
        return image_data_base64
    except ModelError as e:
        return "Error generating image: " + str(e)
    except Exception as e:
        return "Error generating image: " + str(e)


def enhance_image(strength):
    global image_data_base64
    if image_data_base64 is None:
        return "Please generate an image first!"

    cv_img = cv2.detailEnhance(image_data_base64, sigma_s=strength, sigma_r=0.15)
    cv_img = cv2.edgePreservingFilter(cv_img, flags=1, sigma_s=64, sigma_r=0.2)
    image_data_base64 = cv_img
    return image_data_base64


def upscale_image(factor):
    global image_data_base64
    if image_data_base64 is None:
        return "Please generate an image first!"
    
    upscaler = realesrgan.RealESRGANer(scale=factor, model_path=os.path.join(hfc_directory, "RealESRGAN_x4plus.pth"))
    if factor == 1:
        return image_data_base64
    image = upscaler.upscale(image_data_base64, factor=factor)
    image_data_base64 = image
    return image_data_base64


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

        enhance_strength = gr.Slider(label="Enhancement Strength", minimum=1, maximum=20, step=1, value=10)
        upscale_factor = gr.Slider(label="Upscale Factor", minimum=2, maximum=4, step=1, value=2)

        with gr.Row():
            gen_btn = gr.Button("Generate Image")
            enh_btn = gr.Button("Enhance Image")
            ups_btn = gr.Button("Upscale Image")

        output = gr.Image(label="Result", type="numpy")

        gen_btn.click(fn=generate, inputs=[prompt, negative_prompt, steps, guidance, width, height], outputs=[output])
        enh_btn.click(fn=enhance_image, inputs=[enhance_strength], outputs=[output])
        ups_btn.click(fn=upscale_image, inputs=[upscale_factor], outputs=[output])

    gr.close_all()
    return demo


@studio_bp.before_app_first_request
def initialize_gradio_interface():
    current_app.gradio_data = {'interface': None, 'thread': None}


@studio_bp.route('/start_gradio', methods=['GET'])
def start_gradio():
    try:
        if 'interface' not in current_app.gradio_data or 'thread' not in current_app.gradio_data or (current_app.gradio_data['thread'] and not current_app.gradio_data['thread'].is_alive()):
            print("Attempting to start Gradio interface...")
            current_app.gradio_data['interface'] = create_gradio_interface()
            demo_thread = threading.Thread(target=current_app.gradio_data['interface'].launch, args=(True, "7860"))
            current_app.gradio_data['thread'] = demo_thread
            demo_thread.start()
        return {"message": "Gradio app started"}
    except Exception as e:
        print("Error while starting Gradio:", str(e))
        return {"message": "Error while starting Gradio: " + str(e)}, 500


@studio_bp.route('/stop_gradio', methods=['GET'])
def stop_gradio():
    try:
        if current_app.gradio_data.get('interface'):
            print("Attempting to stop Gradio interface...")
            current_app.gradio_data['interface'].close()
            current_app.gradio_data['interface'] = None

        if current_app.gradio_data.get('thread'):
            current_app.gradio_data['thread'].join()
            current_app.gradio_data['thread'] = None

        return {"message": "Gradio app stopped"}
    except Exception as e:
        print("Error while stopping Gradio:", str(e))
        return {"message": "Error while stopping Gradio: " + str(e)}, 500


@studio_bp.route('/gradio', methods=['GET'])
def gradio():
    print('gradio is called')
    if 'thread' not in current_app.gradio_data or (current_app.gradio_data['thread'] and not current_app.gradio_data['thread'].is_alive()):
        print('starting gradio')
        start_gradio()
    return render_template('gradio.html', models=MODELS)


@studio_bp.after_request
def cleanup_gradio(response):
    if request.path == '/studio/stop_gradio':
        stop_gradio()
    return response