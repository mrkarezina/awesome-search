import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

config = ConfigParser()
config.read(os.path.join(BASE_DIR, "config.ini"))

HOST = config.get('redis', 'HOST')
PORT = config.get('redis', 'PORT')
REDIS_URL = f'redis://{HOST}:{PORT}/1'


API_KEY = config.get('tweepy', 'API_KEY')
API_SECRET_KEY = config.get('tweepy', 'API_SECRET_KEY')

ACCESS_TOKEN = config.get('tweepy', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config.get('tweepy', 'ACCESS_TOKEN_SECRET')
