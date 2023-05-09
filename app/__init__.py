import secrets
from flask import Flask

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = secrets.token_hex(16)

# avoid circular import
from app import routes