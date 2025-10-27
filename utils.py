"""
Utility functions for the weather app.
Includes temperature conversions, weather icon mappings, and formatting helpers.
"""

from datetime import datetime


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9


def get_weather_icon(weather_code, description):
    """
    Map weather codes to emoji icons.
    
    Args:
        weather_code: OpenWeatherMap weather condition code
        description: Weather description string
    
    Returns:
        Emoji icon representing the weather condition
    """
    # Weather condition codes: https://openweathermap.org/weather-conditions
    icon_map = {
        # Thunderstorm (200-232)
        range(200, 233): "⛈️",
        # Drizzle (300-321)
        range(300, 322): "🌦️",
        # Rain (500-531)
        range(500, 505): "🌧️",
        range(505, 532): "🌧️",
        # Snow (600-622)
        range(600, 623): "❄️",
        # Atmosphere (700-781)
        range(700, 782): "🌫️",
        # Clear (800)
        800: "☀️",
        # Clouds (801-804)
        range(801, 805): "☁️",
    }
    
    # Check for specific code
    if weather_code in icon_map:
        return icon_map[weather_code]
    
    # Check for code ranges
    for code_range, icon in icon_map.items():
        if isinstance(code_range, range) and weather_code in code_range:
            return icon
    
    # Special cases based on description
    description_lower = description.lower()
    if "rain" in description_lower:
        return "🌧️"
    elif "cloud" in description_lower:
        return "☁️"
    elif "clear" in description_lower:
        return "☀️"
    elif "snow" in description_lower:
        return "❄️"
    elif "thunder" in description_lower or "storm" in description_lower:
        return "⛈️"
    
    # Default icon
    return "🌤️"


def format_timestamp(timestamp, timezone_offset=0):
    """
    Format Unix timestamp to readable time.
    
    Args:
        timestamp: Unix timestamp
        timezone_offset: Timezone offset in seconds
    
    Returns:
        Formatted time string (HH:MM AM/PM)
    """
    dt = datetime.fromtimestamp(timestamp + timezone_offset)
    return dt.strftime("%I:%M %p")


def format_date(timestamp):
    """
    Format Unix timestamp to readable date.
    
    Args:
        timestamp: Unix timestamp
    
    Returns:
        Formatted date string (Mon, Jan 01)
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%a, %b %d")


def get_wind_direction(degrees):
    """
    Convert wind direction in degrees to cardinal direction.
    
    Args:
        degrees: Wind direction in degrees (0-360)
    
    Returns:
        Cardinal direction string (N, NE, E, etc.)
    """
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]
