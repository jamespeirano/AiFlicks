import os
import secrets
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

time_to_live = 24

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', default=secrets.token_hex(16))
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(BASE_DIR, '..', 'flask_session')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=time_to_live)

    # MongoDB configuration
    MONGODB_SETTINGS = {
        'db': 'your-db-name',
        'host': 'localhost',
        'port': 27017
    }