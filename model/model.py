import io
import os
import requests
import base64
from PIL import Image

__all__ = ["Model"]


headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_TOKEN')}"}

class Model:
    def __init__(self, selected_model, prompt, options):
        self.selected_model = selected_model
        self.prompt = prompt
        self.options = options

    def generate_prompt(self):
        """
        Generates the prompt from the options.
        """
        prompt = self.prompt
        for option in self.options:
            prompt += self.options[option]
        return prompt

    def generate_image(self):
        """
        Generates the image from the response.
        """
        self.prompt = self.generate_prompt()
        response = self.fetch_response()

        if response is None:
            return None
        if response.status_code != 200:
            return None

        try:
            image = Image.open(io.BytesIO(response.content))
            image_byte_data = io.BytesIO()
            image.save(image_byte_data, format='PNG')
            base_64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')
        except Exception:
            return None

        return base_64_image
    
    def fetch_response(self):
        """
        Fetches the response from the API.
        """
        try:
            response = requests.post(
                self.selected_model,
                headers=headers,
                json={
                    "inputs": self.prompt,
                    "options": {
                        "seed": -1,
                        "use_cache": False,
                        "wait_for_model": True,
                    }
                }
            )
        except requests.RequestException:
            response = None

        return response