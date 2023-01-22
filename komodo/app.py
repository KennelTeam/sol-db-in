from flask import Flask
from dotenv import load_dotenv
import os


app = Flask(__name__)

env_path = 'dev.env' if app.debug else 'prod.env'
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    raise FileNotFoundError('Environment file not found')
