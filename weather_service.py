import requests
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy import func
from flask_mail import Message
from models import WeatherData, DailySummary, AlertConfig, db
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self, app):
        self.app = app
        self.api_key = app.config['OPENWEATHER_API_KEY']
        self.mail = app.extensions['mail']
        self.alert_email = app.config['ALERT_EMAIL']
        self.cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

    def kelvin_to_celsius(self, kelvin):
        return kelvin - 273.15

    def fetch_weather_data(self):
        with self.app.app_context():
            for city in self.cities:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={self.api_key}"
                try:
                    logger.info(f"Fetching weather data for {city}")
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    data = response.json()
                    weather_data = WeatherData(
                        city=city,
                        temperature=self.kelvin_to_celsius(data['main']['temp']),
                        feels_like=self.kelvin_to_celsius(data['main']['feels_like']),
                        main_condition=data['weather'][0]['main'],
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(weather_data)
                    db.session.commit()
                    
                    self.check_alerts(city, weather_data.temperature)
                    self.update_daily_summary(city)
                    logger.info(f"Successfully updated weather data for {city}")
                except Exception as e:
                    logger.error(f"Error fetching weather data for {city}: {str(e)}")

    def update_daily_summary(self, city):
        today = datetime.utcnow().date()
        data = WeatherData.query.filter(
            WeatherData.city == city,
            func.date(WeatherData.timestamp) == today
        ).all()

        if data:
            temperatures = [d.temperature for d in data]
            conditions = [d.main_condition for d in data]
            dominant_condition = Counter(conditions).most_common(1)[0][0]

            summary = DailySummary.query.filter_by(city=city, date=today).first()
            if not summary:
                summary = DailySummary(city=city, date=today)

            summary.avg_temp = sum(temperatures) / len(temperatures)
            summary.max_temp = max(temperatures)
            summary.min_temp = min(temperatures)
            summary.dominant_condition = dominant_condition

            db.session.add(summary)
            db.session.commit()
            logger.info(f"Updated daily summary for {city}")

    def check_alerts(self, city, temperature):
        alert_config = AlertConfig.query.filter_by(city=city).first()
        if not alert_config:
            return

        recent_readings = WeatherData.query.filter(
            WeatherData.city == city,
            WeatherData.timestamp >= datetime.utcnow() - timedelta(minutes=15)
        ).all()

        if len(recent_readings) >= alert_config.consecutive_alerts:
            if all(r.temperature > alert_config.max_temp_threshold for r in recent_readings[-alert_config.consecutive_alerts:]):
                self.send_alert_email(city, temperature)

    def send_alert_email(self, city, temperature):
        if self.alert_email:
            try:
                msg = Message(
                    f"Weather Alert for {city}",
                    sender="weather-monitor@example.com",
                    recipients=[self.alert_email]
                )
                msg.body = f"Temperature in {city} has exceeded threshold: {temperature:.1f}°C"
                self.mail.send(msg)
                logger.info(f"Sent alert email for {city}")
            except Exception as e:
                logger.error(f"Error sending alert email: {str(e)}")
    def convert_temperature(self, kelvin_temp, unit='C'):
        if unit == 'C':
            return kelvin_temp - 273.15
        elif unit == 'F':
            return (kelvin_temp - 273.15) * 9/5 + 32
        return kelvin_temp

    def fetch_weather_data(self):
        with self.app.app_context():
            for city in self.cities:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={self.api_key}"
                try:
                    logger.info(f"Fetching weather data for {city}")
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    data = response.json()
                    # Store raw Kelvin values in database
                    weather_data = WeatherData(
                        city=city,
                        temperature=data['main']['temp'],  # Store raw Kelvin value
                        feels_like=data['main']['feels_like'],  # Store raw Kelvin value
                        main_condition=data['weather'][0]['main'],
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(weather_data)
                    db.session.commit()
                    
                    self.check_alerts(city, self.convert_temperature(weather_data.temperature))
                    self.update_daily_summary(city)
                    logger.info(f"Successfully updated weather data for {city}")
                except Exception as e:
                    logger.error(f"Error fetching weather data for {city}: {str(e)}")