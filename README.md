# Weather Monitoring System

## Overview

The Weather Monitoring System is a Flask-based web application that provides real-time weather information for major Indian cities. It offers features such as current weather display, daily summaries, temperature trend visualization, and customizable weather alerts.

## Features

- **Real-time Weather Data**: Fetches and displays current weather information for selected Indian cities.
- **Daily Weather Summaries**: Provides a summary of weather conditions for the past 7 days.
- **Temperature Trend Visualization**: Displays a graph of temperature trends over the last 24 hours.
- **Customizable Alerts**: Allows users to set temperature thresholds for weather alerts.
- **User Preferences**: Supports both Celsius and Fahrenheit temperature units based on user preference.
- **Responsive Design**: Built with a mobile-first approach, ensuring a seamless experience across devices.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Data Visualization**: Plotly
- **Task Scheduling**: APScheduler
- **Email Alerts**: Flask-Mail
- **Weather Data**: OpenWeatherMap API

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/tejask2567/Weather-Monitoring-system.git
   cd Weather-Monitoring-system
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY='your_secret_key'
   OPENWEATHER_API_KEY='your_openweathermap_api_key'
   DATABASE_URL='sqlite:///weather.db'
   MAIL_USERNAME='your_email@gmail.com'
   MAIL_PASSWORD'=your_email_password'
   ALERT_EMAIL='recipient@example.com'
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   or
   python app.py
   ```

7. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. **Select a City**: Click on a city button to view its current weather and daily summary.
2. **Change Temperature Unit**: Toggle between Celsius and Fahrenheit using the temperature preference buttons.
3. **View Temperature Trend**: The temperature trend graph updates automatically when you select a city.
4. **Configure Alerts**: Set the maximum temperature threshold and the number of consecutive alerts in the Alert Configuration section.

## Contributing

Contributions to the Weather Monitoring System are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/weather-monitoring-system](https://github.com/yourusername/weather-monitoring-system)

## Acknowledgements

- [OpenWeatherMap API](https://openweathermap.org/api)
- [Flask](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Plotly](https://plotly.com/)
