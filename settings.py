from configparser import ConfigParser
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

config = ConfigParser()
config.read(os.path.join(BASE_DIR, "config.ini"))

API_KEY=config.get('tweepy', 'API_KEY')
API_SECRET_KEY=config.get('tweepy', 'API_SECRET_KEY')

ACCESS_TOKEN = config.get('tweepy', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config.get('tweepy', 'ACCESS_TOKEN_SECRET')
