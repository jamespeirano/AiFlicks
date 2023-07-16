import io
import os
import base64
import requests
from requests.exceptions import Timeout
from PIL import Image

__all__ = ["Model", "ModelError"]

headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_TOKEN')}"}
TIMEOUT = 40

class ModelError(Exception):
    pass

class Model:
    def __init__(self, selected_model, prompt, negative_prompt):
        self.selected_model = selected_model
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.params = {
            "inputs": self.prompt,
            "parameters": {
                "negative_prompt": self.negative_prompt,
                "guidance_scale": 7.5,
                "num_inference_steps": 25,
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
        self.retry_count = 0

    def generate(self):
        try:
            base_64_image = self._generate_image()
            return base_64_image
        except Timeout:
            raise ModelError('Timeout')

    def _generate_image(self):
        try:
            response_content = self.fetch_response()
            if not response_content:
                raise ModelError("No content in the response")
        
            image = Image.open(io.BytesIO(response_content))
            image_byte_data = io.BytesIO()
            image.save(image_byte_data, format='PNG')
            base_64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')
            return base_64_image
        except Exception as e:
            print(f"Failed to generate image: {e}")
            raise ModelError(f"Failed to generate image: {e}") from e

    def fetch_response(self):
        try:
            response = requests.post(
                self.selected_model,
                headers=headers,
                json=self.params,
                timeout=TIMEOUT
            )
        except Exception as e:
            print(f"RequestException: {e}")
            raise ModelError(f"RequestException: {e}") from e

        if response.status_code != 200:
            print(f"Failed to generate image: {response.status_code}")
            print(f"Response text: {response.text}")
            if response.status_code == 400:
                raise ModelError("Bad Request - there might be something wrong with your parameters.")
            elif response.status_code == 401:
                raise ModelError("Unauthorized - there might be something wrong with your authentication.")
            else:
                raise ModelError(f"Unexpected status code: {response.status_code}")

        return response.content