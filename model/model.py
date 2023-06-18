import io
import os
import requests
import base64
from PIL import Image

__all__ = ["Model"]

headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_TOKEN')}"}


class ModelException(Exception):
    pass


class Model:
    def __init__(self, selected_model, prompt, negative_prompt):
        self.selected_model = selected_model
        self.prompt = prompt
        self.negative_prompt = negative_prompt

    def generate_image(self):
        try:
            response_content = self.fetch_response()
            image = Image.open(io.BytesIO(response_content))
            image_byte_data = io.BytesIO()
            image.save(image_byte_data, format='PNG')
            base_64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"Failed to generate image: {e}")
            raise ModelException(f"Failed to generate image: {e}") from e
        return base_64_image

    def fetch_response(self):
        try:
            response = requests.post(
                self.selected_model,
                headers=headers,
                json={
                    "inputs": self.prompt,
                    "parameters": {
                        "negative_prompt": self.negative_prompt,
                        "guidance_scale": 7.5,
                        "num_inference_steps": 75,
                        "height": 512,
                        "width": 512,
                    },
                    "options": {
                        "seed": 42,
                        "temperature": 0.5,
                        "use_cache": False,
                        "wait_for_model": True
                    }
                }
            )
        except requests.RequestException as e:
            print(f"RequestException: {e}")
            raise ModelException(f"RequestException: {e}") from e

        if response.status_code != 200:
            print(f"Failed to generate image: {response.status_code}")
            print(f"Response text: {response.text}")
            if response.status_code == 400:
                raise ModelException("Bad Request - there might be something wrong with your parameters.")
            elif response.status_code == 401:
                raise ModelException("Unauthorized - there might be something wrong with your authentication.")
            else:
                raise ModelException(f"Unexpected status code: {response.status_code}")

        return response.content