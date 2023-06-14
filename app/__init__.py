import os
import secrets
from datetime import datetime, timedelta
from flask import Flask
from flask_session import Session
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, template_folder='frontend', static_folder='frontend/assets')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '../flask_session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
Session(app)

def cleanup_sessions(session_folder, expiration_time):
    now = datetime.now()

    for filename in os.listdir(session_folder):
        file_path = os.path.join(session_folder, filename)
        if os.path.getmtime(file_path) < (now - timedelta(seconds=expiration_time)).timestamp():
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(lambda: cleanup_sessions(app.config['SESSION_FILE_DIR'], 1*60), 'interval', minutes=1)

# avoid circular import
from app import routes