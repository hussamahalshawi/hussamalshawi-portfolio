import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = int(os.getenv('MONGO_PORT'))
    # MONGO_URI = {
    #     'host': os.getenv('MONGO_URI')
    # }