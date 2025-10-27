"""
Real-Time Weather App
A Streamlit application for displaying current weather and forecasts.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from weather_service import WeatherService
from utils import (
    get_weather_icon,
    format_timestamp,
    format_date,
    get_wind_direction,
    celsius_to_fahrenheit
)

# Page configuration
st.set_page_config(
    page_title="Real-Time Weather App",
    page_icon="🌤️",
    layout="wide"
)

# Initialize weather service
@st.cache_resource
def get_weather_service():
    """Initialize and cache the weather service."""
    try:
        return WeatherService()
    except ValueError as e:
        st.error(f"⚠️ {e}")
        st.info("Please create a .env file with your OPENWEATHER_API_KEY")
        st.stop()

weather_service = get_weather_service()

# App header
st.title("🌤️ Real-Time Weather App")
st.markdown("Get current weather conditions and 5-day forecasts for any city worldwide")

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Temperature unit toggle
    temp_unit = st.radio(
        "Temperature Unit",
        options=["Celsius (°C)", "Fahrenheit (°F)"],
        index=0
    )
    units = "metric" if "Celsius" in temp_unit else "imperial"
    unit_symbol = "°C" if units == "metric" else "°F"
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app uses the **OpenWeatherMap API** to provide real-time weather data.")
    st.markdown("Enter a city name to get started!")

# Main content
# City input
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("🔍 Enter city name", placeholder="e.g., New York, London, Tokyo")
with col2:
    search_button = st.button("Search", type="primary", use_container_width=True)

# Fetch and display weather when city is entered
if city and (search_button or city):
    with st.spinner(f"Fetching weather data for {city}..."):
        # Get current weather
        current_data = weather_service.get_current_weather(city, units)
        weather = weather_service.parse_current_weather(current_data)
        
        if "error" in weather:
            st.error(f"❌ {weather['error']}")
        else:
            # Current weather section
            st.markdown("---")
            st.header(f"Current Weather in {weather['city']}, {weather['country']}")
            
            # Weather icon and main info
            col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
            
            with col1:
                icon = get_weather_icon(weather['weather_id'], weather['weather_description'])
                st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{icon}</h1>", 
                           unsafe_allow_html=True)
            
            with col2:
                st.metric("Temperature", f"{weather['temperature']:.1f}{unit_symbol}")
                st.caption(f"Feels like: {weather['feels_like']:.1f}{unit_symbol}")
            
            with col3:
                st.metric("Humidity", f"{weather['humidity']}%")
                st.metric("Pressure", f"{weather['pressure']} hPa")
            
            with col4:
                wind_dir = get_wind_direction(weather['wind_deg'])
                wind_unit = "m/s" if units == "metric" else "mph"
                st.metric("Wind Speed", f"{weather['wind_speed']:.1f} {wind_unit}")
                st.caption(f"Direction: {wind_dir}")
            
            # Weather description
            st.markdown(f"### {weather['weather_main']} - {weather['weather_description'].title()}")
            
            # Additional details
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**☀️ Sunrise**")
                sunrise_time = format_timestamp(weather['sunrise'], weather['timezone'])
                st.write(sunrise_time)
            
            with col2:
                st.markdown("**🌅 Sunset**")
                sunset_time = format_timestamp(weather['sunset'], weather['timezone'])
                st.write(sunset_time)
            
            with col3:
                st.markdown("**☁️ Cloudiness**")
                st.write(f"{weather['clouds']}%")
            
            with col4:
                st.markdown("**👁️ Visibility**")
                st.write(f"{weather['visibility']:.1f} km")
            
            # Fetch and display forecast
            st.markdown("---")
            st.header("📊 5-Day Forecast")
            
            forecast_data = weather_service.get_forecast(city, units)
            forecast = weather_service.parse_forecast(forecast_data)
            
            if "error" in forecast:
                st.error(f"❌ Failed to fetch forecast: {forecast['error']}")
            else:
                # Prepare data for chart
                df = pd.DataFrame(forecast)
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
                df['date'] = df['datetime'].dt.strftime('%a, %b %d')
                df['time'] = df['datetime'].dt.strftime('%I %p')
                
                # Create interactive temperature chart
                fig = go.Figure()
                
                # Add temperature line
                fig.add_trace(go.Scatter(
                    x=df['datetime'],
                    y=df['temperature'],
                    mode='lines+markers',
                    name='Temperature',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{x|%a, %b %d - %I %p}</b><br>' +
                                  f'Temperature: %{{y:.1f}}{unit_symbol}<br>' +
                                  '<extra></extra>'
                ))
                
                # Add feels like line
                fig.add_trace(go.Scatter(
                    x=df['datetime'],
                    y=df['feels_like'],
                    mode='lines',
                    name='Feels Like',
                    line=dict(color='#FFA500', width=2, dash='dash'),
                    hovertemplate='<b>%{x|%a, %b %d - %I %p}</b><br>' +
                                  f'Feels Like: %{{y:.1f}}{unit_symbol}<br>' +
                                  '<extra></extra>'
                ))
                
                # Update layout
                fig.update_layout(
                    title=f"Temperature Forecast for {weather['city']}",
                    xaxis_title="Date & Time",
                    yaxis_title=f"Temperature ({unit_symbol})",
                    hovermode='x unified',
                    height=400,
                    template='plotly_white',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Forecast cards
                st.markdown("### Detailed Forecast")
                
                # Group by day and show daily forecasts
                daily_forecasts = df.groupby('date').first().head(5)
                
                cols = st.columns(5)
                for idx, (date, row) in enumerate(daily_forecasts.iterrows()):
                    with cols[idx]:
                        icon = get_weather_icon(row['weather_id'], row['weather_description'])
                        st.markdown(f"**{date}**")
                        st.markdown(f"<h2 style='text-align: center;'>{icon}</h2>", 
                                   unsafe_allow_html=True)
                        st.markdown(f"**{row['temperature']:.0f}{unit_symbol}**")
                        st.caption(row['weather_description'].title())
                        st.caption(f"💧 {row['humidity']}%")
                        st.caption(f"☔ {row['pop']:.0f}%")

else:
    # Welcome message
    st.info("👆 Enter a city name above to get started!")
    
    # Sample cities
    st.markdown("### Try these popular cities:")
    sample_cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Mumbai", "Dubai", "Singapore"]
    
    cols = st.columns(4)
    for idx, sample_city in enumerate(sample_cities):
        with cols[idx % 4]:
            if st.button(sample_city, use_container_width=True):
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by OpenWeatherMap API | "
    "Data updates in real-time</p>",
    unsafe_allow_html=True
)
