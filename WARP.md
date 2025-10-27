# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

A Streamlit-based weather application that displays real-time weather conditions and 5-day forecasts using the OpenWeatherMap API. The app is built with Python and uses Plotly for interactive data visualization.

## Development Commands

### Setup
```bash
# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Copy .env.example to .env and add your OPENWEATHER_API_KEY
```

### Running the Application
```bash
# Start the Streamlit development server
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8501
```

### Testing
No automated test suite currently exists. Manual testing is performed by running the app and verifying functionality with different cities.

## Architecture

### Module Structure

**app.py** - Main Streamlit application
- Entry point and UI orchestration
- Handles user input, state management, and display rendering
- Uses `@st.cache_resource` to cache the WeatherService instance for performance
- Implements a two-column layout with sidebar for settings
- Creates interactive Plotly charts for temperature visualization

**weather_service.py** - API integration layer
- `WeatherService` class encapsulates all OpenWeatherMap API interactions
- Two main endpoints: `/weather` (current) and `/forecast` (5-day)
- Handles API key validation, HTTP requests, error handling, and response parsing
- Separates data fetching (`get_*`) from data parsing (`parse_*`) for testability
- Returns error dictionaries with `{"error": "message"}` format on failures

**utils.py** - Presentation helpers
- Pure functions for data transformation and formatting
- `get_weather_icon()`: Maps OpenWeatherMap condition codes (200-804) to emoji icons
- `format_timestamp()`: Converts Unix timestamps to readable times with timezone offsets
- `get_wind_direction()`: Converts degrees (0-360) to cardinal directions (N, NE, E, etc.)
- Temperature conversion utilities (though API handles unit conversion)

### Data Flow

1. User enters city → `app.py` captures input
2. `WeatherService.get_current_weather()` → Raw JSON from OpenWeatherMap API
3. `WeatherService.parse_current_weather()` → Normalized dict with simplified keys
4. `utils.py` functions → Format data for display (icons, timestamps, directions)
5. Streamlit renders → Weather cards, metrics, and interactive charts
6. Same flow repeats for forecast data with `get_forecast()` and `parse_forecast()`

### Key Design Patterns

- **Service Layer Pattern**: WeatherService abstracts API complexity from UI
- **Parser Functions**: Separate parsing logic allows for easier testing and error handling
- **Stateless Utilities**: All utils.py functions are pure (no side effects)
- **Error Propagation**: Errors bubble up as dicts with "error" key, handled at UI level
- **Caching**: Streamlit's `@st.cache_resource` prevents re-instantiation of WeatherService

## OpenWeatherMap API Notes

- **API Key**: Required, stored in `.env` as `OPENWEATHER_API_KEY`
- **Endpoints Used**:
  - `GET /weather` - Current weather for a city
  - `GET /forecast` - 5-day forecast in 3-hour intervals (40 data points)
- **Units Parameter**: 
  - `metric` (Celsius, m/s)
  - `imperial` (Fahrenheit, mph)
- **Weather Codes**: Standardized codes (200-804) map to conditions (thunderstorm, rain, clouds, etc.)
- **Rate Limits**: Free tier allows 60 calls/minute, 1,000,000 calls/month

## Environment Variables

- `OPENWEATHER_API_KEY` - Required for API authentication (get from https://openweathermap.org/api)

## Streamlit-Specific Behavior

- **Auto-rerun**: Streamlit reruns the entire script on any user interaction
- **Session State**: Not currently used, but available via `st.session_state` for persistence
- **Caching**: `@st.cache_resource` used for WeatherService to avoid re-initialization
- **Layout**: Wide layout mode enabled via `st.set_page_config(layout="wide")`
- **Interactive Elements**: Button clicks, text inputs, and radio selections trigger reruns

## Common Modifications

When adding new weather metrics or changing display:
1. Update parsing functions in `weather_service.py` to extract new fields from API response
2. Add formatting functions to `utils.py` if data transformation is needed
3. Update UI rendering in `app.py` to display the new data
4. Check OpenWeatherMap API docs for available fields: https://openweathermap.org/current

When changing API endpoints or adding new data sources:
1. Add new methods to `WeatherService` class following the pattern: `get_*()` and `parse_*()`
2. Handle errors consistently with `{"error": "message"}` dict format
3. Update `app.py` to call new methods and handle responses
