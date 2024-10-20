# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    main_condition = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class DailySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    dominant_condition = db.Column(db.String(50), nullable=False)

class AlertConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    max_temp_threshold = db.Column(db.Float, nullable=False)
    consecutive_alerts = db.Column(db.Integer, default=2)


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)  # Could be IP or session ID
    temperature_unit = db.Column(db.String(1), nullable=False, default='C')  # 'C' for Celsius, 'F' for Fahrenheit
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)