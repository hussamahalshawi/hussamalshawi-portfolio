import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = int(os.getenv('MONGO_PORT'))
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_PATH = os.path.join(BASE_DIR, 'App', 'static', 'images')
    # MONGO_URI = {
    #     'host': os.getenv('MONGO_URI')
    # }