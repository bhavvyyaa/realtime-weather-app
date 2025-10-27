# Real-Time Weather App

A Streamlit-based weather application that displays current weather conditions and 5-day forecasts for any city using the OpenWeatherMap API.

## Features

- 🌡️ Current weather display (temperature, humidity, wind speed)
- 🌅 Sunrise and sunset times
- 📊 5-day weather forecast with interactive charts
- 🌦️ Dynamic weather icons (sunny, rainy, cloudy, etc.)
- 🔄 Toggle between Celsius and Fahrenheit
- 🔍 Search weather for any city worldwide

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd realtime-weather-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Key**
   - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
   - Copy `.env.example` to `.env`
   - Replace `your_api_key_here` with your actual API key

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter a city name in the search box
2. Toggle temperature units (Celsius/Fahrenheit) as needed
3. View current weather conditions including:
   - Temperature
   - Humidity
   - Wind speed
   - Weather description
   - Sunrise/Sunset times
4. Scroll down to see the 5-day forecast chart

## Sample Queries

Try searching for these cities:
- **New York** - View weather in the Big Apple
- **London** - Check conditions in the UK capital
- **Tokyo** - See weather in Japan
- **Sydney** - Explore weather down under
- **Paris** - Check the weather in the City of Light
- **Mumbai** - View weather in India's financial hub
- **Dubai** - See desert climate conditions
- **Singapore** - Check equatorial weather

## Project Structure

```
realtime-weather-app/
├── app.py                 # Main Streamlit application
├── weather_service.py     # OpenWeatherMap API integration
├── utils.py               # Helper functions (icons, conversions)
├── requirements.txt       # Project dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## Technologies Used

- **Streamlit** - Web application framework
- **OpenWeatherMap API** - Weather data provider
- **Requests** - HTTP library for API calls
- **Plotly** - Interactive charts for forecast visualization
- **Pandas** - Data manipulation for forecast data

## License

MIT License
