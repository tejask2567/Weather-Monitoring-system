from flask import Flask, render_template, jsonify, request
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import plotly.express as px
from datetime import datetime
from models import db, WeatherData, DailySummary, AlertConfig,UserPreference
from weather_service import WeatherService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
mail = Mail(app)

with app.app_context():
    db.create_all()
    weather_service = WeatherService(app)
    
    # Fetch initial data for all cities
    try:
        logger.info("Fetching initial weather data...")
        weather_service.fetch_weather_data()
        logger.info("Initial weather data fetched successfully")
    except Exception as e:
        logger.error(f"Error fetching initial weather data: {str(e)}")

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=weather_service.fetch_weather_data,
    trigger="interval",
    seconds=app.config['WEATHER_UPDATE_INTERVAL']
)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current-weather')
def current_weather():
    try:
        city = request.args.get('city', 'Delhi')
        user_id = request.remote_addr
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        unit = preference.temperature_unit if preference else 'C'
        
        data = WeatherData.query.filter_by(city=city).order_by(WeatherData.timestamp.desc()).first()
        
        if not data:
            weather_service.fetch_weather_data()
            data = WeatherData.query.filter_by(city=city).order_by(WeatherData.timestamp.desc()).first()
            
            if not data:
                return jsonify({'error': 'No data available'}), 404
            
        return jsonify({
            'temperature': float(weather_service.convert_temperature(data.temperature, unit)),
            'feels_like': float(weather_service.convert_temperature(data.feels_like, unit)),
            'condition': data.main_condition,
            'timestamp': data.timestamp.isoformat(),
            'unit': unit
        })
    except Exception as e:
        logger.error(f"Error in current_weather: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/daily-summary')
def daily_summary():
    try:
        city = request.args.get('city', 'Delhi')
        summaries = DailySummary.query.filter_by(city=city).order_by(DailySummary.date.desc()).limit(7).all()
        
        return jsonify([{
            'date': s.date.isoformat(),
            'avg_temp': float(s.avg_temp),
            'max_temp': float(s.max_temp),
            'min_temp': float(s.min_temp),
            'dominant_condition': s.dominant_condition
        } for s in summaries])
    except Exception as e:
        logger.error(f"Error in daily_summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/update-alert-config', methods=['POST'])
def update_alert_config():
    try:
        data = request.json
        config = AlertConfig.query.filter_by(city=data['city']).first()
        if not config:
            config = AlertConfig(city=data['city'])
        
        config.max_temp_threshold = data['max_temp_threshold']
        config.consecutive_alerts = data['consecutive_alerts']
        
        db.session.add(config)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error in update_alert_config: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/visualization')
def visualization():
    try:
        city = request.args.get('city', 'Delhi')
        data = WeatherData.query.filter_by(city=city).order_by(WeatherData.timestamp.desc()).limit(24).all()
        
        if not data:
            return jsonify({'error': 'No data available'}), 404
            
        df = pd.DataFrame([{
            'timestamp': d.timestamp,
            'temperature': float(d.temperature),
            'condition': d.main_condition
        } for d in data])
        
        fig = px.line(df, x='timestamp', y='temperature', title=f'Temperature Trend - {city}')
        return jsonify(fig.to_json())
    except Exception as e:
        logger.error(f"Error in visualization: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/user-preference', methods=['GET'])
def get_user_preference():
    user_id = request.remote_addr  # Using IP as user identifier
    preference = UserPreference.query.filter_by(user_id=user_id).first()
    if not preference:
        preference = UserPreference(user_id=user_id)
        db.session.add(preference)
        db.session.commit()
    return jsonify({
        'temperature_unit': preference.temperature_unit
    })

@app.route('/api/user-preference', methods=['POST'])
def update_user_preference():
    try:
        user_id = request.remote_addr
        data = request.json
        unit = data.get('temperature_unit', 'C')
        
        if unit not in ['C', 'F']:
            return jsonify({'error': 'Invalid temperature unit'}), 400
            
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        if not preference:
            preference = UserPreference(user_id=user_id, temperature_unit=unit)
        else:
            preference.temperature_unit = unit
            
        db.session.add(preference)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error updating user preference: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)