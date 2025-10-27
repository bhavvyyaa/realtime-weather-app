"""
Weather service module for interacting with OpenWeatherMap API.
Handles fetching current weather and 5-day forecast data.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherService:
    """Service class for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self, api_key=None):
        """
        Initialize the weather service.
        
        Args:
            api_key: OpenWeatherMap API key (optional, defaults to env variable)
        """
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("API key not found. Please set OPENWEATHER_API_KEY in .env file")
    
    def get_current_weather(self, city, units="metric"):
        """
        Fetch current weather data for a city.
        
        Args:
            city: City name
            units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)
        
        Returns:
            Dictionary containing weather data or None if request fails
        """
        url = f"{BASE_URL}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {"error": f"City '{city}' not found"}
            return {"error": f"HTTP error: {e}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}
    
    def get_forecast(self, city, units="metric"):
        """
        Fetch 5-day weather forecast for a city.
        
        Args:
            city: City name
            units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)
        
        Returns:
            Dictionary containing forecast data or None if request fails
        """
        url = f"{BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {"error": f"City '{city}' not found"}
            return {"error": f"HTTP error: {e}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}
    
    def parse_current_weather(self, data):
        """
        Parse current weather data into a simplified format.
        
        Args:
            data: Raw weather data from API
        
        Returns:
            Dictionary with parsed weather information
        """
        if "error" in data:
            return data
        
        try:
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "temp_min": data["main"]["temp_min"],
                "temp_max": data["main"]["temp_max"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "weather_id": data["weather"][0]["id"],
                "weather_main": data["weather"][0]["main"],
                "weather_description": data["weather"][0]["description"],
                "weather_icon": data["weather"][0]["icon"],
                "wind_speed": data["wind"]["speed"],
                "wind_deg": data["wind"].get("deg", 0),
                "clouds": data["clouds"]["all"],
                "sunrise": data["sys"]["sunrise"],
                "sunset": data["sys"]["sunset"],
                "timezone": data["timezone"],
                "visibility": data.get("visibility", 0) / 1000,  # Convert to km
            }
        except KeyError as e:
            return {"error": f"Failed to parse weather data: {e}"}
    
    def parse_forecast(self, data):
        """
        Parse forecast data into a simplified format.
        
        Args:
            data: Raw forecast data from API
        
        Returns:
            List of dictionaries with parsed forecast information
        """
        if "error" in data:
            return data
        
        try:
            forecast_list = []
            for item in data["list"]:
                forecast_list.append({
                    "timestamp": item["dt"],
                    "temperature": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "temp_min": item["main"]["temp_min"],
                    "temp_max": item["main"]["temp_max"],
                    "humidity": item["main"]["humidity"],
                    "weather_id": item["weather"][0]["id"],
                    "weather_main": item["weather"][0]["main"],
                    "weather_description": item["weather"][0]["description"],
                    "weather_icon": item["weather"][0]["icon"],
                    "wind_speed": item["wind"]["speed"],
                    "clouds": item["clouds"]["all"],
                    "pop": item.get("pop", 0) * 100,  # Probability of precipitation
                })
            return forecast_list
        except KeyError as e:
            return {"error": f"Failed to parse forecast data: {e}"}
