# config.py
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///weather.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    WEATHER_UPDATE_INTERVAL = 300  # 5 minutes in seconds
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL')