import io
import os
import aiohttp
import base64
from PIL import Image
import asyncio
from aiohttp import ClientSession, ClientTimeout

__all__ = ["Model"]

headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_TOKEN')}"}
TIMEOUT = 28

class ModelException(Exception):
    pass

class TimeoutException(Exception):
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

    async def generate_image(self):
        try:
            response_content = await self.fetch_response()
            if not response_content:
                raise ModelException("No content in the response")
            
            image = Image.open(io.BytesIO(response_content))
            image_byte_data = io.BytesIO()
            image.save(image_byte_data, format='PNG')
            base_64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')
            return base_64_image
        except Exception as e:
            print(f"Failed to generate image: {e}")
            raise ModelException(f"Failed to generate image: {e}") from e

    async def fetch_response(self, retry_count=0):
        timeout = ClientTimeout(total=28)
        async with ClientSession(timeout=timeout) as session:
            try:
                async with session.post(
                self.selected_model,
                headers=headers,
                json=self.params,
                timeout=28  # Setting a low value for testing
            ) as response:
                    if response.status != 200:
                        print(f"Failed to generate image: {response.status}")
                        if response.status == 400:
                            raise ModelException("Bad Request - there might be something wrong with your parameters.")
                        elif response.status == 401:
                            raise ModelException("Unauthorized - there might be something wrong with your authentication.")
                        else:
                            raise ModelException(f"Unexpected status code: {response.status}")
                    
                    return await response.read()
            except aiohttp.ClientError as e:
                print(f"RequestException: {e}")
                raise ModelException(f"RequestException: {e}") from e
            except asyncio.TimeoutError as e:
                if retry_count < 5:
                    print(f"TimeoutException: {e}. Retrying attempt {retry_count + 1}")
                    return await self.fetch_response(retry_count + 1)
                else:
                    print(f"TimeoutException: {e}")
                    raise TimeoutException("Timeout - the API call took too long") from e
