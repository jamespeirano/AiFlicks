import secrets
from flask import Flask
import stripe
import os
from dotenv import load_dotenv

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = secrets.token_hex(16)

load_dotenv()

stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

# avoid circular import
from app import routes